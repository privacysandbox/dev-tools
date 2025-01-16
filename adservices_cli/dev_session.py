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

"""Command for interacting with AdServices dev sessions."""

import adb
import utilities


ERROR_FAILED_TO_PARSE = "Failed to decode JSON response from device: "
ERROR_NOT_FOUND = "Attribution reporting not found."

_COMMAND_PREFIX = "adservices-api"
_COMMAND = "dev-session"
_START_SUBCOMMAND = "start"
_END_SUBCOMMAND = "end"
_ARG_ERASE_DB = "--erase-db"

_MESSAGE_FAILURE_ERASE_DB = (
    "WARNING: Enabling a development session will cause the AdServices database"
    " to be reset to a factory new state. Re-run with the --erase-db flag to"
    " acknowledge."
)


class DevSession:
  """Interact with AdServices dev sessions."""

  def __init__(
      self,
      adb_client: adb.AdbClient,
  ):
    self._adb = adb_client

  def start(self, erase_db: bool = False) -> str:
    """Start a dev session.

    Args:
      erase_db: If true, erase the database.

    Returns:
      A success message if the dev session was started successfully.
    """
    if not erase_db:
      return _MESSAGE_FAILURE_ERASE_DB
    output = self._adb.execute_adservices_shell_command(
        utilities.format_command(
            _COMMAND_PREFIX,
            _COMMAND,
            _START_SUBCOMMAND,
            {
                _ARG_ERASE_DB: "",
            },
        )
    )

    return output

  def end(self, erase_db: bool = False) -> str:
    """End a dev session.

    Args:
      erase_db: If true, erase the database.

    Returns:
      A success message if the dev session was ended successfully.
    """
    if not erase_db:
      return _MESSAGE_FAILURE_ERASE_DB
    output = self._adb.execute_adservices_shell_command(
        utilities.format_command(
            _COMMAND_PREFIX,
            _COMMAND,
            _END_SUBCOMMAND,
            {
                _ARG_ERASE_DB: "",
            },
        )
    )
    return output
