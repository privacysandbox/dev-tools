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

from unittest import mock

from absl.testing import absltest

import adb
import adservices
import flag_constants


class AdServicesTest(absltest.TestCase):

  def setUp(self):
    super().setUp()
    self.adb = mock.create_autospec(adb.AdbClient)
    self.adservices = adservices.AdServices(self.adb)

    self.adb.get_sdk_version.return_value = 33
    self.adb.is_root.return_value = True

  def test_kill_with_root(self):
    self.adservices.kill()

    cmd = self.adb.shell.call_args.args[0]
    self.adb.shell.assert_called_once()
    self.assertIn('force-stop', cmd)

  def test_kill_without_root(self):
    self.adb.is_root.return_value = False

    self.adservices.kill()

    cmd = self.adb.shell.call_args.args[0]
    self.adb.shell.assert_called_once()
    self.assertIn('force-stop', cmd)

  def test_enable(self):
    self.adservices.enable(flag_constants.FEATURE_ALL)

    self.adb.put_device_config.assert_called()
    self.adb.setprop.assert_called()
    self.adb.set_sync_disabled_for_tests.assert_called_once_with('until_reboot')

  def test_enable_disable_flag_push_is_false(self):
    self.adservices.enable(flag_constants.FEATURE_ALL, False)

    self.adb.put_device_config.assert_called()
    self.adb.setprop.assert_called()
    self.adb.set_sync_disabled_for_tests.assert_called_once_with('none')

  def test_enable_invalid_argument(self):
    try:
      self.adservices.enable('invalid-argument')
    except ValueError as unused_error:
      pass

    self.adb.put_device_config.assert_not_called()
    self.adb.setprop.assert_not_called()

  def test_enable_without_root_android_34(self):
    self.adb.is_root.return_value = False
    self.adb.get_sdk_version.return_value = 34

    self.adservices.enable(flag_constants.FEATURE_ALL)

    self.adb.put_device_config.assert_called()
    self.adb.setprop.assert_called()

  def test_disable(self):
    self.adservices.disable('all')

    self.adb.put_device_config.assert_called()
    self.adb.setprop.assert_called()
    self.adb.set_sync_disabled_for_tests.assert_called_once_with('none')

  def test_disable_invalid_argument(self):
    try:
      self.adservices.disable('invalid-argument')
    except ValueError as unused_error:
      pass

    self.adb.put_device_config.assert_not_called()
    self.adb.setprop.assert_not_called()

  def test_status(self):
    self.adservices.status()

    self.adb.get_device_config.assert_called()
    self.adb.getprop.assert_called()

  def test_open_ui(self):
    self.adservices.open_ui()

    self.adb.shell.assert_called_once()

  @mock.patch('webbrowser.open', return_value=mock.MagicMock())
  def test_open_docs_calls_webbrowser(self, webbrowser_open_mock):
    self.adservices.open_docs()

    webbrowser_open_mock.assert_called_once()

  @mock.patch('webbrowser.open', return_value=mock.MagicMock())
  def test_open_feedback_calls_webbrowser(self, webbrowser_open_mock):
    self.adservices.feedback()

    webbrowser_open_mock.assert_called_once()


if __name__ == '__main__':
  absltest.main()
