---
name: non-destructive-autonomy
description: Complete authorized local implementation tasks autonomously while preserving existing files and verifying a backup before each edit. Use when the user wants work finished without repeated routine approvals and forbids deletion; do not use for read-only reviews.
---

# Non-destructive autonomy

Finish the user's authorized local task without asking again about routine implementation choices. Autonomy changes the pace of work, not its scope or permissions.

## Before changing anything

- Read applicable project instructions and inspect the exact target files, current changes, and affected consumers.
- Choose the smallest implementation that satisfies the request. Preserve unrelated work, including uncommitted changes from the user or other agents.
- For each existing file that may be edited or overwritten, make and verify a recoverable backup of its current state before the first write. Apply the procedure in the companion verified-backup-before-edit skill if installed. Otherwise copy to a trusted location outside the project and verify equal size and SHA-256. Stop on backup failure. A new file has no prior version.
- Treat secret-bearing files as protected data. If a safe backup cannot be made, stop that part of the task instead of copying secrets to an unsafe destination.

## While working

- Do not delete, trash, prune, move, rename, or replace an existing file or directory as a way to remove its old path. Avoid commands and tools with hidden cleanup or destructive effects, including Git clean/reset and sync options that delete destination files.
- Editing an in-scope file is allowed only after its backup is verified. Do not overwrite an unrelated file or discard someone else's changes.
- If the requested result genuinely requires removal or a move, complete independent safe parts and explain the exact conflict. Do not silently leave a broken substitute or reinterpret this workflow as permission to delete.
- Do not publish, deploy, send data externally, or broaden access unless the task already authorizes it.

## Before reporting completion

Run checks that could reveal a failure in the changed behavior. Confirm the relevant files still exist, the intended change is present, and the backup receipts cover every edited pre-existing file. Report changed files, checks and observed results, backup locations, and any part left blocked. Do not call the task complete when an essential requirement remains unfulfilled.

This workflow describes agent behavior. A skill alone is not an operating-system control. Users who need enforced tool restrictions can add product-specific permissions or hooks without weakening the backup and no-deletion rules.
