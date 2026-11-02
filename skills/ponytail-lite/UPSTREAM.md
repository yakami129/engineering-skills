# 上游来源

- 作者：Daniel Ilin（ilindaniel），基于 DietrichGebert 的 [Ponytail](https://github.com/DietrichGebert/ponytail)
- 仓库：[ilindaniel/ponytail-lite](https://github.com/ilindaniel/ponytail-lite)
- 固定提交：[`e7b42dc2d384a702240dea4d52a7bf5530b821b6`](https://github.com/ilindaniel/ponytail-lite/commit/e7b42dc2d384a702240dea4d52a7bf5530b821b6)
- 原文件：[`AGENTS.md`](https://github.com/ilindaniel/ponytail-lite/blob/e7b42dc2d384a702240dea4d52a7bf5530b821b6/AGENTS.md)
- 许可证：[MIT，Copyright (c) 2026 DietrichGebert、Daniel Ilin](LICENSE)

上游只有一个 `AGENTS.md`，要求复制到 Agent 的项目指令文件中。本目录把它改为技能分发：`SKILL.md` 正文保持上游 `AGENTS.md` 原文，只增加 frontmatter，作为模型可自动调用的技能。

为了不改 `AGENTS.md` 或 `CLAUDE.md` 也能常驻生效，额外提供 `scripts/inject-context.sh` 与 `HOOKS.md`：通过 Claude Code 和 Codex 的 `SessionStart`、`SubagentStart` hook，把正文作为 `additionalContext` 注入每个会话和子 Agent。这一做法取自完整版 Ponytail 的 hook 设计，但只保留注入规则这一项，不含模式切换、状态栏与代码地图。脚本只依赖 `sh`、`sed`、`awk`，注入时会在正文前加一句说明来源的陈述句。`agents/openai.yaml` 为本仓库新增。

更新时对照固定提交比对 `AGENTS.md`，同步 `SKILL.md` 正文，再运行 `tests/test_ponytail_lite_hook.py` 确认注入内容完整。
