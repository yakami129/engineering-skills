# Engineering Skills

把自己反复使用的方法，整理成 AI Agent 可以按需调用的技能。

参考 [Matt Pocock 的 skills 仓库](https://github.com/mattpocock/skills) 的组织方式：一个技能一个目录，先把流程写清楚，再按需补充脚本、参考资料和素材。迁入的第三方技能在各自目录中保留来源、固定版本与许可证。

## 快速开始

```bash
git clone https://github.com/yakami129/engineering-skills.git
cd engineering-skills
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt

python tools/skills.py new my-skill \
  --description "把访谈记录整理成用户需求；用于访谈结束后的需求提炼。"
```

接着编辑 `skills/my-skill/SKILL.md`，替换其中的 `[TODO: ...]`。最后运行：

```bash
python tools/skills.py check
python -m unittest discover -s tests -v
```

建议每次新增技能使用独立分支和 Pull Request。完整步骤见 [贡献指南](CONTRIBUTING.md)。开发工具需要 Python 3.9+；安装技能本身不需要 Python。

## 目录

```text
skills/
  domain-modeling/             共享术语表与 ADR 的维护机制
  grilling/                    设计讨论与追问，供组合入口调用
  grill-with-docs/             讨论过程中同步维护项目文档
  diagnosing-bugs/
    SKILL.md                  Matt 的调试技能，保留上游原文
    agents/openai.yaml        Codex 显示信息
    scripts/                  人工配合复现的 Bash 模板
    LICENSE / UPSTREAM.md     上游许可与版本记录
  meeting-notes/
    SKILL.md                  可直接使用、也可删除的示例
templates/
  SKILL.md.template           不会被安装器当作技能发现的模板
tools/
  skills.py                   新建技能和检查格式
tests/                        工具的行为测试
.github/workflows/check.yml   推送和 PR 自动检查
```

每个技能只需要 `SKILL.md`。当实际工作流需要时，再在该技能下增加 `scripts/`、`references/` 或 `assets/`。脚本放可执行工具，参考资料放按需读取的说明，素材放会进入输出的文件。

## 安装与使用

使用 [skills CLI](https://github.com/vercel-labs/skills)；需要 Node.js，版本要求以安装器当前文档为准。在需要使用技能的项目中运行：

```bash
# 只查看可用技能，不安装
npx skills@latest add yakami129/engineering-skills --list

# 交互选择技能和目标 Agent
npx skills@latest add yakami129/engineering-skills

# 只给当前项目的 Codex 安装调试技能
npx skills@latest add yakami129/engineering-skills --skill diagnosing-bugs -a codex
```

同一安装器也支持 Claude Code、Cursor 等 Agent。需要跨项目使用时，可以自行添加 `-g`；默认保持在当前项目中。复制安装后的技能不会跟随此仓库的每次提交自动同步，可使用 `npx skills@latest check` 和 `npx skills@latest update` 检查和更新。

## 技能目录

| 技能 | 用途 |
| --- | --- |
| [domain-modeling](skills/domain-modeling/SKILL.md) | 在设计讨论中明确项目术语和概念边界，维护 `GLOSSARY.md` 并记录重要 ADR；[来源与版本](skills/domain-modeling/UPSTREAM.md) |
| [grilling](skills/grilling/SKILL.md) | 围绕计划或设计分轮追问，澄清尚未决定的问题；[来源与版本](skills/grilling/UPSTREAM.md) |
| [grill-with-docs](skills/grill-with-docs/SKILL.md) | 手动调用的组合入口：边讨论边维护术语表与 ADR，依赖上面两个技能；[兼容调整与来源](skills/grill-with-docs/UPSTREAM.md) |
| [diagnosing-bugs](skills/diagnosing-bugs/SKILL.md) | Matt Pocock 的疑难故障与性能回归诊断流程：建立反馈循环、复现并最小化、验证假设、修复与回归检查；[来源与版本](skills/diagnosing-bugs/UPSTREAM.md) |
| [meeting-notes](skills/meeting-notes/SKILL.md) | 将会议记录整理成结论、决策、待办和待确认问题；作为写作示例，可直接修改或删除 |

新增技能时，在这里补一行，方便自己查找。技能较多后再考虑分类，不需要提前维护插件清单或发布流水线。

## 项目上下文：CONTEXT.md / GLOSSARY.md

Matt 旧版示例中的 `CONTEXT.md` 是项目共享术语表；当前技能把它命名为 `GLOSSARY.md`。这套机制让开发者和 Agent 对同一概念使用同一个名字，并在讨论中持续维护定义。

| 文件 | 记录什么 | 何时创建 |
| --- | --- | --- |
| `GLOSSARY.md` | 项目特有的术语、定义与应避免的别名 | 第一个术语确定时 |
| `docs/adr/0001-事项.md` | 重要决策及其理由，保留真实的取舍 | 决策难以逆转、缺少上下文会令人意外、且确实比较过替代方案时 |
| `GLOSSARY-MAP.md` | 多个业务上下文的术语表位置及关系 | 项目确实存在多个上下文时 |

在目标项目中安装完整组合：

```bash
npx skills@latest add yakami129/engineering-skills \
  --skill domain-modeling --skill grilling --skill grill-with-docs -a codex
```

然后发起讨论，例如：

> 使用 $grill-with-docs，帮我梳理订单取消与退款的设计；确定术语后及时写入 GLOSSARY.md，重要且有取舍的决定记录为 ADR。

日常只维护术语或决策时，可以直接使用 `$domain-modeling`。`grill-with-docs` 保持手动调用；技能不会自动替你安装它依赖的另外两个技能。

若希望后续任务也按需读取这些文件，可在目标项目的 `AGENTS.md` 中加入读取约定：

```markdown
讨论业务术语或修改领域行为时，先读取 GLOSSARY.md（如果存在）；涉及设计取舍时，读取 docs/adr/ 中的相关决策。术语变化使用 domain-modeling 技能同步维护。
```

已有 `CONTEXT.md` 的项目，应先检查其内容与引用，再决定是否迁移到当前约定。术语表保持精简，实施计划、临时笔记和实现细节各自保存在合适的项目文档中。

## 写一个好用的技能

- `name` 与目录名一致，使用小写字母、数字和连字符。
- `description` 写清楚「做什么、什么时候用」，让 Agent 能判断是否适用。
- 正文写输入、关键步骤和完成标准，保留真正来自你经验的判断方法。
- 较长资料放到 `references/`，并在正文注明何时读取。
- 用一个真实请求试跑后再调整。格式检查只验证结构，无法证明技能效果。

公开提交前检查内容归属，使用虚构或脱敏示例。凭据、客户原始资料和未获准公开的内部流程应保存在合适的私有位置。

格式参考：[Agent Skills 规范](https://agentskills.io/specification)。原创内容使用 [MIT 许可证](LICENSE)；迁入技能的版权、许可证和版本记录见各自目录中的 `LICENSE` 与 `UPSTREAM.md`。
