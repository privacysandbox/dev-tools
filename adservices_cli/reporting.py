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

"""Command for interacting with Attribution Reporting API."""

import json

import adb
import utilities


ERROR_FAILED_TO_PARSE = "Failed to decode JSON response from device: "
ERROR_NOT_FOUND = "Attribution reporting not found."

_COMMAND_PREFIX = "attribution-reporting"
_LIST_COMMAND = "list_source_registrations"


class Reporting:
  """Interact with Attribution Reporting.

  Overview:
  https://developers.google.com/privacy-sandbox/private-advertising/attribution-reporting
  """

  def __init__(
      self,
      adb_client: adb.AdbClient,
  ):
    self._adb = adb_client

  def list_source_registrations(
      self
  ) -> str:
    """List all source registrations on the device.

    Returns:
      Textual output of attribution reporting data.
    """
    output = self._adb.execute_adservices_shell_command(
        utilities.format_command(
            _COMMAND_PREFIX,
            _LIST_COMMAND,
            "",
            {},
        )
    )
    try:
      return json.dumps(json.loads(output), indent=4)
    except json.JSONDecodeError:
      return ERROR_FAILED_TO_PARSE + output
