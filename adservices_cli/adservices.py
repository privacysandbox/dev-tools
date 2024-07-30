"""Command for interacting with adservices."""

import webbrowser

import ad_selection
import adb
import custom_audience
import device_utils
import flag_constants


class AdServices:
  """Privacy Sandbox for Android CLI (http://g.co/privacysandbox)."""

  _ADSERVICES_SYSTEM_PROPERTIES_NAMESPACE = "debug.adservices"
  _ADSERVICES_DEVICE_CONFIG_NAMESPACE = "adservices"
  _ADSERVICES_PACKAGE = "com.google.android.adservices"
  _ADSERVICES_API_PACKAGE = "com.google.android.adservices.api"
  _ADSERVICES_DOCS_URL = (
      "https://developer.android.com/design-for-safety/privacy-sandbox"
  )
  _ADSERVICES_CLI_ISSUES_URL = (
      "https://github.com/privacysandbox/dev-tools/issues"
  )
  _ADSERVICES_UI_ACTIVITY_NAME = "com.android.adservices.ui.settings.activities.AdServicesSettingsMainActivity"

  def __init__(
      self,
      adb_client: adb.AdbClient,
  ):
    self.adb = adb_client
    self.custom_audience = custom_audience.CustomAudience(adb_client)
    self.ad_selection = ad_selection.AdSelection(adb_client)

  def status(self):
    """Print details about running adservices.

    This also queries for relevant device properties, such as the configuration
    for the Privacy Sandbox feature flag and enrollment checks.
    """
    print("DEVICE INFORMATION")
    sdk_version = self.adb.get_sdk_version()
    print(f"Android SDK Version: {sdk_version}")
    print(f"Is AdServices installed: {self._is_adservices_installed()}")
    print(f"AdServices extension version: {self._get_ad_services_version()}")
    print(f"Apex version: {self.adb.get_package(self._ADSERVICES_PACKAGE)}")
    print(f"Is AdServices running: {self._is_adservices_running()}")
    print("")
    print("AD SERVICES INFORMATION")
    for kill_switch in flag_constants.KILL_SWITCHES:
      sys_property_value = self._get_adservices_sys_prop(kill_switch)
      if not sys_property_value:
        sys_property_value = "unknown"
      print(f"{kill_switch}: {sys_property_value}")

    for flag in flag_constants.FEATURE_FLAGS:
      device_config_value = self._get_adservices_device_config(flag)
      if not device_config_value:
        device_config_value = "unknown"
      print(f"{flag}: {device_config_value}")

    for cli_flag in flag_constants.DEBUG_FLAGS:
      sys_property_value = self._get_adservices_sys_prop(cli_flag)
      if not sys_property_value:
        sys_property_value = "unknown"
      print(f"{cli_flag}: {sys_property_value}")

    for allow_list in flag_constants.ALLOW_LISTS:
      allow_list_value = self._get_adservices_device_config(allow_list)
      if not allow_list_value:
        allow_list_value = ""
      print(f"{allow_list}: {allow_list_value}")

  def enable(
      self,
      disable_flag_push: bool = False,
  ):
    """Enable the adservices process and feature flags.

    This command will activate all adservices features such as Measurement, Ad
    Selection API, Custom Audience API, Topics, etc...

    Also disables enrollment checks for FLEDGE and Topics.

    Args:
      disable_flag_push: Disable remote feature flag pushes from Google.
    """
    if not self._is_adservices_installed():
      print("Error: adservices module is not installed.")
    else:
      self._set_service_enabled(True, disable_flag_push)

  def disable(self):
    """Disable the adservices process and feature flags.

    This command is the inverse of the `enable` command. After disabling the
    feature flags the adservices process is then killed.
    """
    if not self._is_adservices_installed():
      print("Error: adservices module is not installed.")
    else:
      self._set_service_enabled(False)

  def kill(self):
    """Kill the core adservices process if running.

    Send a SIGKILL to the adservices process.

    If the user doesn't have root access, then fallback to `am force-stop`
    instead. This is a fallback as force-stop also tears down any other
    processes in the adservices apex, and doesn't just stop the currently
    running process.
    """
    if not self._is_adservices_installed():
      print("Cannot kill adservice process. Module is not installed.")
      return
    if not self._is_adservices_running():
      print("Cannot kill adservice process. Module is not running.")
      return

    self.adb.shell(f"am force-stop {self._ADSERVICES_API_PACKAGE}")

    if self._is_adservices_running():
      print("Error: adservices module is still running.")
    else:
      print("Success: adservices process is not running after killing.")

  def open_ui(self):
    """Open Privacy Sandbox UI on connected device."""
    self.adb.shell(
        "am start -n"
        f" {self._ADSERVICES_API_PACKAGE}/{self._ADSERVICES_UI_ACTIVITY_NAME}"
    )

  def open_docs(self):
    """Open Privacy Sandbox for Android documentation."""
    webbrowser.open(self._ADSERVICES_DOCS_URL)

  def feedback(self):
    """Open Privacy Sandbox for DevTools feedback page."""
    webbrowser.open(self._ADSERVICES_CLI_ISSUES_URL)

  def _is_service_supported(self) -> bool:
    # TODO(b/328846161): Add support for ExtServices.
    version_code = self.adb.get_sdk_version()
    adservices_ext = self._get_ad_services_version()
    return (
        version_code >= 33 and adservices_ext >= 4
    ) and not device_utils.is_extservices(version_code)

  def _set_service_enabled(
      self,
      enabled: bool,
      disable_flag_push: bool = False,
  ):
    """Set the adservices process and feature flags to enabled or not.

    Args:
      enabled: If true, disable all kill switches.
      disable_flag_push: If true, prevent remote flag pushes from being set.
        Uses the test override to do this.
    """
    if not self._is_service_supported():
      print("Warning: adservices is supported from 33-ext4+")

    kill_switch_value = "false" if enabled else "true"
    flag_value = "true" if enabled else "false"
    allow_list_value = '"*"' if enabled else '""'
    for kill_switch in flag_constants.KILL_SWITCHES:
      self._put_adservices_sys_prop(kill_switch, kill_switch_value)

    for flag in flag_constants.FEATURE_FLAGS:
      self._put_adservices_device_config(flag, flag_value)

    for cli_flag in flag_constants.DEBUG_FLAGS:
      self._put_adservices_sys_prop(cli_flag, flag_value)

    for allow_list in flag_constants.ALLOW_LISTS:
      self._put_adservices_device_config(allow_list, allow_list_value)

    self.adb.set_sync_disabled_for_tests(
        "persistent" if enabled and disable_flag_push else "none",
    )
    print("Killing adservices process to reset flags.")
    self.kill()

  def _get_ad_services_version(self) -> int:
    """Get AdServices extension version on device.

    Returns:
      int representation of SDK version, or -1 if unknown.
    """
    version_str = self.adb.getprop("build.version.extensions.ad_services")
    if not version_str:
      return -1
    return int(version_str)

  def _get_adservices_device_config(self, key: str, silent: bool = True) -> str:
    return self.adb.get_device_config(
        self._ADSERVICES_DEVICE_CONFIG_NAMESPACE, key, silent
    )

  def _put_adservices_device_config(self, key: str, value: str):
    self.adb.put_device_config(
        self._ADSERVICES_DEVICE_CONFIG_NAMESPACE, key, value, silent=False
    )

  def _get_adservices_sys_prop(self, key: str, silent: bool = True) -> str:
    return self.adb.getprop(
        f"{self._ADSERVICES_SYSTEM_PROPERTIES_NAMESPACE}.{key}", silent
    )

  def _put_adservices_sys_prop(self, key: str, value: str):
    self.adb.setprop(
        f"{self._ADSERVICES_SYSTEM_PROPERTIES_NAMESPACE}.{key}",
        value,
        silent=False,
    )

  def _is_adservices_installed(self) -> bool:
    """Return true if adservices is currently installed.

    Returns:
      true if package is currently installed.
    """
    return self.adb.is_package_installed(self._ADSERVICES_PACKAGE)

  def _is_adservices_running(self) -> bool:
    return self.adb.is_process_running(self._ADSERVICES_API_PACKAGE)
