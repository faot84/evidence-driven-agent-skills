---
name: verified-backup-before-edit
description: Create and verify a recoverable backup before editing an existing local file in an authorized task. Use for code, documents, configuration, or generated output that may be overwritten; do not use for read-only work.
---

# Verified backup before edit

Preserve the state actually found immediately before the first authorized change to each existing file. An uncommitted edit is part of that state. A Git commit or an editor undo history is not a substitute for this backup.

1. Identify the exact existing files that the task or a tool may change. Record newly created files as having no previous version. Do not back up unrelated files merely because they are nearby.
2. Choose a trusted backup directory outside the project. Prefer separate storage. Check access and capacity before changing the source. Never silently switch to a different destination.
3. Classify sensitive content before copying. Keep credentials, private keys, and other secrets in a protected backup location that retains their access controls. If that cannot be arranged, stop before editing that file. Do not put secrets or their contents in a public repository or report.
4. For ordinary files, run the bundled script with the project root, exact source file, and chosen backup root. SKILL_DIR is the directory containing this SKILL.md. Relative paths are resolved from the current directory, and the backup root must already exist:

       python SKILL_DIR/scripts/backup_file.py --project-root PROJECT --source FILE --backup-root BACKUP_ROOT

   It creates a new, non-overwriting backup, compares size and SHA-256 against the source before and after copying, and writes a JSON receipt. If it fails, do not edit the file. The filename filter is only a guard against obvious secrets; it cannot classify every sensitive file. On Windows, the restrictive directory mode is ignored; the backup inherits the permissions of the backup root.
5. If the script is unavailable, use an equivalent copy and verify the source and backup by size and SHA-256 before the first edit. Record the path and result. Never claim a backup was verified from a copy command alone.
6. For a directory operation, inventory and verify each material existing file. For a live database or service state, use its consistent backup mechanism and a suitable restore check; an ordinary file copy is insufficient.

Keep previous backups. A backup does not authorize deletion, moving files, or edits beyond the original request. Report the backup location and verification result without disclosing protected contents. If a file was already changed before the backup, say which state was actually preserved.
