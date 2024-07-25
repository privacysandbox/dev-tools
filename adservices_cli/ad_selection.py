"""Command for interacting with Protected Audience Ad Selection CLI Commands."""

import json

import adb
import utilities


ERROR_FAILED_TO_PARSE = "Failed to decode JSON response from device: "
ERROR_NOT_FOUND = "Custom audience not found."

_COMMAND_PREFIX = "ad-selection"
_CONSENTED_DEBUG_COMMAND = "consented-debug"
_CONSENTED_DEBUG_COMMAND_ENABLE = "enable"
_CONSENTED_DEBUG_COMMAND_ENABLE_SECRET_DEBUG_TOKEN = "--secret-debug-token"
_CONSENTED_DEBUG_COMMAND_ENABLE_EXPIRY_IN_HOURS = "--expires-in-hours"
_CONSENTED_DEBUG_COMMAND_DISABLE = "disable"
_CONSENTED_DEBUG_COMMAND_VIEW = "view"


class AdSelection:
  """Interact with Ad Selection."""

  def __init__(
      self,
      adb_client: adb.AdbClient,
  ):
    self._adb = adb_client

  def view_consented_debug(self) -> str:
    """View adtech consented debugging information on the device.

    Returns:
      Textual output of consented debug view command.
    """
    view_output: str = self._adb.execute_adservices_shell_command(
        utilities.format_command(
            _COMMAND_PREFIX,
            _CONSENTED_DEBUG_COMMAND,
            _CONSENTED_DEBUG_COMMAND_VIEW,
            {},
        )
    )
    try:
      json_obj = json.loads(view_output)
      return json.dumps(json_obj, indent=4)
    except ValueError as unused_error:
      return view_output

  def enable_consented_debug(
      self,
      token: str,
      expiry_in_hours: int = 30 * 24,  # 30 days
  ) -> str:
    """Enable adtech consented debugging on the device.

    Args:
      token: Secret token which is also set on the TEE server.
      expiry_in_hours: Hours after which the consented debug will be disabled.

    Returns:
      Textual output of consented debug enable command.
    """

    enable_output: str = self._adb.execute_adservices_shell_command(
        utilities.format_command(
            _COMMAND_PREFIX,
            _CONSENTED_DEBUG_COMMAND,
            _CONSENTED_DEBUG_COMMAND_ENABLE,
            {
                _CONSENTED_DEBUG_COMMAND_ENABLE_SECRET_DEBUG_TOKEN: token,
                _CONSENTED_DEBUG_COMMAND_ENABLE_EXPIRY_IN_HOURS: (
                    expiry_in_hours
                ),
            },
        )
    )
    print(enable_output)
    return self.view_consented_debug()

  def disable_consented_debug(self) -> str:
    """Disable adtech consented debugging on the device.

    Returns:
      Textual output of consented debug disable command.
    """
    return self._adb.execute_adservices_shell_command(
        utilities.format_command(
            _COMMAND_PREFIX,
            _CONSENTED_DEBUG_COMMAND,
            _CONSENTED_DEBUG_COMMAND_DISABLE,
            {},
        )
    )
