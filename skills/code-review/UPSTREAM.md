# 上游来源

- 作者：Matt Pocock
- 仓库：[mattpocock/skills](https://github.com/mattpocock/skills)
- 固定提交：[`4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`](https://github.com/mattpocock/skills/commit/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d)
- 原目录：[`skills/engineering/code-review/`](https://github.com/mattpocock/skills/tree/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/code-review)
- 许可证：[MIT，Copyright (c) 2026 Matt Pocock](LICENSE)

`SKILL.md` 做了一项兼容调整：上游在未配置 issue tracker 时提示运行 `/setup-matt-pocock-skills`，本仓库未迁入该技能，改为询问用户 spec 所在的 tracker 及读取方式。其余流程（两轴审查、Fowler 坏味道基线、并行子 Agent）与 `agents/openai.yaml` 保持上游原文。

此目录额外包含本来源记录，以及从上游根目录复制的许可证，确保单独安装时保留版权声明。更新时对照固定提交检查文件、依赖与调用策略，再通过 PR 更新内容和版本记录。
