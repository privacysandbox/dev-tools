"""Privacy Sandbox for Android CLI (http://g.co/privacysandbox)."""

import fire
import adb
import adservices


if __name__ == "__main__":
  fire.Fire(adservices.AdServices(adb.AdbClient()))
