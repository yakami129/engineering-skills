# 上游来源

- 作者：Matt Pocock
- 仓库：[mattpocock/skills](https://github.com/mattpocock/skills)
- 固定提交：[`4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`](https://github.com/mattpocock/skills/commit/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d)
- 原目录：[`skills/productivity/grilling/`](https://github.com/mattpocock/skills/tree/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/productivity/grilling)、[`skills/engineering/grill-with-docs/`](https://github.com/mattpocock/skills/tree/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/grill-with-docs)
- 许可证：[MIT，Copyright (c) 2026 Matt Pocock](LICENSE)

本技能由上游 `grilling` 与 `grill-with-docs` 合并而成，名称取自上游的手动入口 [`grill-me`](https://github.com/mattpocock/skills/tree/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/productivity/grill-me)，通过 `/grill-me`（Codex 为 `$grill-me`）调用。与上游的差异：

- `SKILL.md` 直接内联上游 `grilling` 的设计树、frontier 与推荐答案机制，不再依赖单独的 `grilling` 技能；上游原有段落保持原文。
- 在此之上并入仓库作者自己编写的采访模式技能（interview-spec）的做法：开场复述目标并提炼已知信息、按需使用结构化提问工具、每轮先小结、控制每轮问题数量、不问可由常识决定的细节，以及结束前对照 `COVERAGE.md` 检查。
- 保留上游 `grill-with-docs` 的文档职责：读取同级 `domain-modeling` 技能维护术语表与 ADR（原为 Skill 工具调用，改为读取同级文件），讨论功能或系统时另产出 SPEC，写入 `docs/exec-plans/YYYY-MM-DD-<slug>.md`。
- `COVERAGE.md`（十维覆盖清单）与 `SPEC-FORMAT.md`（SPEC 模板）来自同一采访模式，非上游文件。
- 保留 `disable-model-invocation: true` 与 Codex 的 `allow_implicit_invocation: false`，维持手动调用；`description` 与 `agents/openai.yaml` 相应调整。

安装时需同时安装 `domain-modeling`。此目录额外包含本来源记录，以及从上游根目录复制的许可证，确保单独安装时保留版权声明。更新时对照固定提交检查上述三个上游目录、依赖与调用策略，再通过 PR 更新内容和版本记录。
