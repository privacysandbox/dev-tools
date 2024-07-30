"""Command for interacting with Protected App Signals CLI Commands."""

import adb
import constants


_TRIGGER_ENCODING_JOB_ID = 29


class AppSignals:
  """Interact with Protected App Signals.

  Overview:
  https://developers.google.com/privacy-sandbox/relevance/protected-audience/android/protected-app-signals
  """

  def __init__(
      self,
      adb_client: adb.AdbClient,
  ):
    self._adb = adb_client

  def trigger_encoding(self) -> str:
    """Triggers encoding for all buyers who have updated signals on the device.

    Returns:
      Textual output of trigger encoding command.
    """
    return self._adb.run_scheduled_background_job(
        constants.ADSERVICES_API_PACKAGE, _TRIGGER_ENCODING_JOB_ID
    )
