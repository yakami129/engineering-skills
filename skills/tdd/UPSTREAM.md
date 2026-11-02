# 上游来源

- 作者：Matt Pocock
- 仓库：[mattpocock/skills](https://github.com/mattpocock/skills)
- 固定提交：[`4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`](https://github.com/mattpocock/skills/commit/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d)
- 原目录：[`skills/engineering/tdd/`](https://github.com/mattpocock/skills/tree/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/tdd)
- 许可证：[MIT，Copyright (c) 2026 Matt Pocock](LICENSE)

`SKILL.md` 做了一项兼容调整：上游通过 Skill 工具调用 `codebase-design` 获取模块、接口、深度、seam 等术语，改为读取同级的 `codebase-design` 技能；该技能仅在讨论接口形态时参考，故保留「如已安装」，`tdd` 仍可单独安装。`tests.md`、`mocking.md` 和 `agents/openai.yaml` 保持上游原文。

此目录额外包含本来源记录，以及从上游根目录复制的许可证，确保单独安装时保留版权声明。更新时对照固定提交检查文件、依赖与调用策略，再通过 PR 更新内容和版本记录。
