"""ADB commands expressed as simple functions."""

import subprocess


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
    return "root" in self.shell("id", silent=True)

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

  def _pidof(self, process: str) -> int:
    try:
      pid = self.shell(f"pidof -s {process}", silent=True)
    except subprocess.CalledProcessError as e:
      # pidof returns exit code 1 if no process was found.
      if e.returncode == 1:
        return -1
    return -1 if not pid else int(pid)
