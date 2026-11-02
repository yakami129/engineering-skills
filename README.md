<h1 align="center">Engineering Skills</h1>

<p align="center">
  <strong>想清楚 · 做最小的改动 · 每一步都验证</strong><br />
  把反复使用的工程方法，整理成 Claude Code、Codex 等 AI Agent 能按需调用的技能。
</p>

<p align="center">
  <a href="#技能目录">技能目录</a> ·
  <a href="#工作流">工作流</a> ·
  <a href="#快速开始">快速开始</a> ·
  <a href="#常驻加载ponytail-lite-与-hook">常驻加载</a> ·
  <a href="#开发与贡献">开发与贡献</a> ·
  <a href="https://github.com/yakami129/engineering-skills/issues">反馈</a>
</p>

<p align="center">
  <a href="https://github.com/yakami129/engineering-skills/actions/workflows/check.yml"><img src="https://github.com/yakami129/engineering-skills/actions/workflows/check.yml/badge.svg" alt="Check skills" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-111214" alt="MIT License" /></a>
  <a href="https://agentskills.io/specification"><img src="https://img.shields.io/badge/format-Agent_Skills-111214" alt="Agent Skills format" /></a>
  <img src="https://img.shields.io/badge/agents-Claude_Code_%7C_Codex_%7C_Cursor-111214" alt="Claude Code, Codex, Cursor" />
</p>

**一个技能一个目录，一个目录讲清楚一件事。** 从需求追问、领域建模、原型验证，到 TDD 实现、两轴审查和疑难排障，每个技能都写明输入、关键判断和完成标准，Agent 只在任务相关时读取。需要每轮生效的规则（如 `ponytail-lite`）通过生命周期 hook 常驻加载，不必改动 `AGENTS.md`。

