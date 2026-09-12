"""Submission font guard must run before credentials, network, or cache writes."""
import contextlib
import io
import json
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "tools/manitoba-precalc-40s/pqp"
sys.path.insert(0, str(SCRIPT_DIR))
import mathpix_submit_manitoba as submit


class FontSubmissionGuardTests(unittest.TestCase):
    def check_batch(self, dry_run):
        documents = [SimpleNamespace(id="first"), SimpleNamespace(id="second")]
        clear = {"missing_mt_extra": []}
        bad = {"missing_mt_extra": [{"name": "MT-Extra"}], "affected_pages": [2], "unknown_codes": []}
        argv = ["submit", "--force"] + (["--dry-run"] if dry_run else [])
        output = io.StringIO()
        with patch.object(sys, "argv", argv), \
                patch.object(submit, "source_documents", return_value=documents), \
                patch.object(submit, "choose_upload_path", return_value=(Path("input.pdf"), "original")), \
                patch.object(submit, "inspect_pdf", side_effect=[clear, bad]), \
                patch.object(submit, "mathpix_headers") as headers, \
                patch.object(submit, "submit_pdf") as network, \
                patch.object(submit, "save_manifest") as save, \
                patch.object(submit, "load_manifest") as load, \
                contextlib.redirect_stdout(output):
            with self.assertRaises(SystemExit) as error:
                submit.main()
            self.assertEqual(error.exception.code, 2)
            headers.assert_not_called()
            network.assert_not_called()
            save.assert_not_called()
            load.assert_not_called()
        report = json.loads(output.getvalue())
        self.assertEqual(report["submitted"], [])
        self.assertEqual(report["blocked"][0]["id"], "second")
        self.assertEqual(report["dryRun"], dry_run)

    def test_later_blocker_prevents_earlier_paid_request_even_with_force(self):
        self.check_batch(False)

    def test_dry_run_reports_same_blocker(self):
        self.check_batch(True)


if __name__ == "__main__":
    unittest.main()
