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
