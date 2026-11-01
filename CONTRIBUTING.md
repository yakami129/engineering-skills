# 添加或修改技能

## 新增

1. 按 README 准备 Python 环境，从 `main` 创建工作分支：

   ```bash
   git switch -c codex/add-my-skill
   python tools/skills.py new my-skill --description "说明技能能力和适用场景。"
   ```

2. 编辑生成的 `skills/my-skill/SKILL.md`，用实际流程替换 `[TODO: ...]`。命令不会覆盖已有目录。
3. 只有需要时才添加 `scripts/`、`references/` 或 `assets/`，在正文中链接需要读取的资料。
4. 在 README 的技能目录补一行。用一个真实请求试跑，确认输入、判断和输出符合预期；新增可执行脚本还需实际运行验证。
5. 执行检查，提交分支并创建 Pull Request：

   ```bash
   python tools/skills.py check
   python -m unittest discover -s tests -v
   git add skills/my-skill README.md
   git commit -m "feat: add my-skill"
   git push -u origin codex/add-my-skill
   gh pr create --fill
   ```

PR 说明适用场景、一个调用示例和试跑结果。CI 会检查所有已提交技能的格式以及脚手架工具的测试。

## 维护约定

- `skills/` 下每个直属目录就是一个技能，名称不超过 64 个字符。
- `SKILL.md` 的 YAML 头部必须包含非空字符串 `name`、`description`，正文必须有可执行的指导。
- 模板中的 `[TODO: ...]` 必须替换完成；校验会拒绝未完成的模板。
- 参考资料保留在所属技能目录内，便于单独安装和移动。
- 示例 `meeting-notes` 可以修改或删除；一个尚未添加技能的空库也允许通过检查。
- 修改已有技能时，优先用真实失败案例验证修正，而不是不断累加通用规则。
