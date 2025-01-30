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

"""Command for interacting with Protected Audience APIs."""

import json

import jsondiff

import adb
import utilities


ERROR_FAILED_TO_PARSE = "Failed to decode JSON response from device: "
ERROR_NOT_FOUND = "Custom audience not found."

_COMMAND_PREFIX = "custom-audience"
_GET_COMMAND = "view"
_LIST_COMMAND = "list"
_REFRESH_COMMAND = "refresh"

_ARG_NAME = "--name"
_ARG_OWNER = "--owner"
_ARG_BUYER = "--buyer"


class CustomAudience:
  """Interact with Custom Audience.

  Overview:
  https://developers.google.com/privacy-sandbox/relevance/protected-audience/android#custom-audience-management
  """

  def __init__(
      self,
      adb_client: adb.AdbClient,
  ):
    self._adb = adb_client

  def get(
      self,
      name: str,
      owner_app_package: str,
      buyer: str,
  ) -> str:
    """Get custom audience from the device.

    Args:
      name: Name of custom audience to query.
      owner_app_package: Package name of owning app.
      buyer: Ad tech buyer.

    Returns:
      Textual output of custom audiences data.
    """
    output = self._do_get_custom_audience(
        name=name,
        owner_app_package=owner_app_package,
        buyer=buyer,
    )
    try:
      return json.dumps(json.loads(output), indent=4)
    except json.JSONDecodeError:
      return ERROR_FAILED_TO_PARSE + output

  def list(
      self,
      owner_app_package: str,
      buyer: str,
  ) -> str:
    """List all custom audiences on the device.

    Args:
      owner_app_package: Package name of owning app.
      buyer: Ad tech buyer.

    Returns:
      Textual output of custom audiences data.
    """
    output = self._adb.execute_adservices_shell_command(
        utilities.format_command(
            _COMMAND_PREFIX,
            _LIST_COMMAND,
            "",
            {
                _ARG_OWNER: owner_app_package,
                _ARG_BUYER: buyer,
            },
        )
    )
    try:
      return json.dumps(json.loads(output), indent=4)
    except json.JSONDecodeError:
      return ERROR_FAILED_TO_PARSE + output

  def refresh(
      self,
      name: str,
      owner_app_package: str,
      buyer: str,
  ) -> str:
    """Refresh a custom audience on the device.

    Args:
      name: Name of custom audience to refresh.
      owner_app_package: Package name of owning app.
      buyer: Ad tech buyer.

    Returns:
      Textual output of custom audiences data.
    """
    try:
      existing_custom_audience = json.loads(
          self._do_get_custom_audience(name, owner_app_package, buyer)
      )
      if not existing_custom_audience:
        return ERROR_NOT_FOUND
      self._adb.execute_adservices_shell_command(
          utilities.format_command(
              _COMMAND_PREFIX,
              _REFRESH_COMMAND,
              "",
              {
                  _ARG_NAME: name,
                  _ARG_OWNER: owner_app_package,
                  _ARG_BUYER: buyer,
              },
          )
      )
      updated_custom_audience = json.loads(
          self._do_get_custom_audience(name, owner_app_package, buyer)
      )
      diff_in_ca = json.loads(
          jsondiff.diff(
              existing_custom_audience,
              updated_custom_audience,
              syntax="explicit",
              dump=True,
          )
      )
      return json.dumps(
          {
              "existing_custom_audience": existing_custom_audience,
              "updated_fields": diff_in_ca,
          },
          indent=4,
      )
    except json.JSONDecodeError:
      return ERROR_FAILED_TO_PARSE

  def _do_get_custom_audience(
      self,
      name: str,
      owner_app_package: str,
      buyer: str,
  ) -> str:
    return self._adb.execute_adservices_shell_command(
        utilities.format_command(
            _COMMAND_PREFIX,
            _GET_COMMAND,
            "",
            {_ARG_NAME: name, _ARG_OWNER: owner_app_package, _ARG_BUYER: buyer},
        )
    )
