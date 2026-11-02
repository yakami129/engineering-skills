import json
import subprocess
import unittest

from tools.skills import ROOT


SCRIPT = ROOT / "skills/ponytail-lite/scripts/inject-context.sh"


def run_hook(event):
    # Agent 会把事件 JSON 写进 stdin；脚本不读取 stdin，这里照样传入，确认不会阻塞。
    result = subprocess.run(
        ["sh", str(SCRIPT), event],
        input='{"hook_event_name": "%s"}' % event,
        capture_output=True,
        text=True,
        timeout=5,
        check=True,
    )
    return json.loads(result.stdout)


class PonytailLiteHookTests(unittest.TestCase):
    def test_session_start_injects_rules_without_frontmatter(self):
        """SessionStart：输出 Claude Code 与 Codex 共用的 additionalContext JSON，正文为规则全文。

        数据构造：
          skills/ponytail-lite/SKILL.md = YAML frontmatter + 上游 AGENTS.md 正文（约 2.6k 字符）

        执行过程：
          1. sh inject-context.sh SessionStart → 去掉 frontmatter，读取正文
          2. 正文做 JSON 转义，套进 hookSpecificOutput → stdout 是一个 JSON 对象

        预期结果：
          - hookEventName 为 SessionStart：两个 Agent 都按它路由上下文
          - 包含阶梯中的一级与「何时不偷懒」：说明正文完整注入
          - 不包含 frontmatter 的 name 行：元数据不应进入上下文
          - 长度低于 8000 字符：Claude Code 单条上限 10000 字符，Codex 默认约 2500 token
        """
        output = run_hook("SessionStart")["hookSpecificOutput"]
        context = output["additionalContext"]

        self.assertEqual(output["hookEventName"], "SessionStart", "事件名错误，Agent 不会把内容当作会话上下文")
        self.assertIn("Does the standard library do it?", context, "阶梯规则缺失，正文没有完整注入")
        self.assertIn("When not to be lazy:", context, "安全边界段缺失，正文被截断")
        self.assertNotIn("name: ponytail-lite", context, "frontmatter 泄漏进了上下文")
        self.assertLess(len(context), 8000, "上下文过长，会被 Agent 改为落盘预览")

    def test_subagent_start_uses_its_own_event_name(self):
        """SubagentStart：子 Agent 拿不到父会话的 SessionStart 上下文，需要单独注入。

        执行过程：
          1. sh inject-context.sh SubagentStart → 输出同样的规则

        预期结果：
          - hookEventName 为 SubagentStart：事件名不匹配时 Agent 会忽略这段输出
          - 仍包含阶梯规则：子 Agent 写代码时同样受约束
        """
        output = run_hook("SubagentStart")["hookSpecificOutput"]

        self.assertEqual(output["hookEventName"], "SubagentStart", "子 Agent 事件名错误，规则不会注入")
        self.assertIn("Does the standard library do it?", output["additionalContext"], "子 Agent 没有收到阶梯规则")


if __name__ == "__main__":
    unittest.main()
