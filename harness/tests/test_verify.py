"""Public provenance and private bundles have separate verification outcomes."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from harness.verify import source_checks


class SourceVerificationTests(unittest.TestCase):
    def test_missing_imported_bundle_is_unavailable_not_corrupt(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'course_skill_manifest.json').write_text('{"days": {}}')
            (root / 'lesson_versions').mkdir()
            (root / 'lesson_versions/index.json').write_text(json.dumps({'days': {
                'nap07': {'record': 'lesson_versions/nap07/version.json', 'runbook_review': 'required'}}}))
            checks, unavailable = source_checks(root)
            self.assertEqual(checks, [])
            self.assertEqual(unavailable, ['nap07'])

    def test_installed_imported_bytes_are_still_verified(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'course_skill_manifest.json').write_text('{"days": {}}')
            (root / 'lesson_versions').mkdir()
            (root / 'lesson_versions/index.json').write_text(json.dumps({'days': {
                'nap07': {'record': 'lesson_versions/version.json', 'runbook_review': 'required'}}}))
            (root / 'lesson_versions/version.json').write_text(json.dumps({'files': {
                'index.html': hashlib.sha256(b'expected lesson').hexdigest()}}))
            bundle = root / 'nap07/nap07'
            bundle.mkdir(parents=True)
            (bundle / 'index.html').write_bytes(b'expected lesson')
            checks, unavailable = source_checks(root)
            self.assertTrue(checks[0]['passed'])
            self.assertEqual(unavailable, [])
            (bundle / 'index.html').write_bytes(b'changed bytes')
            checks, unavailable = source_checks(root)
            self.assertFalse(checks[0]['passed'])
            self.assertEqual(unavailable, [])
