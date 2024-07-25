"""Command for interacting with adservices."""

import webbrowser

import ad_selection
import adb
import constants
import custom_audience
import device_utils


class AdServices:
  """Privacy Sandbox for Android CLI (http://g.co/privacysandbox)."""

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
    print(
        "is adservices installed:"
        f" {self.adb.is_package_installed(constants.ADSERVICES_PACKAGE)}"
    )
    print(
        "is running:"
        f" {self.adb.is_process_running(constants.ADSERVICES_API_PACKAGE)}"
    )
    print(f"apex version: {self.adb.get_package(constants.ADSERVICES_PACKAGE)}")
    build_date = self.adb.getprop("ro.bootimage.build.date")
    print(f"build date: {build_date}")
    print(f"is userdebug: {self.adb.is_userdebug()}")
    for prop in [
        "ro.bootimage.build.version.release_or_codename",
        "debug.adservices.global_kill_switch",
        "debug.adservices.fledge_custom_audience_service_kill_switch",
        "debug.adservices.fledge_select_ads_kill_switch",
    ]:
      value = self.adb.getprop(prop)
      if not value:
        value = "unknown prop"
      print(f"{prop}: {value}")

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
    if not self.adb.is_package_installed(constants.ADSERVICES_PACKAGE):
      print("Error: adservices module is not installed.")
    else:
      self._set_service_enabled(True, disable_flag_push)

  def disable(self):
    """Disable the adservices process and feature flags.

    This command is the inverse of the `enable` command. After disabling the
    feature flags the adservices process is then killed.
    """
    if not self.adb.is_package_installed(constants.ADSERVICES_PACKAGE):
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
    if not self.adb.is_package_installed(constants.ADSERVICES_PACKAGE):
      print("Cannot kill adservice process. Module is not installed.")
      return
    if not self.adb.is_process_running(constants.ADSERVICES_API_PACKAGE):
      print("Cannot kill adservice process. Module is not running.")
      return

    self.adb.shell(f"am force-stop {constants.ADSERVICES_API_PACKAGE}")

    if self.adb.is_process_running(constants.ADSERVICES_API_PACKAGE):
      print("Error: adservices module is still running.")
    else:
      print("Success: adservices process is not running after killing.")

  def open_ui(self):
    """Open Privacy Sandbox UI on connected device."""
    self.adb.shell(
        "am start -n"
        f" {constants.ADSERVICES_API_PACKAGE}/{constants.ADSERVICES_UI_ACTIVITY_NAME}"
    )

  def open_docs(self):
    """Open Privacy Sandbox for Android documentation."""
    webbrowser.open(constants.ADSERVICES_DOCS_URL)

  def feedback(self):
    """Open Privacy Sandbox for DevTools feedback page."""
    webbrowser.open(constants.ADSERVICES_CLI_ISSUES_URL)

  def _is_service_supported(self) -> bool:
    # TODO(b/328846161): Add support for ExtServices.
    version_code = self.adb.get_sdk_version()
    adservices_ext = int(
        self.adb.getprop("build.version.extensions.ad_services")
    )
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

    for kill_switch in [
        "global_kill_switch",
        "fledge_custom_audience_service_kill_switch",
        "fledge_select_ads_kill_switch",
    ]:
      self.adb.put_device_config(
          "adservices",
          kill_switch,
          "false" if enabled else "true",
      )
      self.adb.setprop(
          f"debug.adservices.{kill_switch}", "false" if enabled else "true"
      )
    for feature_flag in [
        "adservice_system_service_enabled",
        "adservices_shell_command_enabled",
        "fledge_is_custom_audience_cli_enabled",
    ]:
      self.adb.put_device_config(
          "adservices",
          feature_flag,
          "true" if enabled else "false",
      )

    self.adb.set_sync_disabled_for_tests(
        "persistent" if enabled and disable_flag_push else "none",
    )
    print("Killing adservices process to reset flags.")
    self.kill()
