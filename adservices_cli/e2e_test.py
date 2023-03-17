from unittest import mock

from absl.testing import absltest

from google3.wireless.android.adservices.devtools.adservices_cli import adb
from google3.wireless.android.adservices.devtools.adservices_cli import adservices


class AdservicesTest(absltest.TestCase):

  def setUp(self):
    super().setUp()
    self.adb = mock.create_autospec(adb.AdbClient)
    self.adservices = adservices.AdServices(self.adb)

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


if __name__ == '__main__':
  absltest.main()
