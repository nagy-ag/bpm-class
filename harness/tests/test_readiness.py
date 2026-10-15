"""An uncertain fictional CRM write must retain its checkpoint before any retry."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from harness.course_tools.readiness_updated import live


class ReadinessTests(unittest.TestCase):
    def test_existing_crm_checkpoint_stops_before_any_service_access(self):
        with tempfile.TemporaryDirectory() as temporary:
            out = Path(temporary)
            checkpoint = out / 'crm.json'
            checkpoint.write_bytes(b'{"cleanup":"write_attempted_reconcile_if_unknown"}')
            before = checkpoint.read_bytes()
            with patch('harness.course_tools.day03.bpa_access.CourseAPI') as client:
                with self.assertRaises(FileExistsError):
                    live(out)
                client.assert_not_called()
            self.assertEqual(checkpoint.read_bytes(), before)
