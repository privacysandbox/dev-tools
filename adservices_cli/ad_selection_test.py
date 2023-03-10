"""
Copyright 2024 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import json

from absl.testing import absltest

import ad_selection
import fake_adb
import utilities

_TEST_TOKEN = "abcdefghij"
_TEST_EXPIRY = 24
_EXPECTED_TEST_EXPIRY = "24"
_ENABLE_CONSENTED_DEBUG_SUCCESS_RESPONSE = (
    "Successfully disabled consented debugging"
)
_VIEW_CONSENTED_DEBUG_NO_DATA = "No configuration for consented debug found"
_VIEW_CONSENTED_DEBUG_VIEW_RESPONSE = json.dumps(
    {"secret_debug_token": _TEST_TOKEN}
)
_DISABLED_CONSENTED_DEBUG_RESPONSE = (
    "Successfully disabled consented debugging."
)


class AdSelectionTest(absltest.TestCase):

  def setUp(self):
    super().setUp()
    self.adb = fake_adb.FakeAdb()
    self.ad_selection = ad_selection.AdSelection(self.adb)

  def tearDown(self):
    super().tearDown()
    self.adb.reset()

  def test_enable_consented_debug_happy_path(self):
    self.adb.set_shell_outputs([
        _ENABLE_CONSENTED_DEBUG_SUCCESS_RESPONSE,
        _VIEW_CONSENTED_DEBUG_VIEW_RESPONSE,
    ])

    output = self.ad_selection.enable_consented_debug(
        token=_TEST_TOKEN,
        expiry_in_hours=_TEST_EXPIRY,
    )

    self.assertContainsSubset(
        utilities.split_adb_command(ad_selection._COMMAND_PREFIX)
        + [
            ad_selection._CONSENTED_DEBUG_COMMAND,
            ad_selection._CONSENTED_DEBUG_COMMAND_ENABLE,
            ad_selection._CONSENTED_DEBUG_COMMAND_ENABLE_SECRET_DEBUG_TOKEN,
            _TEST_TOKEN,
            ad_selection._CONSENTED_DEBUG_COMMAND_ENABLE_EXPIRY_IN_HOURS,
            _EXPECTED_TEST_EXPIRY,
        ],
        self.adb.shell_calls[0],
    )
    json_output = json.dumps(json.loads(output))
    self.assertEqual(json_output, _VIEW_CONSENTED_DEBUG_VIEW_RESPONSE)

  def test_view_consented_debug_happy_path(self):
    self.adb.set_shell_outputs([_VIEW_CONSENTED_DEBUG_VIEW_RESPONSE])

    output = self.ad_selection.view_consented_debug()

    self.assertContainsSubset(
        utilities.split_adb_command(ad_selection._COMMAND_PREFIX)
        + [
            ad_selection._CONSENTED_DEBUG_COMMAND,
            ad_selection._CONSENTED_DEBUG_COMMAND_VIEW,
        ],
        self.adb.shell_calls[0],
    )
    json_output = json.dumps(json.loads(output))
    self.assertEqual(json_output, _VIEW_CONSENTED_DEBUG_VIEW_RESPONSE)

  def test_view_consented_debug_no_data(self):
    self.adb.set_shell_outputs([_VIEW_CONSENTED_DEBUG_NO_DATA])

    output = self.ad_selection.view_consented_debug()

    self.assertContainsSubset(
        utilities.split_adb_command(ad_selection._COMMAND_PREFIX)
        + [
            ad_selection._CONSENTED_DEBUG_COMMAND,
            ad_selection._CONSENTED_DEBUG_COMMAND_VIEW,
        ],
        self.adb.shell_calls[0],
    )
    self.assertEqual(output, _VIEW_CONSENTED_DEBUG_NO_DATA)

  def test_disable_consented_debug_happy_path(self):
    self.adb.set_shell_outputs([_DISABLED_CONSENTED_DEBUG_RESPONSE])

    output = self.ad_selection.disable_consented_debug()

    self.assertContainsSubset(
        utilities.split_adb_command(ad_selection._COMMAND_PREFIX)
        + [
            ad_selection._CONSENTED_DEBUG_COMMAND,
            ad_selection._CONSENTED_DEBUG_COMMAND_DISABLE,
        ],
        self.adb.shell_calls[0],
    )
    self.assertEqual(output, _DISABLED_CONSENTED_DEBUG_RESPONSE)


if __name__ == "__main__":
  absltest.main()
