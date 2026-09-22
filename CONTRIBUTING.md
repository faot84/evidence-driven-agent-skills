# Contributing

Improvements are welcome when they make a skill clearer, more general, or better supported by a reproducible example.

## Before opening a pull request

1. Keep each skill self-contained in `skills/<name>/SKILL.md`, with `name` matching the directory and a `description` that says when to use it and when not to.
2. Add any new skill or agent to `SKILLS` or `AGENTS` in `scripts/validate.py`.
3. Do not include credentials, private project content, personal paths, names of real private individuals, or internal incident details. Describe failures generally.
4. Run the three commands in the README's "Validate this package" section. All must pass.
5. If you change agent-facing behavior, say how you checked it. A manual run of an example counts; state the assistant, the prompt, and what happened. Do not present a single run as proof that every agent follows the skill.

## Style

Write short, direct instructions. Say what to do, why it matters, and where the skill stops. Prefer a concrete failure pattern over general advice.

By contributing, you agree that your contribution is licensed under the [MIT License](LICENSE).
