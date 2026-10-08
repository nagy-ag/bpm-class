"""Regression: updating one shared heading must not overwrite the following task."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from harness.cli import ROOT


class LegacyTrackerTests(unittest.TestCase):
    def test_targeted_update_preserves_next_task_and_prior_evidence(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'TASK_PROGRESS.md'
            before = '''# Tasks

### first-01 — First

Status: `in_progress` · Owner: `current automation chat` · Updated: 2026-01-01 · Next step: 2

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read | done | unique-prior-evidence |
| 2 | Verify | in_progress | claimed |

### second-01 — Second

Status: `done` · Owner: `unassigned` · Updated: 2026-01-01 · Next step: None

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read | done | second-read-evidence |
| 2 | Verify | done | second-verify-evidence |
'''
            path.write_text(before, encoding='utf-8')
            result = subprocess.run([sys.executable, str(ROOT / 'nap03/working/task_update.py'), str(path),
                                     'first-01', '2', 'done', 'actual-first-result'], capture_output=True)
            self.assertEqual(result.returncode, 0)
            after = path.read_text(encoding='utf-8')
            self.assertEqual(before.split('### second-01')[1], after.split('### second-01')[1])
            self.assertIn('| 1 | Read | done | unique-prior-evidence |', after)
            self.assertIn('| 2 | Verify | done | actual-first-result |', after)


if __name__ == '__main__':
    unittest.main()
