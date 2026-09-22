<div align="center">
  <img src="assets/evidence-driven-agent-skills.svg" alt="Evidence-driven agent skills icon" width="180" />

  <h1>Evidence-driven agent skills</h1>

  <p><strong>Reusable workflows for auditing, debugging, verification, safe delegation, and non-destructive AI-assisted software work.</strong></p>

  <p>
    <a href="https://github.com/faot84/evidence-driven-agent-skills/actions/workflows/validate.yml"><img alt="validate" src="https://github.com/faot84/evidence-driven-agent-skills/actions/workflows/validate.yml/badge.svg"></a>
    <img alt="9 skills" src="https://img.shields.io/badge/skills-9-0ea5a5">
    <img alt="Python 3.9+" src="https://img.shields.io/badge/Python-3.9%2B-3776AB">
    <a href="LICENSE"><img alt="MIT license" src="https://img.shields.io/badge/license-MIT-2563eb"></a>
  </p>
</div>

Nine reusable agent skills and one optional subagent for examining a software delivery, making an evidence-based acceptance decision, finding the real cause of a failure, reporting only what was checked, delegating work safely, and carrying out an authorized change without discarding existing work. They are generalized from internal workflows into standalone instructions that do not require a named team, a particular repository layout, or private memory.

| Skill | Use it when | Result |
| --- | --- | --- |
| [audit-delivery](skills/audit-delivery/SKILL.md) | You need to investigate whether claims, requirements, code, tests, and evidence agree. | Findings, their evidence, and the limits of the review. |
| [certify-delivery](skills/certify-delivery/SKILL.md) | You have a specific version and predefined acceptance criteria, and need a release decision. | One verdict with a status for every mandatory criterion. |
| [verified-backup-before-edit](skills/verified-backup-before-edit/SKILL.md) | An authorized task may change an existing local file. | A verified copy of its pre-edit state and a receipt. |
| [non-destructive-autonomy](skills/non-destructive-autonomy/SKILL.md) | The user wants an authorized local change completed with routine autonomy and no deletion. | A bounded change, checks, and verified backups of edited existing files. |
| [reproduce-before-fixing](skills/reproduce-before-fixing/SKILL.md) | Something fails and the cause is not yet known. | A reproduction, a confirmed cause, a fix, and a negative control. |
| [claim-evidence-table](skills/claim-evidence-table/SKILL.md) | You are about to report that something works, is fixed, or is the cause. | A table of claims with status, literal evidence, and how each check could be wrong. |
| [test-tenant-isolation](skills/test-tenant-isolation/SKILL.md) | Several customers share one database and one must never reach another's data. | A rerunnable set of checks executed as each role, with real or emulated scope stated. |
| [brief-a-subagent](skills/brief-a-subagent/SKILL.md) | You are delegating substantial work to another agent. | A brief with verified inputs, a destination file, limits, and a stopping condition. |
| [stop-repeating-rounds](skills/stop-repeating-rounds/SKILL.md) | A fix-and-review cycle is about to start its second round. | A decision to continue, measure, or stop and rethink with the user. |

The optional [adversarial-reviewer](agents/adversarial-reviewer.md) subagent attacks finished work before delivery and reports only defects, with a one-line verdict.

The audit explores an open question. Certification decides whether a defined delivery satisfies fixed criteria. These two review workflows are read-only by default, and the adversarial reviewer is instructed to change nothing except its single report file, although running checks can create caches. The backup and non-destructive workflows apply only when the user has authorized a local change. test-tenant-isolation runs queries, so use it against a disposable or authorized environment. None of the skills grants permission to deploy, publish, access secrets, or expand the task.

## Try the example

The [synthetic calculator delivery](examples/calculator/README.md) contains requirements, implementation, a small test suite, and a claim that the tests prove acceptance. The tests pass, but one mandatory behavior is wrong. Start with:

> Use the audit-delivery skill to review examples/calculator against its requirements and evidence. Report what is demonstrated, contradicted, and still unknown.

Then try:

> Use the certify-delivery skill to decide whether the calculator delivery meets every mandatory criterion in examples/calculator/requirements.md.

Compare your result with the [expected analysis](examples/calculator/expected-analysis.md). This example is illustrative; it is not a benchmark of model performance.

The [safe change exercise](examples/safe-change/README.md) gives an assistant a small bug to fix while preserving an unrelated file and making a verified backup first. Its focused test deliberately fails in the untouched fixture. The [misleading error exercise](examples/misleading-error/README.md) crashes with an error that points away from its cause; a symptom fix makes the crash disappear and the test still fails. The [backup helper tests](tests/test_backup_file.py) check file-copy invariants independently of any agent's decisions.

## Install

