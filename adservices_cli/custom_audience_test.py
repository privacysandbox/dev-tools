import json

from absl.testing import absltest

import adb
import custom_audience

_TEST_NAME = 'test_name'
_TEST_INSTALLED_OWNER_PACKAGE = 'com.example.test'
_TEST_BUYER = 'com.example'
_TEST_CUSTOM_AUDIENCE_NAME = 'test_custom_audience_name'
_TEST_CUSTOM_AUDIENCE = {
    'name': _TEST_CUSTOM_AUDIENCE_NAME,
    'field': 'test_data',
}
_TEST_CUSTOM_AUDIENCE_MODIFIED = {
    'name': _TEST_CUSTOM_AUDIENCE_NAME,
    'field': 'modified_test_data',
}

_LIST_AUDIENCES_RESPONSE = json.dumps({'audiences': [_TEST_CUSTOM_AUDIENCE]})
_LIST_AUDIENCES_RESPONSE_EMPTY = json.dumps({'audiences': []})
_REFRESH_AUDIENCE_RESPONSE = json.dumps({})
_GET_AUDIENCE_RESPONSE = json.dumps({'audiences': [_TEST_CUSTOM_AUDIENCE]})
_GET_AUDIENCE_RESPONSE_MODIFIED = json.dumps(
    {'audiences': [_TEST_CUSTOM_AUDIENCE_MODIFIED]}
)
_GET_AUDIENCE_RESPONSE_EMPTY = json.dumps({'audiences': []})


_ARG_NAME = '--name'
_ARG_OWNER = '--owner'
_ARG_BUYER = '--buyer'


def _split_adb_command(command: str) -> list[str]:
  return command.split(' ')


class FakeAdb(adb.AdbClient):
  """Fake ADB client for testing.

  Shell calls are split apart into their base parts for assertions, for example
  a call to FakeAdb.shell("hello --world") will result in ("hello", "--world")
  being saved to the shell_calls field.

  Not thread-safe.
  """

  def __init__(self):
    """Initializes the fake ADB client."""
    self._shell_outputs = ''
    self.shell_calls = []

  def set_shell_output(self, output: str) -> None:
    """Sets the shell output."""
    self.set_shell_outputs([output])

  def set_shell_outputs(self, outputs: list[str]) -> None:
    """Sets the shell output."""
    self._shell_outputs = outputs

  def reset(self) -> None:
    self._shell_outputs = []
    self.shell_calls = []

  @property
  def shell_called(self) -> bool:
    return self.shell_calls

  def shell(self, command: str, silent: bool = False) -> str:
    output = self._shell_outputs.pop(0)
    self.shell_calls.append(_split_adb_command(command))
    return output

  def is_package_installed(self, package: str) -> bool:
    return package == _TEST_INSTALLED_OWNER_PACKAGE


