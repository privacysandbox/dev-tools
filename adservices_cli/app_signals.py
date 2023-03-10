"""
Copyright 2024 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

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
