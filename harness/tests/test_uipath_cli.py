"""Project context and truthful CLI verdicts, without running a robot in tests."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from harness.course_tools.uipath_cli import envelope, execute, successful


class UiPathCliTests(unittest.TestCase):
    def test_logs_before_json_do_not_hide_the_run_verdict(self):
        raw = '[Information] literal {text}\n'+json.dumps({'Result':'Success','Data':{'hasErrors':False}})
        self.assertTrue(successful('run', envelope(raw)))

    def test_zero_exit_outer_success_is_not_a_runtime_pass(self):
        for data in ({'hasErrors':True,'errorMessage':'failed'},
                     {'hasErrors':False,'debugState':'Suspended'},
                     {'errors':[],'output':'Failed to open the file x.xaml'},
                     {'message':'Something unknown'}):
            with self.subTest(data=data):
                self.assertFalse(successful('run', {'Result':'Success','Data':data}))
        self.assertTrue(successful('run', {'Result':'Success','Data':{'errors':[],'output':'Session ended'}}))

    def test_build_and_validate_require_their_actual_success_payloads(self):
        self.assertFalse(successful('build', {'Result':'Success','Data':{'Success':False}}))
        self.assertFalse(successful('validate', {'Result':'Success','Data':{'diagnostics':['error']}}))
        self.assertTrue(successful('build', {'Result':'Success','Data':{'Success':True}}))
        self.assertTrue(successful('validate', {'Result':'Success','Data':{'message':'No diagnostics found.'}}))

    def test_project_spaces_literal_metacharacters_and_no_retry_on_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)/'project with spaces & literal'
            project.mkdir()
            (project/'project.json').write_text('{}')
            (project/'Main.xaml').write_text('<Activity/>')
            response = json.dumps({'Result':'Failure','Message':'workflow failed'})
            with patch('harness.course_tools.uipath_cli.official_cli', return_value=['node','official.js']), \
                 patch('harness.course_tools.uipath_cli.subprocess.run', return_value=subprocess.CompletedProcess([],0,response.encode(),b'')) as process:
                _, record = execute('run', project, 'Main.xaml', Path(temp)/'evidence')
                self.assertFalse(record['success'])
                process.assert_called_once()
                args, kwargs = process.call_args
                self.assertEqual(kwargs['cwd'], project.resolve())
                self.assertIs(kwargs['shell'], False)
                self.assertEqual(args[0][args[0].index('--project-dir')+1], str(project.resolve()))
                self.assertEqual(args[0][args[0].index('--file-path')+1], str((project/'Main.xaml').resolve()))
                with self.assertRaises(FileExistsError):
                    execute('run', project, 'Main.xaml', Path(temp)/'evidence')
                process.assert_called_once()

    def test_mixed_encoding_native_logs_are_preserved_byte_for_byte(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)/'project'
            project.mkdir()
            (project/'project.json').write_text('{}')
            raw = b'[WARN] accented legacy byte: \xe1\n'+json.dumps({'Result':'Success','Data':{'Success':True}}).encode()
            with patch('harness.course_tools.uipath_cli.official_cli', return_value=['node','official.js']), \
                 patch('harness.course_tools.uipath_cli.subprocess.run', return_value=subprocess.CompletedProcess([],0,raw,b'\xf6')):
                _, record = execute('build', project, None, Path(temp)/'evidence')
            self.assertTrue(record['success'])
            self.assertEqual((Path(temp)/'evidence/stdout.log').read_bytes(), raw)
            self.assertEqual((Path(temp)/'evidence/stderr.log').read_bytes(), b'\xf6')

    def test_workflow_outside_project_is_rejected_before_execution(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)/'project'
            project.mkdir()
            (project/'project.json').write_text('{}')
            (Path(temp)/'outside.xaml').write_text('<Activity/>')
            with patch('harness.course_tools.uipath_cli.official_cli', return_value=['node','official.js']), \
                 patch('harness.course_tools.uipath_cli.subprocess.run') as process:
                with self.assertRaises(ValueError):
                    execute('run', project, '../outside.xaml', Path(temp)/'evidence')
                process.assert_not_called()
