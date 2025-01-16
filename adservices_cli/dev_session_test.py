# Copyright 2025 Google LLC
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

import dev_session
import fake_adb


class DevSessionTest(absltest.TestCase):
  """Tests for DevSession."""

  def setUp(self):
    super().setUp()
    self.fake_adb = fake_adb.FakeAdb()
    self.session = dev_session.DevSession(self.fake_adb)

  def test_start_success(self):
    """Test case: Enable a dev session successfully."""
    expected_output = "Dev session started successfully."
    self.fake_adb.set_shell_output(expected_output)

    output = self.session.start(erase_db=True)

    self.assertEqual(output, expected_output)

  def test_end_success(self):
    """Test case: Disable a dev session successfully."""
    expected_output = "Dev session ended successfully."
    self.fake_adb.set_shell_output(expected_output)

    output = self.session.end(erase_db=True)

    self.assertEqual(output, expected_output)

  def test_start_erase_db_already_in_dev_mode(self):
    """Test case: Enable a dev session with erase db when already in dev mode."""
    expected_output = (
        "Error occurred while running adb shell cmd adservices_manager"
        " adservices-api dev-session start --erase-db \nAlready in developer"
        " mode. Call 'end' and 'start' to reset state."
    )
    self.fake_adb.set_shell_output(expected_output)

    output = self.session.start(erase_db=True)

    self.assertEqual(output, expected_output)

  def test_end_erase_db_success(self):
    """Test case: Disable a dev session and erase db successfully."""
    expected_output = "Successfully changed developer mode to: false"
    self.fake_adb.set_shell_output(expected_output)

    output = self.session.end(erase_db=True)

    self.assertEqual(output, expected_output)

  def test_start_failure_erase_db_flag_not_set(self):
    """Test case: Failure starting a dev session due to no erase db flag."""
    output = self.session.start()

    self.assertEqual(output, dev_session._MESSAGE_FAILURE_ERASE_DB)

  def test_end_failure_erase_db_flag_not_set(self):
    """Test case: Failure when ending a dev session due to no erase db flag."""
    output = self.session.end()

    self.assertEqual(output, dev_session._MESSAGE_FAILURE_ERASE_DB)


if __name__ == "__main__":
  absltest.main()
