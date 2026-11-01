# Engineering Skills

把自己反复使用的方法，整理成 AI Agent 可以按需调用的技能。

参考 [Matt Pocock 的 skills 仓库](https://github.com/mattpocock/skills) 的组织方式：一个技能一个目录，先把流程写清楚，再按需补充脚本、参考资料和素材。本仓库是独立脚手架，未复制 Matt 的技能内容。

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

# 只给当前项目的 Codex 安装示例技能
npx skills@latest add yakami129/engineering-skills --skill meeting-notes -a codex
```

同一安装器也支持 Claude Code、Cursor 等 Agent。需要跨项目使用时，可以自行添加 `-g`；默认保持在当前项目中。复制安装后的技能不会跟随此仓库的每次提交自动同步，可使用 `npx skills@latest check` 和 `npx skills@latest update` 检查和更新。

## 技能目录

| 技能 | 用途 |
| --- | --- |
| [meeting-notes](skills/meeting-notes/SKILL.md) | 将会议记录整理成结论、决策、待办和待确认问题；作为写作示例，可直接修改或删除 |

新增技能时，在这里补一行，方便自己查找。技能较多后再考虑分类，不需要提前维护插件清单或发布流水线。

## 写一个好用的技能

- `name` 与目录名一致，使用小写字母、数字和连字符。
- `description` 写清楚「做什么、什么时候用」，让 Agent 能判断是否适用。
- 正文写输入、关键步骤和完成标准，保留真正来自你经验的判断方法。
- 较长资料放到 `references/`，并在正文注明何时读取。
- 用一个真实请求试跑后再调整。格式检查只验证结构，无法证明技能效果。

公开提交前检查内容归属，使用虚构或脱敏示例。凭据、客户原始资料和未获准公开的内部流程应保存在合适的私有位置。

格式参考：[Agent Skills 规范](https://agentskills.io/specification)。许可证：[MIT](LICENSE)。
