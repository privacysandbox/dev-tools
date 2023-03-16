"""Command for interacting with adservices."""

from google3.wireless.android.adservices.devtools.adservices_cli import adb

ADSERVICES_PACKAGE = "com.google.android.adservices.api"


class AdServices:
  """Privacy Sandbox for Android CLI (http://g.co/privacysandbox)."""

  def __init__(
      self,
      adb_client: adb.AdbClient,
  ):
    self.adb = adb_client

  def kill(self):
    """Kill the core adservices process if running.

    Send a SIGKILL to the adservices process.

    If the user doesn't have root access, then fallback to `am force-stop`
    instead. This is a fallback as force-stop also tears down any other
    processes in the adservices apex, and doesn't just stop the currently
    running process.
    """
    if not self.adb.is_package_installed(
        ADSERVICES_PACKAGE
    ) or not self.adb.is_process_running(ADSERVICES_PACKAGE):
      print("Error: adservices module is not installed or running.")
      return

    if not self.adb.is_root():
      self.adb.shell(f"am force-stop {ADSERVICES_PACKAGE}")
      print("Warning: not root, using `am force-stop` as fallback.")
    else:
      self.adb.shell(f"su 0 killall -9 {ADSERVICES_PACKAGE}")

    if self.adb.is_process_running(ADSERVICES_PACKAGE):
      print("Error: adservices module is still running.")
    else:
      print("Success: adservices process is not running.")
