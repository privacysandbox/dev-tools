"""Privacy Sandbox for Android CLI (http://g.co/privacysandbox)."""

import fire
from google3.wireless.android.adservices.devtools.adservices_cli import adb
from google3.wireless.android.adservices.devtools.adservices_cli import adservices


if __name__ == "__main__":
  fire.Fire(adservices.AdServices(adb.AdbClient()))