组织方式参考 [Matt Pocock 的 skills 仓库](https://github.com/mattpocock/skills)。迁入的第三方技能在各自目录中保留来源、固定版本与许可证。

## 工作流

```text
想法 / 需求
      |  /grill-me             分轮追问，对照十维清单查漏，产出 docs/exec-plans/ 下的 SPEC
      v
设计
      +-- domain-modeling      术语表 GLOSSARY.md 与 ADR
      +-- codebase-design      深模块、接口与 seam 的共享术语
      +-- prototype            单文件逻辑演示，或可切换的多方案 UI
      v
实现  /implement
      +-- tdd                  在约定的 seam 上走红绿循环
      +-- code-review          编码规范 × spec 符合度，两轴并行审查
      v
排障  diagnosing-bugs          建立反馈循环 → 复现 → 最小化 → 验证假设 → 修复

常驻  ponytail-lite            每个会话与子 Agent 都带着「先复用、最小改动」的规则
      /setup-ponytail-lite    一次登记 SessionStart 与 SubagentStart hook
```

技能之间通过产物衔接：`grill-me` 写下的 `GLOSSARY.md`、ADR 与 `docs/exec-plans/` 下的 SPEC，是 `implement`、`tdd` 和 `code-review` 的输入。

可以这样开始：

| 你可以说 | 会发生什么 |
| --- | --- |
| “/grill-me 帮我梳理订单取消与退款的设计” | 一次只问一个分支，确定的术语写进 `GLOSSARY.md`，有取舍的决定记成 ADR，最后产出 SPEC |
| “用 $prototype 做三种布局不同的设置页方案” | 在已有页面中做出可通过 `?variant=` 切换的方案，方便并排比较 |
| “/implement 按 docs/exec-plans/2026-06-21-order-refund.md 实现退款” | 先约定测试 seam，按垂直切片走 TDD，完成后两轴审查并提交 |
| “这个接口偶发超时，帮我查一下” | 先建立能稳定复现的反馈循环，再逐个验证假设，修复后补回归检查 |
| “/setup-ponytail-lite” | 检查依赖与冲突，确认后把规则登记为 Claude Code 与 Codex 的常驻 hook |

## 技能目录

| 技能 | 调用 | 用途 |
| --- | --- | --- |
| [grill-me](skills/grill-me/SKILL.md) | `/grill-me` | 围绕计划、设计或功能需求分轮追问，对照十维覆盖清单查漏，边讨论边维护术语表与 ADR，讨论功能时产出 `docs/exec-plans/YYYY-MM-DD-<slug>.md`；依赖 `domain-modeling`；[合并说明与来源](skills/grill-me/UPSTREAM.md) |
| [domain-modeling](skills/domain-modeling/SKILL.md) | 自动 | 在设计讨论中明确项目术语和概念边界，维护 `GLOSSARY.md` 并记录重要 ADR；[来源与版本](skills/domain-modeling/UPSTREAM.md) |
| [codebase-design](skills/codebase-design/SKILL.md) | 自动 | 深模块设计的共享术语（module、interface、seam、adapter、depth 等）与原则，附模块深化和多方案接口设计方法；[来源与版本](skills/codebase-design/UPSTREAM.md) |
| [prototype](skills/prototype/SKILL.md) | 自动 | 用可交互原型验证设计问题：单文件 HTML 逻辑演示，或可切换的多方案 UI 布局；[来源与版本](skills/prototype/UPSTREAM.md) |
| [implement](skills/implement/SKILL.md) | `/implement` | 按 spec 或工单实现，在约定的 seam 上走 TDD，完成后做两轴审查并提交；依赖 `tdd` 与 `code-review`；[兼容调整与来源](skills/implement/UPSTREAM.md) |
| [tdd](skills/tdd/SKILL.md) | 自动 | 先与用户约定测试 seam，再按垂直切片走红绿循环，附好测试示例与 mock 原则；[兼容调整与来源](skills/tdd/UPSTREAM.md) |
| [code-review](skills/code-review/SKILL.md) | 自动 | 审查某个固定点以来的改动，用并行子 Agent 分别检查编码规范（含 Fowler 坏味道基线）与 spec 符合度；[兼容调整与来源](skills/code-review/UPSTREAM.md) |
| [diagnosing-bugs](skills/diagnosing-bugs/SKILL.md) | 自动 | 疑难故障与性能回归诊断：建立反馈循环、复现并最小化、验证假设、修复与回归检查；[来源与版本](skills/diagnosing-bugs/UPSTREAM.md) |
| [ponytail-lite](skills/ponytail-lite/SKILL.md) | 自动 / hook 常驻 | 懒惰资深开发者规则：写代码前依次确认是否需要、代码库、标准库、平台、已装依赖能否解决，只写最小可用改动，不削减校验与安全；[改编说明与来源](skills/ponytail-lite/UPSTREAM.md) |
| [setup-ponytail-lite](skills/setup-ponytail-lite/SKILL.md) | `/setup-ponytail-lite` | 把 `ponytail-lite` 登记为 Claude Code 与 Codex 的 `SessionStart`/`SubagentStart` hook；可查看状态、重装与卸载，不改动其他 hook |
| [meeting-notes](skills/meeting-notes/SKILL.md) | 自动 | 将会议记录整理成结论、决策、待办和待确认问题；作为写作示例，可直接修改或删除 |

「自动」表示 Agent 判断任务相关时自行加载；带斜杠命令的技能只能手动调用（Codex 中使用 `$技能名`），因为它们会主导整个流程或修改你的配置。

## 快速开始

### 1. 安装技能

使用 [skills CLI](https://github.com/vercel-labs/skills)（需要 Node.js），在需要使用技能的项目中运行：

```bash
# 只查看可用技能，不安装
npx skills@latest add yakami129/engineering-skills --list

# 交互选择技能和目标 Agent
npx skills@latest add yakami129/engineering-skills

# 只给当前项目的 Codex 安装调试技能
npx skills@latest add yakami129/engineering-skills --skill diagnosing-bugs -a codex
```

同一安装器也支持 Claude Code、Cursor 等 Agent。默认装在当前项目，跨项目使用时加 `-g`。安装后的技能不会自动跟随本仓库更新，可用 `npx skills@latest check` 和 `npx skills@latest update` 检查和更新。

### 2. 让 ponytail-lite 常驻

```bash
npx skills@latest add yakami129/engineering-skills \
  --skill ponytail-lite --skill setup-ponytail-lite -g
```

然后在 Claude Code 中输入 `/setup-ponytail-lite`（Codex 中为 `$setup-ponytail-lite`），按提示确认要配置的 Agent 与范围。原理见[常驻加载](#常驻加载ponytail-lite-与-hook)。

### 3. 从一次讨论开始

> /grill-me 帮我梳理订单取消与退款的设计；确定术语后及时写入 GLOSSARY.md，重要且有取舍的决定记录为 ADR。

讨论产出 `docs/exec-plans/YYYY-MM-DD-<slug>.md` 后，用 `/implement` 进入实现。

## 项目上下文：GLOSSARY.md 与 ADR

Matt 旧版示例中的 `CONTEXT.md` 是项目共享术语表；当前技能把它命名为 `GLOSSARY.md`。这套机制让开发者和 Agent 对同一概念使用同一个名字，并在讨论中持续维护定义。

| 文件 | 记录什么 | 何时创建 |
| --- | --- | --- |
| `GLOSSARY.md` | 项目特有的术语、定义与应避免的别名 | 第一个术语确定时 |
| `docs/adr/0001-事项.md` | 重要决策及其理由，保留真实的取舍 | 决策难以逆转、缺少上下文会令人意外、且确实比较过替代方案时 |
| `GLOSSARY-MAP.md` | 多个业务上下文的术语表位置及关系 | 项目确实存在多个上下文时 |

```bash
npx skills@latest add yakami129/engineering-skills \
  --skill domain-modeling --skill grill-me -a codex
```

日常只维护术语或决策时，可以直接使用 `$domain-modeling`。`grill-me` 不会自动替你安装它依赖的 `domain-modeling`。若希望后续任务也按需读取这些文件，可在目标项目的 `AGENTS.md` 中加入读取约定：

```markdown
讨论业务术语或修改领域行为时，先读取 GLOSSARY.md（如果存在）；涉及设计取舍时，读取 docs/adr/ 中的相关决策。术语变化使用 domain-modeling 技能同步维护。
```

已有 `CONTEXT.md` 的项目，应先检查其内容与引用，再决定是否迁移到当前约定。术语表保持精简，实施计划、临时笔记和实现细节各自保存在合适的项目文档中。

## 原型设计：逻辑与界面

`prototype` 根据你要验证的问题选择输出：

- **逻辑与状态**：生成单个 HTML 文件，提供当前状态、自由操作按钮和分场景引导，直接打开即可体验。示例：`用 $prototype 做一个订单取消与退款的状态演示，验证部分取消后哪些退款动作仍然合法。`
- **界面与布局**：优先在项目已有页面中制作结构不同的方案，通过 `?variant=` 和底部切换栏比较，默认 3 个方案。示例：`用 $prototype 为设置页面做三种信息层级和布局不同的方案，方便切换比较。`

原型用于快速回答设计问题。确定方案后，把经过验证的逻辑或设计落实到正式代码，将原型保存在独立的临时分支并记录结论；主分支保留确认后的实现。

## 常驻加载：ponytail-lite 与 hook

技能默认按需加载：Agent 判断任务相关时才读取正文。`ponytail-lite` 这类需要每轮都生效的规则，上游的做法是复制进 `AGENTS.md`。如果不想改这些文件，可以用 Agent 的生命周期 hook 注入：

| 方式 | 何时生效 | 代价 |
| --- | --- | --- |
| 只装技能 | Agent 自行判断时 | 不保证每次都用上 |
| `SessionStart` + `SubagentStart` hook | 每个会话启动、`/clear` 与压缩后，以及每个子 Agent | 需在 Agent 配置中登记两条 hook；Codex 需在 `/hooks` 中信任 |
| 写入 `AGENTS.md` / `CLAUDE.md` | 每个会话 | 与项目指令混在一起 |

```text
会话启动 / /clear / 压缩 ──SessionStart──┐
子 Agent 启动 ───────────SubagentStart──┤
                                       v
            sh ponytail-lite/scripts/inject-context.sh <事件>
                                       |  去掉 frontmatter，输出 JSON
                                       v
      {"hookSpecificOutput": {"additionalContext": "<规则全文>"}}
                                       |
                                       v
                  Claude Code / Codex 把规则放进上下文
```

两个 Agent 读取同一种输出格式，所以一份脚本同时适用，只依赖 `sh`、`sed` 和 `awk`。`/setup-ponytail-lite` 负责登记：

```bash
python3 ~/.agents/skills/setup-ponytail-lite/scripts/setup.py status            # 查看登记状态与冲突
python3 ~/.agents/skills/setup-ponytail-lite/scripts/setup.py install --agent all
python3 ~/.agents/skills/setup-ponytail-lite/scripts/setup.py uninstall --agent all
```

- 追加在已有 hook 之后，重复安装只替换自己的条目；修改前写入 `<文件>.ponytail-lite.bak`，配置不是合法 JSON 时拒绝写入。
- 已启用完整版 Ponytail 插件时会给出提醒，先停用它，避免注入两套规则。
- 卸载 `ponytail-lite` 前先运行 `uninstall`，否则每次会话都会触发一个找不到脚本的 hook。

手动配置方法见 [HOOKS.md](skills/ponytail-lite/HOOKS.md)。

## 开发与贡献

开发工具需要 Python 3.9+；安装和使用技能本身不需要 Python。

```bash
git clone https://github.com/yakami129/engineering-skills.git
cd engineering-skills
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt

# 生成一个待完善的技能
python tools/skills.py new my-skill \
  --description "把访谈记录整理成用户需求；用于访谈结束后的需求提炼。"

# 提交前检查
python tools/skills.py check
python -m unittest discover -s tests -v
```

编辑 `skills/my-skill/SKILL.md`，替换其中的 `[TODO: ...]`，并在上面的技能目录补一行。每次新增技能使用独立分支和 Pull Request，完整步骤见[贡献指南](CONTRIBUTING.md)。

```text
skills/
  <name>/
    SKILL.md                  必需：frontmatter（name、description）+ 正文
    agents/openai.yaml        可选：Codex 显示信息与调用策略
    scripts/                  可选：可执行工具
    references/               可选：按需读取的长资料
    LICENSE / UPSTREAM.md     迁入技能：上游许可与版本记录
templates/SKILL.md.template   不会被安装器当作技能发现的模板
tools/skills.py               新建技能和检查格式
tests/                        工具与脚本的行为测试
.github/workflows/check.yml   推送和 PR 自动检查
```

### 写一个好用的技能

- `name` 与目录名一致，使用小写字母、数字和连字符。
- `description` 写清楚「做什么、什么时候用」，让 Agent 能判断是否适用。
- 正文写输入、关键步骤和完成标准，保留真正来自你经验的判断方法。
- 较长资料放到 `references/`，并在正文注明何时读取。
- 用一个真实请求试跑后再调整。格式检查只验证结构，无法证明技能效果。

公开提交前检查内容归属，使用虚构或脱敏示例。凭据、客户原始资料和未获准公开的内部流程应保存在合适的私有位置。

## 文档

| 想了解 | 从这里开始 |
| --- | --- |
| 如何新增或修改技能 | [贡献指南](CONTRIBUTING.md) |
| Agent 维护本仓库的约定 | [AGENTS.md](AGENTS.md) |
| 技能文件格式 | [Agent Skills 规范](https://agentskills.io/specification) |
| ponytail-lite 的手动 hook 配置 | [HOOKS.md](skills/ponytail-lite/HOOKS.md) |
| 迁入技能的来源与改动 | 各技能目录下的 `UPSTREAM.md` |

问题和想法请提交到 [GitHub Issues](https://github.com/yakami129/engineering-skills/issues)。

## 许可证

原创内容使用 [MIT 许可证](LICENSE) · Copyright © 2026 yakami129。迁入技能的版权、许可证和版本记录见各自目录中的 `LICENSE` 与 `UPSTREAM.md`。
