# Copyright 2025 Google LLC
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

from unittest import mock

from absl.testing import absltest
from absl.testing import parameterized

import adb
import adservices
import constants
import flag_constants


class AdServicesTest(parameterized.TestCase):

  def setUp(self):
    super().setUp()
    self.adb = mock.create_autospec(adb.AdbClient)
    self.adservices = adservices.AdServices(self.adb)
    self.adb.get_sdk_version.return_value = 33

  @parameterized.named_parameters(
      {
          'testcase_name': 'all_enabled',
          'feature_name': flag_constants.FEATURE_ALL,
          'feature_enabled': True,
          'js_cache_enabled': 'false',
      },
      {
          'testcase_name': 'on_device_auction_enabled',
          'feature_name': flag_constants.ON_DEVICE_AUCTION,
          'feature_enabled': True,
          'js_cache_enabled': 'false',
      },
      {
          'testcase_name': 'on_device_auction_v3_enabled',
          'feature_name': flag_constants.ON_DEVICE_AUCTION_V3,
          'feature_enabled': True,
          'js_cache_enabled': 'false',
      },
      {
          'testcase_name': 'all_disabled',
          'feature_name': flag_constants.FEATURE_ALL,
          'feature_enabled': False,
          'js_cache_enabled': 'true',
      },
      {
          'testcase_name': 'on_device_auction_disabled',
          'feature_name': flag_constants.ON_DEVICE_AUCTION,
          'feature_enabled': False,
          'js_cache_enabled': 'true',
      },
      {
          'testcase_name': 'on_device_auction_v3_disabled',
          'feature_name': flag_constants.ON_DEVICE_AUCTION_V3,
          'feature_enabled': False,
          'js_cache_enabled': 'true',
      },
  )
  def test_set_service_enabled_sets_js_cache(
      self, feature_name, feature_enabled, js_cache_enabled
  ):
    self.adservices._set_service_enabled(feature_enabled, feature_name)

    self.adb.put_device_config.assert_any_call(
        constants.ADSERVICES_DEVICE_CONFIG_NAMESPACE,
        flag_constants.ENABLE_HTTP_CACHE_JS_CACHING,
        js_cache_enabled,
        silent=False,
    )


if __name__ == '__main__':
  absltest.main()
