import shutil
import tempfile
import unittest
from pathlib import Path

from tools.skills import ROOT, check_repository, create_skill


class SkillsTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "templates").mkdir()
        (self.root / "skills").mkdir()
        shutil.copy(ROOT / "templates/SKILL.md.template", self.root / "templates")

    def write_skill(self, content, name="demo"):
        directory = self.root / "skills" / name
        directory.mkdir()
        (directory / "SKILL.md").write_text(content, encoding="utf-8")

    def test_generated_skill_round_trip_with_yaml_sensitive_description(self):
        directory = create_skill(self.root, "demo", '整理记录: 含 "引号"\n第二行')
        errors, count = check_repository(self.root)
        self.assertEqual(count, 1)
        self.assertIn("TODO", errors[0])
        skill = directory / "SKILL.md"
        lines = skill.read_text(encoding="utf-8").splitlines()
        skill.write_text("\n".join(line for line in lines if "[TODO:" not in line), encoding="utf-8")
        self.assertEqual(check_repository(self.root), ([], 1))

    def test_existing_skill_is_never_overwritten(self):
        directory = create_skill(self.root, "demo", "整理记录")
        before = (directory / "SKILL.md").read_bytes()
        with self.assertRaises(FileExistsError):
            create_skill(self.root, "demo", "覆盖描述")
        self.assertEqual((directory / "SKILL.md").read_bytes(), before)

    def test_yaml_like_names_remain_strings(self):
        for name in ("123", "on", "yes", "null"):
            with self.subTest(name=name):
                directory = create_skill(self.root, name, "整理记录")
                skill = directory / "SKILL.md"
                content = skill.read_text(encoding="utf-8")
                frontmatter = content.partition("\n---\n")[0]
                skill.write_text(frontmatter + "\n---\n\n整理记录。", encoding="utf-8")
        self.assertEqual(check_repository(self.root), ([], 4))

    def test_invalid_names_cannot_escape_skills_directory(self):
        for name in ("../escape", "/tmp/escape", "UPPER", "two--dashes", "-name", "a" * 65):
            with self.subTest(name=name), self.assertRaises(ValueError):
                create_skill(self.root, name, "整理记录")
        self.assertEqual(list((self.root / "skills").iterdir()), [])

    def test_invalid_frontmatter_and_unfinished_skills_are_reported(self):
        cases = (
            "# 没有 frontmatter",
            "---\n- demo\n---\n正文",
            "---\nname: [\n---\n正文",
            "---\nname: other\ndescription: 描述\n---\n正文",
            "---\nname: demo\ndescription: ' '\n---\n正文",
            "---\nname: demo\ndescription: 123\n---\n正文",
            "---\nname: demo\ndescription: 描述\n---\n",
            "---\nname: demo\ndescription: 描述\n---\n[TODO: 完善流程]",
        )
        for content in cases:
            with self.subTest(content=content):
                self.write_skill(content)
                self.assertTrue(check_repository(self.root)[0])
                shutil.rmtree(self.root / "skills/demo")

    def test_missing_entrypoint_is_reported(self):
        (self.root / "skills/demo").mkdir()
        errors, count = check_repository(self.root)
        self.assertEqual(count, 1)
        self.assertIn("SKILL.md", errors[0])

    def test_empty_catalog_is_valid(self):
        self.assertEqual(check_repository(self.root), ([], 0))


if __name__ == "__main__":
    unittest.main()