Each skill is a self-contained directory with a SKILL.md file. Copy the desired directory from skills/ into one of the locations below, then invoke it by name or describe a matching task. To use the optional subagent in Claude Code, copy agents/adversarial-reviewer.md into ~/.claude/agents/ or .claude/agents/. Codex configures agents differently; there, use the file as a role prompt.

| Product | User scope | Project scope |
| --- | --- | --- |
| Codex | ~/.agents/skills/ | .agents/skills/ |
| Claude Code | ~/.claude/skills/ | .claude/skills/ |

For example, copy the desired skill directories into that project's skill directory. Install verified-backup-before-edit alongside non-destructive-autonomy for the bundled script and full backup procedure; non-destructive-autonomy also states the minimum backup invariant when used alone. The content follows the common Agent Skills format. See the [Codex skill guide](https://learn.chatgpt.com/docs/build-skills) and [Claude Code skill guide](https://code.claude.com/docs/en/skills) for current discovery rules.

No subagents are required. [Agent recommendations](docs/agents.md) explain when specialized reviewers or testers materially improve confidence and show the boundaries they should follow.

## Validate this package

The code targets Python 3.9 or newer, and CI checks 3.10 and 3.13; no external packages are needed:

~~~text
python -B scripts/validate.py
python -B -m unittest discover -s examples/calculator -p "test_*.py" -v
python -B -m unittest discover -s tests -p "test_*.py" -v
~~~

All three commands should pass. Passing calculator tests are part of that example's misleading evidence and do not establish acceptance. Run the safe-change and misleading-error fixtures separately to see their intentional failing baselines before an agent fixes them.

## Scope and limitations

- These are instructions for an AI assistant, not a guarantee of correctness or a substitute for human review.
- Read-only review may leave some behavior unverified. A dynamic test can be proposed or run only when the task and environment permit it.
- The backup helper handles ordinary files. Live databases require a consistent backup method. A filename filter cannot identify all secrets, and a backup on the same disk does not protect against disk loss.
- The no-deletion workflow is an instruction, not a tool-level prohibition. Product-specific permissions or hooks can add enforcement. The automated tests verify the backup helper, not universal agent compliance.
- test-tenant-isolation contains PostgreSQL examples; the questions apply elsewhere, but the commands must be adapted. An emulated database tests policies, not authentication, storage, or the HTTP layer.
- The sample data is fictional. Do not put credentials, private project content, or personal memory in a public issue or pull request.

## Resumen en español

El paquete separa varios trabajos: **auditar** una entrega, **certificar** una versión contra criterios definidos, **respaldar y verificar** un archivo antes de editarlo, **completar cambios autorizados sin borrar**, **encontrar la causa** de un fallo antes de arreglarlo, **declarar con evidencia** cada afirmación, **probar el aislamiento** entre clientes de una misma base de datos, **encargar trabajo** a otro agente sin perderlo y **parar** cuando otra ronda sería más de lo mismo. Incluye además un revisor adversarial opcional. Incluye un caso donde unas pruebas pasan aunque falta un requisito, otro donde el agente debe arreglar un fallo conservando un archivo ajeno, y otro donde el mensaje de error señala el lugar equivocado. Las skills funcionan sin agentes adicionales; la [guía](docs/agents.md) recomienda especialistas sólo cuando aportan evidencia nueva.

## Origin and license

These public skills are generalized adaptations of private Spanish workflows for auditing, certification, implementation, pre-edit backup, debugging, evidence reporting, tenant-isolation testing, delegation, stopping repeated review rounds, and adversarial review. Private incident details were replaced with general descriptions. The original files are not included. This repository is licensed under [MIT](LICENSE).

Related public work addresses parts of the same problem: [files-buddy](https://github.com/wyattowalsh/agents/blob/main/skills/files-buddy/SKILL.md) restricts destructive file operations, [cursor-memory-curator](https://github.com/stark-ai-de/agent-skills/blob/main/skills/cursor-operations/cursor-memory-curator/SKILL.md) records verified backups for its domain, and [agent-skills-sync](https://github.com/marcolinoffls/agent-skills-sync) uses ownership and recovery controls for skill synchronization. Some checks in claim-evidence-table, test-tenant-isolation, and brief-a-subagent were adapted after reading the MIT-licensed [agency-agents](https://github.com/msitarzewski/agency-agents) collection. This package offers general-purpose task workflows and a small reproducible backup helper; it does not claim the underlying ideas are unique.

See [publishing notes](PUBLISHING.md) for proposed GitHub metadata and the final owner review, [CONTRIBUTING](CONTRIBUTING.md) for changes, and [SECURITY](SECURITY.md) for reporting a vulnerability.
