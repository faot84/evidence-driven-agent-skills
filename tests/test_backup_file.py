"""Exercise the file-backup helper in disposable test directories."""

import hashlib
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(
    0, str(ROOT / "skills" / "verified-backup-before-edit" / "scripts")
)
from backup_file import BackupError, backup_file  # noqa: E402


class BackupFileTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.project = self.base / "project"
        self.store = self.base / "backups"
        self.project.mkdir()
        self.store.mkdir()
        self.source = self.project / "src" / "app.txt"
        self.source.parent.mkdir()
        self.source.write_text("uncommitted user change\n", encoding="utf-8")

    def test_verified_backup_keeps_pre_edit_state(self):
        receipt = backup_file(self.project, self.source, self.store)
        saved = Path(receipt["backup"])
        self.assertEqual(receipt["status"], "verified")
        self.assertEqual(saved.read_bytes(), self.source.read_bytes())
        self.assertEqual(
            receipt["sha256"], hashlib.sha256(saved.read_bytes()).hexdigest()
        )
        self.assertTrue(Path(receipt["receipt"]).is_file())
        self.source.write_text("later edit\n", encoding="utf-8")
        self.assertEqual(saved.read_text(encoding="utf-8"), "uncommitted user change\n")

    def test_second_backup_does_not_replace_first(self):
        first = backup_file(self.project, self.source, self.store)
        self.source.write_text("version two\n", encoding="utf-8")
        second = backup_file(self.project, self.source, self.store)
        self.assertNotEqual(first["backup"], second["backup"])
        self.assertEqual(
            Path(first["backup"]).read_text(encoding="utf-8"),
            "uncommitted user change\n",
        )
        self.assertEqual(
            Path(second["backup"]).read_text(encoding="utf-8"), "version two\n"
        )

    def test_rejects_backup_destination_inside_project(self):
        nested_store = self.project / "backups"
        nested_store.mkdir()
        with self.assertRaises(BackupError):
            backup_file(self.project, self.source, nested_store)
        self.assertEqual(list(nested_store.iterdir()), [])

    def test_rejects_obvious_secret_without_copying(self):
        secret = self.project / ".env"
        secret.write_text("example only\n", encoding="utf-8")
        with self.assertRaises(BackupError):
            backup_file(self.project, secret, self.store)
        self.assertEqual(list(self.store.iterdir()), [])

    def test_rejects_source_outside_project(self):
        outside = self.base / "outside.txt"
        outside.write_text("outside\n", encoding="utf-8")
        with self.assertRaises(BackupError):
            backup_file(self.project, outside, self.store)
        self.assertEqual(list(self.store.iterdir()), [])

    def test_missing_store_fails_before_copy(self):
        with self.assertRaises(FileNotFoundError):
            backup_file(self.project, self.source, self.base / "missing")
        self.assertEqual(self.source.read_text(encoding="utf-8"), "uncommitted user change\n")


if __name__ == "__main__":
    unittest.main()
