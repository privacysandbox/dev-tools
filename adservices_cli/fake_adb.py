"""Utilities for testing adservices cli."""

import adb
import utilities

_TEST_INSTALLED_OWNER_PACKAGE = 'com.example.test'


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
    self.shell_calls.append(utilities.split_adb_command(command))
    return output

  def is_package_installed(self, package: str) -> bool:
    return package == _TEST_INSTALLED_OWNER_PACKAGE
