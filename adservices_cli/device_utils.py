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
