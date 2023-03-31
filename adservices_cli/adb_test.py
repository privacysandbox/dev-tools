from unittest import mock

from absl.testing import absltest

import adb


class AdbTest(absltest.TestCase):

  @mock.patch("subprocess.run", return_value=mock.MagicMock())
  def test_elevated_to_root_on_init(self, mock_subprocess_run):
    adb.AdbClient()

    self.assertIn("id", mock_subprocess_run.call_args_list[0].args[0])
    self.assertIn("root", mock_subprocess_run.call_args_list[1].args[0])


if __name__ == "__main__":
  absltest.main()
