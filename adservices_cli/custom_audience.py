"""Command for interacting with Protected Audience APIs."""

import json

import jsondiff

import adb


ERROR_FAILED_TO_PARSE = "Failed to decode JSON response from device: "
ERROR_NOT_FOUND = "Custom audience not found."

_COMMAND_PREFIX = "cmd adservices_manager custom-audience"
_GET_COMMAND = "view"
_LIST_COMMAND = "list"
_REFRESH_COMMAND = "refresh"


def _make_command(command_name: str, **kwargs) -> str:
  """Makes a command to run on the device.

  Args:
    command_name: Raw command name to execute.
    **kwargs: --key=value arguments to be passed to the command.

  Returns:
    (str) formatted to run via ADB.
  """
  args = [_COMMAND_PREFIX, command_name]
  for arg_name, arg_value in kwargs.items():
    args.append("--" + arg_name)
    args.append(arg_value)
  return " ".join(args)


class CustomAudience:
  """Interact with Protected Audience.

  This includes Custom Audience and Ad Selection.
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
    output = self._adb.shell(
        _make_command(
            _LIST_COMMAND,
            owner=owner_app_package,
            buyer=buyer,
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
      self._adb.shell(
          _make_command(
              _REFRESH_COMMAND,
              name=name,
              owner=owner_app_package,
              buyer=buyer,
          )
      )
      updated_custom_audience = json.loads(
          self._do_get_custom_audience(name, owner_app_package, buyer)
      )
      return json.dumps(
          {
              "existing_custom_audience": existing_custom_audience,
              "updated_fields": jsondiff.diff(
                  existing_custom_audience,
                  updated_custom_audience,
              ),
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
    return self._adb.shell(
        _make_command(
            _GET_COMMAND,
            name=name,
            owner=owner_app_package,
            buyer=buyer,
        )
    )