class CustomAudienceTest(absltest.TestCase):

  def setUp(self):
    super().setUp()
    self.adb = FakeAdb()
    self.custom_audience = custom_audience.CustomAudience(self.adb)

  def tearDown(self):
    super().tearDown()
    self.adb.reset()

  def test_list_audiences_happy_path(self):
    self.adb.set_shell_output(json.dumps(_LIST_AUDIENCES_RESPONSE))

    output = self.custom_audience.list(
        owner_app_package=_TEST_INSTALLED_OWNER_PACKAGE,
        buyer=_TEST_BUYER,
    )

    self.assertContainsSubset(
        _split_adb_command(custom_audience._COMMAND_PREFIX)
        + [
            custom_audience._LIST_COMMAND,
            _ARG_OWNER,
            _TEST_INSTALLED_OWNER_PACKAGE,
            _ARG_BUYER,
            _TEST_BUYER,
        ],
        self.adb.shell_calls[0],
    )
    self.assertEqual(output, _LIST_AUDIENCES_RESPONSE)

  def test_list_audiences_empty_response(self):
    self.adb.set_shell_output(json.dumps(_LIST_AUDIENCES_RESPONSE_EMPTY))

    output = self.custom_audience.list(
        owner_app_package=_TEST_INSTALLED_OWNER_PACKAGE,
        buyer=_TEST_BUYER,
    )

    self.assertTrue(self.adb.shell_called)
    self.assertEqual(output, _LIST_AUDIENCES_RESPONSE_EMPTY)

  def test_list_audiences_bad_adb_response(self):
    self.adb.set_shell_output('bad_response #%%@')

    output = self.custom_audience.list(
        owner_app_package=_TEST_INSTALLED_OWNER_PACKAGE,
        buyer=_TEST_BUYER,
    )

    self.assertTrue(self.adb.shell_called)
    self.assertStartsWith(output, custom_audience.ERROR_FAILED_TO_PARSE)

  def test_get_audiences_happy_path(self):
    self.adb.set_shell_output(json.dumps(_GET_AUDIENCE_RESPONSE))

    output = self.custom_audience.get(
        name=_TEST_NAME,
        owner_app_package=_TEST_INSTALLED_OWNER_PACKAGE,
        buyer=_TEST_BUYER,
    )

    self.assertContainsSubset(
        _split_adb_command(custom_audience._COMMAND_PREFIX)
        + [
            custom_audience._GET_COMMAND,
            _ARG_OWNER,
            _TEST_INSTALLED_OWNER_PACKAGE,
            _ARG_BUYER,
            _TEST_BUYER,
            _ARG_NAME,
            _TEST_NAME,
        ],
        self.adb.shell_calls[0],
    )
    self.assertEqual(output, _GET_AUDIENCE_RESPONSE)

  def test_get_audiences_empty_response(self):
    self.adb.set_shell_output(json.dumps(_GET_AUDIENCE_RESPONSE_EMPTY))

    output = self.custom_audience.get(
        name=_TEST_NAME,
        owner_app_package=_TEST_INSTALLED_OWNER_PACKAGE,
        buyer=_TEST_BUYER,
    )

    self.assertTrue(self.adb.shell_called)
    self.assertEqual(output, _GET_AUDIENCE_RESPONSE_EMPTY)

  def test_get_audiences_bad_adb_response(self):
    self.adb.set_shell_output('bad_response #%%@')

    output = self.custom_audience.get(
        name=_TEST_NAME,
        owner_app_package=_TEST_INSTALLED_OWNER_PACKAGE,
        buyer=_TEST_BUYER,
    )

    self.assertStartsWith(output, custom_audience.ERROR_FAILED_TO_PARSE)

  def test_refresh_happy_path(self):
    self.adb.set_shell_outputs([
        json.dumps(_GET_AUDIENCE_RESPONSE),
        json.dumps(_REFRESH_AUDIENCE_RESPONSE),
        json.dumps(_GET_AUDIENCE_RESPONSE_MODIFIED),
    ])

    diffed_json = json.loads(
        self.custom_audience.refresh(
            name=_TEST_NAME,
            owner_app_package=_TEST_INSTALLED_OWNER_PACKAGE,
            buyer=_TEST_BUYER,
        )
    )

    self.assertEqual(
        diffed_json['diff'],
        '{"audiences": [{"name": "test_custom_audience_name", "field":'
        ' "modified_test_data"}]}',
    )
    parts = _split_adb_command(custom_audience._COMMAND_PREFIX) + [
        _ARG_OWNER,
        _TEST_INSTALLED_OWNER_PACKAGE,
        _ARG_BUYER,
        _TEST_BUYER,
        _ARG_NAME,
        _TEST_NAME,
    ]
    self.assertContainsSubset(
        parts + [custom_audience._GET_COMMAND],
        self.adb.shell_calls[0],
    )
    self.assertContainsSubset(
        parts + [custom_audience._REFRESH_COMMAND],
        self.adb.shell_calls[1],
    )
    self.assertContainsSubset(
        parts + [custom_audience._GET_COMMAND],
        self.adb.shell_calls[2],
    )


if __name__ == '__main__':
  absltest.main()
