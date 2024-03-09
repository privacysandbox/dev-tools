"""Command for interacting with adservices."""

import webbrowser

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
        f" {self.adb.is_process_running(constants.ADSERVICES_PACKAGE)}"
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
      override_consent: bool = False,
      disable_enrollment_check: bool = False,
  ):
    """Enable the adservices process and feature flags.

    This command will activate all adservices features such as Measurement, Ad
    Selection API, Custom Audience API, Topics, etc...

    Also disables enrollment checks for FLEDGE and Topics.

    Args:
      disable_flag_push: Disable remote feature flag pushes from Google.
      override_consent: Override the consent switch on the Privacy Sandbox UI.
      disable_enrollment_check: Disable enrollment check for AdTechs.
    """
    if not self.adb.is_package_installed(constants.ADSERVICES_PACKAGE):
      print("Error: adservices module is not installed.")
    else:
      self._set_service_enabled(
          True, disable_flag_push, override_consent, disable_enrollment_check
      )
      if not self.adb.is_process_running(constants.ADSERVICES_PACKAGE):
        print("Error: adservices module is not running.")

  def disable(self):
    """Disable the adservices process and feature flags.

    This command is the inverse of the `enable` command. After disabling the
    feature flags the adservices process is then killed.
    """
    if not self.adb.is_package_installed(constants.ADSERVICES_PACKAGE):
      print("Error: adservices module is not installed.")
    else:
      self._set_service_enabled(False)
      self.kill()

  def kill(self):
    """Kill the core adservices process if running.

    Send a SIGKILL to the adservices process.

    If the user doesn't have root access, then fallback to `am force-stop`
    instead. This is a fallback as force-stop also tears down any other
    processes in the adservices apex, and doesn't just stop the currently
    running process.
    """
    if not self.adb.is_package_installed(
        constants.ADSERVICES_PACKAGE
    ) or not self.adb.is_process_running(constants.ADSERVICES_PACKAGE):
      print("Error: adservices module is not installed or running.")
      return

    if not self.adb.is_root():
      self.adb.shell(f"am force-stop {constants.ADSERVICES_PACKAGE}")
      print("Warning: not root, using `am force-stop` as fallback.")
    else:
      self.adb.shell(f"su 0 killall -9 {constants.ADSERVICES_PACKAGE}")

    if self.adb.is_process_running(constants.ADSERVICES_PACKAGE):
      print("Error: adservices module is still running.")
    else:
      print("Success: adservices process is not running.")

  def open_ui(self):
    """Open Privacy Sandbox UI on connected device."""
    self.adb.shell(
        "am start -n"
        f" {constants.ADSERVICES_PACKAGE}/.{constants.ADSERVICES_UI_ACTIVITY_NAME}"
    )

  def open_docs(self):
    """Open Privacy Sandbox for Android documentation."""
    webbrowser.open(constants.ADSERVICES_DOCS_URL)

  def feedback(self):
    """Open Privacy Sandbox for DevTools feedback page."""
    webbrowser.open(constants.ADSERVICES_CLI_ISSUES_URL)

  def _is_service_supported(self) -> bool:
    # TODO(b/328846161): Add support for ExtServices.
    version_code = self.adb.get_sdk_version() >= 33
    return (
        bool(self.adb.getprop("build.version.extensions.ad_services"))
        and version_code >= 33
    ) and not device_utils.is_extservices(version_code)

  def _set_service_enabled(
      self,
      enabled: bool,
      disable_flag_push: bool = False,
      override_consent: bool = False,
      disable_enrollment_check: bool = False,
  ):
    """Set the adservices process and feature flags to enabled or not.

    Args:
      enabled: If true, disable all kill switches.
      disable_flag_push: If true, prevent remote flag pushes from being set.
        Uses the test override to do this.
      override_consent: Override the consent switch on the Privacy Sandbox UI.
      disable_enrollment_check: Disable enrollment check for AdTechs.
    """
    sdk_version = self.adb.get_sdk_version()
    is_root = self.adb.is_root()
    if sdk_version >= 34 and not is_root:
      print("Error: this command requires root in Android U+")
      return
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
    self.adb.put_device_config(
        "adservices",
        "disable_fledge_enrollment_check",
        "true" if enabled and disable_enrollment_check else "false",
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

    self.adb.put_device_config(
        "debug.adservices",
        "consent_manager_debug_mode",
        "true" if enabled and override_consent else "none",
    )
