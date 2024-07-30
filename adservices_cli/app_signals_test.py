from absl.testing import absltest

import app_signals
import constants
import fake_adb
import utilities

_TRIGGER_ENCODING_SUCCESS_RESPONSE = "Success"
_TRIGGER_ENCODING_FAILURE_RESPONSE = (
    "Could not find job 29 in package com.google.android.adservices.api /"
    " user 0"
)


class AdSelectionTest(absltest.TestCase):

  def setUp(self):
    super().setUp()
    self.adb = fake_adb.FakeAdb()
    self.app_signals = app_signals.AppSignals(self.adb)

  def tearDown(self):
    super().tearDown()
    self.adb.reset()

  def test_trigger_encoding_happy_path(self):
    self.adb.set_shell_outputs([
        _TRIGGER_ENCODING_SUCCESS_RESPONSE,
    ])

    output = self.app_signals.trigger_encoding()

    self.assertContainsSubset(
        utilities.split_adb_command(
            "cmd jobscheduler run -f"
            f" {constants.ADSERVICES_API_PACKAGE} {app_signals._TRIGGER_ENCODING_JOB_ID}"
        ),
        self.adb.shell_calls[0],
    )
    self.assertEqual(output, _TRIGGER_ENCODING_SUCCESS_RESPONSE)

  def test_trigger_encoding_failure(self):
    self.adb.set_shell_outputs([_TRIGGER_ENCODING_FAILURE_RESPONSE])

    output = self.app_signals.trigger_encoding()

    self.assertContainsSubset(
        utilities.split_adb_command(
            "cmd jobscheduler run -f"
            f" {constants.ADSERVICES_API_PACKAGE} {app_signals._TRIGGER_ENCODING_JOB_ID}"
        ),
        self.adb.shell_calls[0],
    )
    self.assertEqual(output, _TRIGGER_ENCODING_FAILURE_RESPONSE)


if __name__ == "__main__":
  absltest.main()
