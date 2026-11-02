import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.skills import ROOT


SETUP = ROOT / "skills/setup-ponytail-lite/scripts/setup.py"
HOOK = ROOT / "skills/ponytail-lite/scripts/inject-context.sh"
OTHER = {"type": "command", "command": "/usr/local/bin/other-hook", "timeout": 5}


def ours(group):
    return any("ponytail-lite/scripts/inject-context.sh" in hook["command"] for hook in group["hooks"])


class SetupPonytailLiteTests(unittest.TestCase):
    def setUp(self):
        self.home = Path(tempfile.mkdtemp())
        self.claude = self.home / ".claude/settings.json"
        self.codex = self.home / ".codex/hooks.json"

    def run_setup(self, *args, check=True):
        env = dict(os.environ, HOME=str(self.home))
        env.pop("CODEX_HOME", None)
        return subprocess.run(
            ["python3", str(SETUP), *args],
            env=env, capture_output=True, text=True, timeout=10, check=check,
        )

    def write(self, path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data), encoding="utf-8")

    def read(self, path):
        return json.loads(path.read_text(encoding="utf-8"))

    def test_install_registers_both_events_for_both_agents(self):
        """全新环境：install 为两个 Agent 各登记 SessionStart 与 SubagentStart。

        数据构造：
          HOME = 空临时目录（没有 ~/.claude/settings.json，也没有 ~/.codex/hooks.json）

        执行过程：
          1. setup.py install → 默认 --agent all、--scope user
          2. 为每个文件创建 hooks.SessionStart / hooks.SubagentStart 各一组

        预期结果：
          - 两个文件都被创建：默认同时配置 Claude Code 与 Codex
          - SessionStart 的 matcher 为 startup|resume|clear|compact：/clear 与压缩后要重新注入
          - 命令指向仓库内的 inject-context.sh，并带上各自的事件名
          - SubagentStart 不带 matcher：每个子 Agent 都要注入
        """
        self.run_setup("install")

        for path in (self.claude, self.codex):
            hooks = self.read(path)["hooks"]
            session = hooks["SessionStart"]
            subagent = hooks["SubagentStart"]
            self.assertEqual(len(session), 1, f"{path} 的 SessionStart 应只有一组 ponytail-lite")
            self.assertEqual(session[0]["matcher"], "startup|resume|clear|compact", "matcher 缺少 clear/compact 会导致规则丢失")
            self.assertIn(str(HOOK), session[0]["hooks"][0]["command"], "命令应指向 ponytail-lite 的注入脚本")
            self.assertTrue(session[0]["hooks"][0]["command"].endswith(" SessionStart"), "SessionStart 命令应传入自身事件名")
            self.assertEqual(len(subagent), 1, f"{path} 的 SubagentStart 应只有一组 ponytail-lite")
            self.assertNotIn("matcher", subagent[0], "SubagentStart 不应限制子 Agent 类型")
            self.assertTrue(subagent[0]["hooks"][0]["command"].endswith(" SubagentStart"), "SubagentStart 命令应传入自身事件名")

    def test_install_appends_after_existing_hooks_and_keeps_other_keys(self):
        """已有配置：install 只追加，不改动其他 hook 与设置。

        数据构造：
          settings.json = {model: "opus", hooks.SessionStart: [其他 hook 一组]}
          hooks.json    = {hooks.SessionStart: [其他 hook 一组], hooks.Stop: [其他 hook 一组]}

        执行过程：
          1. setup.py install → 读取已有 JSON
          2. 在 SessionStart 数组末尾追加 ponytail-lite；新建 SubagentStart

        预期结果：
          - 其他 SessionStart 组仍在下标 0：Codex 按「文件:事件:组下标」记录信任，插到前面会让已信任的 hook 失效
          - ponytail-lite 位于下标 1
          - model 与 Stop 原样保留
        """
        self.write(self.claude, {"model": "opus", "hooks": {"SessionStart": [{"hooks": [OTHER]}]}})
        self.write(self.codex, {"hooks": {"SessionStart": [{"hooks": [OTHER]}], "Stop": [{"hooks": [OTHER]}]}})

        self.run_setup("install")

        claude = self.read(self.claude)
        codex = self.read(self.codex)
        self.assertEqual(claude["model"], "opus", "settings.json 中与 hook 无关的设置不应被改动")
        self.assertEqual(claude["hooks"]["SessionStart"][0], {"hooks": [OTHER]}, "已有 SessionStart 组应保持在下标 0")
        self.assertTrue(ours(claude["hooks"]["SessionStart"][1]), "ponytail-lite 应追加在已有组之后")
        self.assertEqual(codex["hooks"]["SessionStart"][0], {"hooks": [OTHER]}, "Codex 已信任的组下标不应移动")
        self.assertTrue(ours(codex["hooks"]["SessionStart"][1]), "Codex 中 ponytail-lite 应追加在末尾")
        self.assertEqual(codex["hooks"]["Stop"], [{"hooks": [OTHER]}], "无关事件应原样保留")

    def test_install_twice_is_idempotent(self):
        """重复 install：替换原有条目，不重复登记。

        数据构造：
          HOME = 空临时目录

        执行过程：
          1. setup.py install → 每个事件一组 ponytail-lite
          2. 再次 setup.py install → 识别命令中的 ponytail-lite/scripts/inject-context.sh，原位替换

        预期结果：
          - 每个文件的 SessionStart 与 SubagentStart 都仍只有一组：重复注入会让上下文出现两份规则
        """
        self.run_setup("install")
        self.run_setup("install")

        for path in (self.claude, self.codex):
            hooks = self.read(path)["hooks"]
            self.assertEqual(len(hooks["SessionStart"]), 1, f"{path} 重复安装后 SessionStart 出现多组")
            self.assertEqual(len(hooks["SubagentStart"]), 1, f"{path} 重复安装后 SubagentStart 出现多组")

    def test_uninstall_removes_only_ponytail_lite(self):
        """uninstall：只删除 ponytail-lite 的 hook，同组的其他 hook 保留。

        数据构造：
          settings.json.hooks.SessionStart = [其他 hook 一组]
          然后 install → SessionStart = [其他组, ponytail-lite 组]
          再手动把 OTHER 并入 SubagentStart 的 ponytail-lite 组 → 一组两个 hook

        执行过程：
          1. setup.py uninstall --agent claude
          2. 删除命令含 ponytail-lite 注入脚本的 hook；删空的组与空数组一并移除

        预期结果：
          - SessionStart 只剩其他组：ponytail-lite 组被删除
          - SubagentStart 剩一组且只有 OTHER：混合组只删我们的 hook
          - Codex 文件未被创建：--agent claude 不应触碰 Codex
        """
        self.write(self.claude, {"hooks": {"SessionStart": [{"hooks": [OTHER]}]}})
        self.run_setup("install", "--agent", "claude")
        settings = self.read(self.claude)
        settings["hooks"]["SubagentStart"][0]["hooks"].append(OTHER)
        self.write(self.claude, settings)

        self.run_setup("uninstall", "--agent", "claude")

        hooks = self.read(self.claude)["hooks"]
        self.assertEqual(hooks["SessionStart"], [{"hooks": [OTHER]}], "SessionStart 应只剩其他 hook 组")
        self.assertEqual(hooks["SubagentStart"], [{"hooks": [OTHER]}], "混合组中的其他 hook 应保留")
        self.assertFalse(self.codex.exists(), "--agent claude 不应创建 Codex 配置")

    def test_installed_command_runs_and_injects_rules(self):
        """端到端：安装后的命令可以直接执行，输出 ponytail-lite 规则。

        数据构造：
          HOME = 空临时目录

        执行过程：
          1. setup.py install --agent codex
          2. 取出 SessionStart 命令，用 sh -c 执行（Agent 运行 hook 的方式）

        预期结果：
          - 输出是 hookEventName 为 SessionStart 的 JSON
          - additionalContext 包含阶梯第 3 级：说明注入的是完整规则
        """
        self.run_setup("install", "--agent", "codex")
        command = self.read(self.codex)["hooks"]["SessionStart"][0]["hooks"][0]["command"]

        output = subprocess.run(["sh", "-c", command], capture_output=True, text=True, timeout=5, check=True)

        payload = json.loads(output.stdout)["hookSpecificOutput"]
        self.assertEqual(payload["hookEventName"], "SessionStart", "登记的命令应输出 SessionStart 事件")
        self.assertIn("Does the standard library do it?", payload["additionalContext"], "登记的命令没有注入规则正文")

    def test_invalid_json_is_left_untouched(self):
        """配置损坏：拒绝写入，原文件保持不变。

        数据构造：
          settings.json = "{not json"

        执行过程：
          1. setup.py install --agent claude → 解析失败

        预期结果：
          - 退出码非 0：调用方需要知道没有安装成功
          - 文件内容仍是 "{not json"：不能用空配置覆盖用户已有设置
        """
        self.claude.parent.mkdir(parents=True)
        self.claude.write_text("{not json", encoding="utf-8")

        result = self.run_setup("install", "--agent", "claude", check=False)

        self.assertNotEqual(result.returncode, 0, "损坏的 JSON 应让安装失败")
        self.assertEqual(self.claude.read_text(encoding="utf-8"), "{not json", "损坏的配置不应被覆盖")

    def test_missing_hook_script_fails_before_writing(self):
        """注入脚本不存在：不写入任何配置。

        数据构造：
          --hook-script = HOME/missing.sh（不存在）

        执行过程：
          1. setup.py install --hook-script missing.sh → 检查脚本存在性失败

        预期结果：
          - 退出码非 0，stderr 提示安装 ponytail-lite
          - 两个配置文件都未创建：登记一个不存在的脚本会让每次会话启动时 hook 报错
        """
        result = self.run_setup("install", "--hook-script", str(self.home / "missing.sh"), check=False)

        self.assertNotEqual(result.returncode, 0, "缺少注入脚本时应失败")
        self.assertIn("ponytail-lite", result.stderr, "错误信息应提示先安装 ponytail-lite")
        self.assertFalse(self.claude.exists(), "失败时不应创建 Claude Code 配置")
        self.assertFalse(self.codex.exists(), "失败时不应创建 Codex 配置")

    def test_status_reports_installed_hooks_and_full_ponytail_conflict(self):
        """status：报告登记状态，并发现已启用的完整版 Ponytail 插件。

        数据构造：
          ~/.codex/config.toml 含 [plugins."ponytail@ponytail"] enabled = true
          install --agent codex 之后执行 status

        执行过程：
          1. setup.py status → 逐个 Agent 读取 hook 文件与插件配置

        预期结果：
          - Codex 两个事件都显示 installed
          - Claude Code 显示 not installed：从未安装
          - 输出提到 ponytail@ponytail：两套规则会同时注入，需要提醒停用
        """
        (self.home / ".codex").mkdir()
        (self.home / ".codex/config.toml").write_text(
            '[plugins."ponytail@ponytail"]\nenabled = true\n\n[plugins."other@x"]\nenabled = false\n',
            encoding="utf-8",
        )
        self.run_setup("install", "--agent", "codex")

        output = self.run_setup("status").stdout

        self.assertIn("codex SessionStart: installed", output, "Codex SessionStart 应显示已安装")
        self.assertIn("codex SubagentStart: installed", output, "Codex SubagentStart 应显示已安装")
        self.assertIn("claude SessionStart: not installed", output, "Claude Code 未安装时应如实显示")
        self.assertIn("ponytail@ponytail", output, "应提示已启用的完整版 Ponytail 插件")


if __name__ == "__main__":
    unittest.main()
