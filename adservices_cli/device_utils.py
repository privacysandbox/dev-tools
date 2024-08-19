# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Utils relating to devices."""

_ANDROID_11_VERSION_CODE = 30
_ANDROID_12_VERSION_CODE = 31
_ANDROID_12L_VERSION_CODE = 32


def is_extservices(version_code: int) -> bool:
  """Return if the device version should have extservices (not adservices)."""
  return version_code in [
      _ANDROID_11_VERSION_CODE,
      _ANDROID_12_VERSION_CODE,
      _ANDROID_12L_VERSION_CODE,
  ]
