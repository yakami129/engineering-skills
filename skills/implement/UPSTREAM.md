# 上游来源

- 作者：Matt Pocock
- 仓库：[mattpocock/skills](https://github.com/mattpocock/skills)
- 固定提交：[`4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`](https://github.com/mattpocock/skills/commit/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d)
- 原目录：[`skills/engineering/implement/`](https://github.com/mattpocock/skills/tree/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/implement)
- 许可证：[MIT，Copyright (c) 2026 Matt Pocock](LICENSE)

`SKILL.md` 做了一项兼容调整：将依赖专用 Skill 工具的两处调用改为读取同级的 `tdd` 和 `code-review` 技能，并注明两者须一并安装，使没有该工具的 Agent 也能使用。保留上游的 `disable-model-invocation: true` 和 Codex 的 `allow_implicit_invocation: false`，维持手动调用入口。`agents/openai.yaml` 保持上游原文。

此目录额外包含本来源记录，以及从上游根目录复制的许可证，确保单独安装时保留版权声明。更新时对照固定提交检查文件、依赖与调用策略，再通过 PR 更新内容和版本记录。
