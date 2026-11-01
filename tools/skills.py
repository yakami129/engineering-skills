#!/usr/bin/env python3
"""Create and validate the flat skills catalog in this repository."""

import argparse
import json
import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def validate_name(name):
    if not isinstance(name, str) or not NAME.fullmatch(name) or len(name) > 64:
        raise ValueError("名称须为 1–64 位小写字母、数字或单个连字符，且首尾不能是连字符")


def validate_description(description):
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        raise ValueError("description 须为 1–1024 字符的非空字符串")


def create_skill(root, name, description):
    validate_name(name)
    validate_description(description)
    template = (root / "templates/SKILL.md.template").read_text(encoding="utf-8")
    content = template.replace("{{name}}", name).replace(
        "{{description}}", json.dumps(description, ensure_ascii=False)
    )
    destination = root / "skills" / name
    destination.mkdir(parents=True, exist_ok=False)
    (destination / "SKILL.md").write_text(content, encoding="utf-8")
    return destination


def check_skill(directory):
    validate_name(directory.name)
    content = (directory / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", content, re.DOTALL)
    if not match:
        raise ValueError("SKILL.md 须以 YAML frontmatter 开头")
    metadata = yaml.safe_load(match.group(1))
    if not isinstance(metadata, dict):
        raise ValueError("YAML frontmatter 须为键值映射")
    validate_name(metadata.get("name"))
    if metadata["name"] != directory.name:
        raise ValueError("name 须与技能目录名一致")
    validate_description(metadata.get("description"))
    if not content[match.end():].strip():
        raise ValueError("技能正文不能为空")
    if "[TODO:" in content:
        raise ValueError("请完成模板中的 [TODO: ...] 后再提交")


def check_repository(root):
    skills = root / "skills"
    if not skills.is_dir():
        return ["缺少 skills/ 目录"], 0
    directories = sorted(path for path in skills.iterdir() if path.is_dir())
    errors = []
    for directory in directories:
        try:
            check_skill(directory)
        except (OSError, ValueError, yaml.YAMLError) as error:
            errors.append(f"{directory.relative_to(root)}: {error}")
    return errors, len(directories)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    new = commands.add_parser("new", help="生成一个待完善的技能，不覆盖已有目录")
    new.add_argument("name")
    new.add_argument("--description", required=True)
    commands.add_parser("check", help="检查 skills/ 下所有技能")
    arguments = parser.parse_args()
    if arguments.command == "new":
        try:
            destination = create_skill(ROOT, arguments.name, arguments.description)
        except (OSError, ValueError) as error:
            parser.exit(1, f"无法创建技能：{error}\n")
        print(f"已创建 {destination.relative_to(ROOT)}/SKILL.md，请完成其中的 TODO。")
        return
    errors, count = check_repository(ROOT)
    if errors:
        parser.exit(1, "\n".join(errors) + "\n")
    print(f"检查通过：{count} 个技能。")


if __name__ == "__main__":
    main()
