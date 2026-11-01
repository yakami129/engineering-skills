# 技能库维护

技能位于 `skills/<name>/SKILL.md`。新增流程见 [CONTRIBUTING.md](CONTRIBUTING.md)，使用 `python tools/skills.py new` 生成骨架。

描述注明能力与触发场景，正文保留任务特有的判断和完成标准。支持文件按实际需要创建，并从入口说明何时读取。保持每项技能可独立安装。

模板保存在 `templates/SKILL.md.template`，发布的技能中应完成所有 `[TODO: ...]`。新增技能同步 README 目录。公开内容仅包含用户明确指定的资料或本仓库新建内容，示例使用虚构或脱敏数据。

修改在工作分支提交 PR。提交前运行：

```bash
python tools/skills.py check
python -m unittest discover -s tests -v
```

修改技能流程还需用一个代表性请求验证效果；增加脚本时实际运行验证。格式检查成功只代表结构有效。
