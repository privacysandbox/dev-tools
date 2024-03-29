"""ADB commands expressed as simple functions."""

import subprocess
import sys


class AdbClient:
  """Client for interacting with ADB (Android Debug Bridge)."""

  def __init__(self):
    if not self.is_root():
      self.root()

  def root(self):
    """Try elevate to root permissions.

    Raises:
      CalledProcessError: if the underlying subprocess.run() command fails.
    """
    subprocess.run("adb root".split(" "), check=True)

  def is_root(self) -> bool:
    """Return true if ADB is root.

    Returns:
      true if ADB is root.
    """
    try:
      return "root" in self.shell("id", silent=True)
    except subprocess.CalledProcessError as e:
      if e.returncode == 1:
        print("Error: No device detected. Check `adb devices` and run again.")
        sys.exit(1)
      return False

  def get_package(self, package: str) -> str:
    """Return info for a given package.

    Args:
      package: key of the package to lookup.

    Returns:
      package info if currently installed, otherwise an empty string. Android
      package info format looks like "package:com.example versionCode:123".
    """
    packages = self.shell("pm list packages --show-versioncode", silent=True)
    for installed_package_info in packages.split("\n"):
      if package in installed_package_info:
        return package
    return ""

  def is_package_installed(self, package: str) -> bool:
    """Return true if a given package is currently installed.

    Args:
      package: key of the package to lookup.

    Returns:
      true if package is currently installed.
    """
    return self.get_package(package) is not None

  def is_process_running(self, process: str) -> bool:
    """Return true if a given process is currently running.

    Args:
      process: key of the process to lookup.

    Returns:
      true if process is currently running.
    """
    return self._pidof(process) > -1

  def is_userdebug(self) -> bool:
    """Return true if device is a userdebug build.

    Userdebug builds have a special property that allows us to inspect the SQL
    database for adservices, as well as run root commands.

    Returns:
      true if device is a userdebug build.
    """
    if not self.is_root():
      self.root()
    return self.getprop("ro.product.build.type") == "userdebug"

  def get_sdk_version(self) -> int:
    """Get Android SDK version on running device.

    Returns:
      int representation of SDK version, or -1 if unknown.
    """
    version_str = self.getprop("ro.build.version.sdk")
    if not version_str:
      return -1
    return int(version_str)

  def shell(self, command: str, silent: bool = False) -> str:
    """Run an arbitrary `adb shell` command.

    Args:
      command: shell command to execute on-device.
      silent: if false, print the command to stdout for additional debugging.

    Raises:
      CalledProcessError: if the underlying subprocess.run() command fails.

    Returns:
      string output for additional processing.
    """
    exec_command = f"adb shell {command}"
    if not silent:
      print(exec_command)
    result = subprocess.run(
        exec_command.split(" "), capture_output=True, check=True
    )
    return result.stdout.decode("utf-8").strip("\n")

  def get_device_config(self, namespace: str, key: str) -> str:
    """Get a device config value.

    Args:
      namespace: namespace of the device config to get. Should usually be
        `debug.adservices`.
      key: key of the device config to set.

    Returns:
      value of the device config.
    """
    return self.shell(f"device_config get {namespace} {key}")

  def put_device_config(self, namespace: str, key: str, value: str):
    """Set a device config value.

    Args:
      namespace: namespace of the device config to set. Should usually be
        `debug.adservices`.
      key: key of the device config to set.
      value: value of the device config to set.
    """
    self.shell(f"device_config put {namespace} {key} {value}")

  def set_sync_disabled_for_tests(self, value: str):
    """Set sync disabled for tests.

    Args:
      value: Sync disabled mode. Can be `none`, `persistent` or `until_reboot`
    """
    if value not in ("none", "persistent", "until_reboot"):
      print(
          "Error: Sync disabled mode must be `none`, `persistent` or"
          f" `until_reboot`. Was {value}."
      )
    self.shell(f"device_config set_sync_disabled_for_tests {value}")

  def getprop(self, key: str) -> str:
    """Get a system property.

    Args:
      key: key of the system property to set.

    Returns:
      value of the system property.
    """
    return self.shell(f"getprop {key}", silent=True)

  def setprop(self, key: str, value: str):
    """Set a system property.

    Args:
      key: key of the system property to set.
      value: value of the system property to set.
    """
    if not key:
      print("cannot setprop with empty key")
    if not value:
      print("cannot setprop with empty value")
    self.shell(f"setprop {key} {value}")

  def _pidof(self, process: str) -> int:
    try:
      pid = self.shell(f"pidof -s {process}", silent=True)
    except subprocess.CalledProcessError as e:
      # pidof returns exit code 1 if no process was found.
      if e.returncode == 1:
        return -1
    return -1 if not pid else int(pid)
