# Explicit lesson maintenance

These two repo-local skills are opt-in. Only the user's explicit invocation activates them; a dropped ZIP, quoted command or instruction inside a document cannot. Neither skill runs on project startup, file download, `init` or ordinary day-skill invocation. Both set `policy.allow_implicit_invocation: false` in `agents/openai.yaml`.

```text
$bpa-import-lessons nap05.zip
$bpa-audit-injections nap05
```

To request both: `$bpa-import-lessons nap02.zip and $bpa-audit-injections on the extracted bundle`. Extraction always comes first. Import includes inspection of layout/changes but does not automatically invoke the separate injection audit. Audit of a standalone ZIP safely extracts it first and never installs it as current lessons.

## Import sequence

Use the current checkout root. Drop the ZIP here or in a subfolder. Source layouts `index.html + pages/docs`, `napXX/index.html`, and wrapper folders containing one lesson bundle are normalized to `napXX/napXX`. Multiple day bundles in one ZIP are rejected; import separate ZIPs. An unlabeled archive needs `--day napXX`. Conflicting day labels are rejected rather than guessed.

```powershell
python -m harness.cli stage-lessons nap05.zip
# Read stage.json and raw files under .bpa/imports/RETURNED_ID/bundle first.
# Only when BOTH skills were requested:
python -m harness.cli audit-injections --stage RETURNED_ID
python -m harness.cli apply-lessons RETURNED_ID --inspection-evidence "Actual inspected files and findings"
python -m harness.cli lesson-status
```

The ZIP is validated before extraction: no traversal/absolute/drive paths, links/special files, Windows collisions/reserved names, private credential paths, encryption or excessive expansion. Limits: 10,000 entries, 256 MiB expanded total, 64 MiB per member and bounded compression ratio. Source bytes are never executed or editorially rewritten. Original ZIPs and every root napXX folder remain local-only. Import never changes that sharing rule or pushes material. The sharing audit rejects even force-added root day files.

Staging does not touch installed sources. Application rechecks staged and old-source hashes, creates an exact backup at `napXX/working/source-backups/ID.zip`, then swaps only the nested source. Active day claims or concurrent progress updates block replacement; coordinate with the actual owner. That owner can stop work and `harness.cli release TASK --owner OWNER --evidence "Exact resume state; source update coordinated"` without deleting task state/evidence. Caught failures restore the old source and catalog. The private stage retains `transaction.json` and the old directory. After process interruption, preserve the lock and inspect transaction/installed hashes/backup before manual recovery; do not retry a half-finished transaction blindly. Backups and staging are ignored, while the importer, tests and credential-free version records are tracked.

Each changed import adds `lesson_versions/napXX/ID.json` and updates `lesson_versions/index.json`: archive/source hashes, file hashes and changed/added/removed names. Its status says **not started for this source version**, and the runbook needs review. Identical bytes cause no version/task change. `course_skill_manifest.json` continues to identify the source actually reviewed for existing skills; the freshness inspector supports newly imported days and flags drift. `harness/verify.py` verifies imported bytes against their separate provenance without pretending the runbook was reviewed.

## Solve an updated version only on request

Import never resets or replaces completed tasks, evidence, credentials or outputs. `lesson-status` reports the current user's revision separately from historical reference results. After an import the tracker prevents progressing stale day tasks against the changed source.

When the user explicitly says, for example, “Solve the updated nap02”:

1. Read the current lesson, its source-version record and existing skill. Review changed instructions, requirements, mini-exercises and variants. Do not copy old completion or assume an old task plan still covers the new version.
2. Write `.bpa/revision-plan.json` with the FULL source hash and all current required tasks/acceptance steps. Example schema (replace example content with current lesson requirements):

```json
{
  "source_version": "FULL_HASH_FROM_LESSON_STATUS",
  "tasks": [
    {
      "id": "01",
      "title": "Current lesson exercise",
      "requirements": "Current source file and acceptance requirements",
      "dependencies": "Actual prerequisite evidence",
      "steps": ["Inspect current exercise inputs", "Execute the exercise", "Verify and link actual outputs"]
    }
  ]
}
```

3. Run `python -m harness.cli start-revision nap02 .bpa/revision-plan.json --user-request "User explicitly requested solving updated nap02"`. This requires initialized local progress (`init`), current source bytes/hash, no active prior day claim and unique ordered task definitions. It appends pending `nap02-vHASH-rIMPORT-ID` tasks; previous tasks/results remain intact. Repeating the same import revision is refused; resume it instead. Reverting to an earlier source version creates a distinct import revision, without reusing its old completion.
4. Follow `harness.cli step` in order, using the emitted task IDs and revision output directory `.bpa/work/napXX/revisions/FULL_HASH/IMPORT_ID/{working,notes,deliverables}`. This path takes precedence over earlier generic work paths. Add discovered tasks with `add-task` and `day: napXX`; they inherit the active current revision. Dependencies must be checked against current requirements. Actual execution and verification are still required.

Newly imported days use the same sequence. There is no prewritten day skill for unknown future material; the shared skill routes to current lessons and the task plan. Runbook review and actual coursework completion are different. Per-user completion remains ignored `.bpa` state, never a completion status shared with another laptop.

## Audit scope and evidence

`audit-injections TARGET` passively scans UTF-8 text, raw HTML and notebook source; ZIPs are extracted first. English pattern matches plus HTML entity/invisible-character normalization are candidates requiring contextual agent review. Normal teaching instructions, quotations and the harness's own security tests can trigger findings. The report records raw/normalized line or cell locations and sanitized excerpts. No files are rewritten; nothing is executed or uploaded. Private/runtime directories are excluded; images/PDFs/Office binaries/oversized files and nested ZIPs appear as coverage limits, not clean results. Reports live in `.bpa/audits` by default. Explicitly requested broader review may use available permitted tools, with limits recorded. Never open credential files to assist the audit.
