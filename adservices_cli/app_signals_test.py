# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
