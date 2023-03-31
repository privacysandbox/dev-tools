from unittest import mock

from absl.testing import absltest

import adb
import adservices


class AdservicesTest(absltest.TestCase):

  def setUp(self):
    super().setUp()
    self.adb = mock.create_autospec(adb.AdbClient)
    self.adservices = adservices.AdServices(self.adb)
    self.adb.get_sdk_version.return_value = 33

  def test_kill_with_root(self):
    self.adb.is_root.return_value = True

    self.adservices.kill()

    cmd = self.adb.shell.call_args.args[0]
    self.adb.shell.assert_called_once()
    self.assertIn('killall', cmd)

  def test_kill_without_root(self):
    self.adb.is_root.return_value = False

    self.adservices.kill()

    cmd = self.adb.shell.call_args.args[0]
    self.adb.shell.assert_called_once()
    self.assertIn('force-stop', cmd)

  def test_enable(self):
    self.adservices.enable()

    self.adb.put_device_config.assert_called()
    self.adb.setprop.assert_called()

  def test_disable(self):
    self.adservices.disable()

    self.adb.put_device_config.assert_called()
    self.adb.setprop.assert_called()

  def test_status(self):
    self.adservices.status()

    self.adb.getprop.assert_called()


if __name__ == '__main__':
  absltest.main()
