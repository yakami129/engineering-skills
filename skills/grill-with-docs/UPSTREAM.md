# 上游来源

- 作者：Matt Pocock
- 仓库：[mattpocock/skills](https://github.com/mattpocock/skills)
- 固定提交：[`4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`](https://github.com/mattpocock/skills/commit/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d)
- 原目录：[`skills/engineering/grill-with-docs/`](https://github.com/mattpocock/skills/tree/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/grill-with-docs)
- 许可证：[MIT，Copyright (c) 2026 Matt Pocock](LICENSE)

`SKILL.md` 做了一项兼容调整：将依赖专用 Skill 工具的调用语句改为读取同级的 `grilling` 和 `domain-modeling` 技能，使没有该工具的 Agent 也能使用。保留上游的 `disable-model-invocation: true` 和 Codex 的 `allow_implicit_invocation: false`，维持手动调用入口。此外新增 `## SPEC.md` 一节和 `SPEC-FORMAT.md`：讨论功能或系统时，在术语表与 ADR 之外产出规格文档，并划分三类文档的职责；结构与写入流程来自仓库作者自己编写的采访模式技能（interview-spec），非上游内容。`description` 与 `agents/openai.yaml` 的 `short_description` 相应补充了 spec。安装时需同时安装这两个依赖技能。

此目录额外包含本来源记录，以及从上游根目录复制的许可证，确保单独安装时保留版权声明。更新时对照固定提交检查文件、依赖与调用策略，再通过 PR 更新内容和版本记录。
