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

import json

from absl.testing import absltest

import ad_selection
import fake_adb
import utilities

_TEST_TOKEN = "abcdefghij"
_TEST_EXPIRY = 24
_EXPECTED_TEST_EXPIRY = "24"
_ENABLE_CONSENTED_DEBUG_SUCCESS_RESPONSE = (
    "Successfully disabled consented debugging"
)
_VIEW_CONSENTED_DEBUG_NO_DATA = "No configuration for consented debug found"
_VIEW_CONSENTED_DEBUG_VIEW_RESPONSE = json.dumps(
    {"secret_debug_token": _TEST_TOKEN}
)
_DISABLED_CONSENTED_DEBUG_RESPONSE = (
    "Successfully disabled consented debugging."
)

_GET_AD_SELECTION_DATA_SHELL_CMD_RESPONSE = '{"output_proto":"EvgBCngKCXdpbm5pbmdDQRIFc2hvZXMSIGJhLWJ1eWVyLTVqeXk1dWxhZ3EtdWMuYS5ydW4uYXBwEgRrZXkxEgRrZXkyGgExKgJ7fUIvY29tLmV4YW1wbGUuYWRzZXJ2aWNlcy5zYW1wbGVzLmZsZWRnZS5zYW1wbGVhcHAKfAoNc2hpcnRzX3NlcnZlchIFc2hvZXMSIGJhLWJ1eWVyLTVqeXk1dWxhZ3EtdWMuYS5ydW4uYXBwEgRrZXkxEgRrZXkyGgEyKgJ7fUIvY29tLmV4YW1wbGUuYWRzZXJ2aWNlcy5zYW1wbGVzLmZsZWRnZS5zYW1wbGVhcHAaAnt9IgJ7fSpAUGxhY2Vob2xkZXItU2hvdWxkLU1hdGNoLVdpdGgtU2VsbGVyLU9yaWdpbi1Eb21haW4tSW4tU0ZFLUNvbmZpZzIuUGxhY2Vob2xkZXItU2hvdWxkLU1hdGNoLVdpdGgtQXBwLVBhY2thZ2UtTmFtZTgBSg4IARIKMTIzNDU2Nzg5MFICCgBYAWJKUGxhY2Vob2xkZXItU2hvdWxkLU1hdGNoLVdpdGgtVG9wLUxldmVsLVNlbGxlci1PcmlnaW4tRG9tYWluLUluLVNGRS1Db25maWdoAHAB"}'
_GET_AD_SELECTION_DATA_SHELL_CMD_RESPONSE_FOR_SELLER = '{"output_proto":"CooBCgtleGFtcGxlLmNvbRJ7H4sIAAAAAAAA\\/+NK5uIsz8zLy8xLd3YUYi3OyE8tFuJOrUjMLchJ\n1UvOzxViyU6tNASTRlKMhlpM1bVO+kBxPZiaxJTi1KKyzOTUYr1isEixXlpOakp6KpSbWFDAlc7F\nW5yRWVRSHA9Sm1pE2CIjsiwCAAj\\/PHbOAAAAEi5QbGFjZWhvbGRlci1TaG91bGQtTWF0Y2gtV2l0aC1BcHAtUGFja2FnZS1OYW1lGAEiFC01NjU2OTEzNzcwNjQ1MjI1NDIzKgAwAVAB"}'
_GET_AD_SELECTION_DATA_SHELL_CMD_RESPONSE_FOR_SELLER_EMPTY = '{"output_proto":"Ei5QbGFjZWhvbGRlci1TaG91bGQtTWF0Y2gtV2l0aC1BcHAtUGFja2FnZS1OYW1lGAEiFC00NzU2\nMjI2NjQ2NTEwODU1MjUzKgAwAVAB\n"}'
_GET_AD_SELECTION_DATA_SHELL_CMD_INVALID_PROTO_RESPONSE = '{"output_proto":"EvgBCngKCXdpbm5pbmdDQRIFc2hvZXMSIGJhLWJ1eWVyLTVqeXk1dWxhZ3EtdWMuYS5ydW4uYXBwEgRrZXkxEgRrZXkyGgExKgJ7fUIvY29tLmV4YW1wbGUuYWRzZXJ2aWNlcy5zYW1wbGVzLmZsZWRnZS5zYW1wbGVhcA=="}'


_GET_AD_SELECTION_DATA_EXPECTED_RESPONSE = json.loads(
    '{"buyerInput":{"interestGroups":[{"name":"winningCA","biddingSignalsKeys":["shoes","ba-buyer-5jyy5ulagq-uc.a.run.app","key1","key2"],"adRenderIds":["1"],"userBiddingSignals":"{}","origin":"com.example.adservices.samples.fledge.sampleapp"},{"name":"shirts_server","biddingSignalsKeys":["shoes","ba-buyer-5jyy5ulagq-uc.a.run.app","key1","key2"],"adRenderIds":["2"],"userBiddingSignals":"{}","origin":"com.example.adservices.samples.fledge.sampleapp"}]},"auctionSignals":"{}","buyerSignals":"{}","seller":"Placeholder-Should-Match-With-Seller-Origin-Domain-In-SFE-Config","publisherName":"Placeholder-Should-Match-With-App-Package-Name","enableDebugReporting":true,"consentedDebugConfig":{"isConsented":true,"token":"1234567890"},"protectedAppSignalsBuyerInput":{"protectedAppSignals":{}},"clientType":"CLIENT_TYPE_ANDROID","topLevelSeller":"Placeholder-Should-Match-With-Top-Level-Seller-Origin-Domain-In-SFE-Config","buyerKvExperimentGroupId":0,"enableUnlimitedEgress":true}'
)
_GET_AD_SELECTION_DATA_EXPECTED_RESPONSE_FOR_SELLER = json.loads(
    '{"auction_config":{"seller_signals":"Replace-With-Seller-Signals","auction_signals":"Replace-With-Auction-Signals","buyer_list":["example.com"],"seller":"Replace-With-Seller","per_buyer_config":{"example.com":{"buyer_signals":"Replace-With-Buyer-Signals","auction_signals":"Replace-With-Auction-Signals"}}},"client_type":"CLIENT_TYPE_ANDROID","raw_protected_audience_input":{"raw_buyer_input":{"example.com":{"interest_groups":[{"name":"winningCA","origin":"com.example.adservices.samples.fledge.sampleapp","bidding_signals_keys":["shoes","example.com","key1","key2"],"ad_render_ids":["1"],"component_ads":[],"user_bidding_signals":"{}"},{"name":"shirts_server","origin":"com.example.adservices.samples.fledge.sampleapp","bidding_signals_keys":["shoes","example.com","key1","key2"],"ad_render_ids":["2"],"component_ads":[],"user_bidding_signals":"{}"}]}},"publisher_name":"Placeholder-Should-Match-With-App-Package-Name","enable_debug_reporting":true,"generation_id":"-5656913770645225423","consented_debug_config":{"is_consented":false,"token":"","is_debug_info_in_response":false}}}'
)
_GET_AD_SELECTION_DATA_EXPECTED_RESPONSE_FOR_SELLER_EMPTY = json.loads(
    '{"client_type":"CLIENT_TYPE_ANDROID","auction_config":{"seller_signals":"Replace-With-Seller-Signals","auction_signals":"Replace-With-Auction-Signals","buyer_list":[],"seller":"Replace-With-Seller","per_buyer_config":{}},"raw_protected_audience_input":{"raw_buyer_input":{},"publisher_name":"Placeholder-Should-Match-With-App-Package-Name","enable_debug_reporting":true,"generation_id":"-4756226646510855253","consented_debug_config":{"is_consented":false,"token":"","is_debug_info_in_response":false}}}'
)

_GET_AD_SELECTION_DATA_SHELL_CMD_NO_DATA_RESPONSE = (
    "could not find data for buyer: test-buyer"
)

_TEST_AD_SELECTION_ID = "-123456789"
_VIEW_AUCTION_RESULT_SHELL_CMD_RESPONSE = '{"output_proto":"Ck9odHRwczovLzI0YjZiYjJjLTY1NzEtNDYzMi1iNTQ5LTZhNDk2YzE1MTk4OC5tb2NrLnBzdG1uLmlvL2JpZGRpbmcvcmVuZGVyX3Nob2VzGgVzaG9lcyIyMjRiNmJiMmMtNjU3MS00NjMyLWI1NDktNmE0OTZjMTUxOTg4Lm1vY2sucHN0bW4uaW81AAAgQUIECgAaAGovY29tLmV4YW1wbGUuYWRzZXJ2aWNlcy5zYW1wbGVzLmZsZWRnZS5zYW1wbGVhcHA="}'
_VIEW_AUCTION_RESULT_EXPECTED_RESPONSE = json.loads(
    '{"adRenderUrl":"https://24b6bb2c-6571-4632-b549-6a496c151988.mock.pstmn.io/bidding/render_shoes","interestGroupName":"shoes","interestGroupOwner":"24b6bb2c-6571-4632-b549-6a496c151988.mock.pstmn.io","bid":10.0,"winReportingUrls":{"buyerReportingUrls":{},"topLevelSellerReportingUrls":{}},"interestGroupOrigin":"com.example.adservices.samples.fledge.sampleapp"}'
)
_VIEW_AUCTION_RESULT_SHELL_CMD_NO_DATA_RESPONSE = (
    "no auction result found for ad selection id: " + _TEST_AD_SELECTION_ID
)


class AdSelectionTest(absltest.TestCase):

  def setUp(self):
    super().setUp()
    self.adb = fake_adb.FakeAdb()
    self.ad_selection = ad_selection.AdSelection(self.adb)

  def tearDown(self):
    super().tearDown()
    self.adb.reset()

  def test_enable_consented_debug_happy_path(self):
    self.adb.set_shell_outputs([
        _ENABLE_CONSENTED_DEBUG_SUCCESS_RESPONSE,
        _VIEW_CONSENTED_DEBUG_VIEW_RESPONSE,
    ])

    output = self.ad_selection.enable_consented_debug(
        token=_TEST_TOKEN,
        expiry_in_hours=_TEST_EXPIRY,
    )

    self.assertContainsSubset(
        utilities.split_adb_command(ad_selection._COMMAND_PREFIX)
        + [
            ad_selection._CONSENTED_DEBUG_COMMAND,
            ad_selection._CONSENTED_DEBUG_COMMAND_ENABLE,
            ad_selection._CONSENTED_DEBUG_COMMAND_ENABLE_SECRET_DEBUG_TOKEN,
            _TEST_TOKEN,
            ad_selection._CONSENTED_DEBUG_COMMAND_ENABLE_EXPIRY_IN_HOURS,
            _EXPECTED_TEST_EXPIRY,
        ],
        self.adb.shell_calls[0],
    )
    json_output = json.dumps(json.loads(output))
    self.assertEqual(json_output, _VIEW_CONSENTED_DEBUG_VIEW_RESPONSE)

  def test_view_consented_debug_happy_path(self):
    self.adb.set_shell_outputs([_VIEW_CONSENTED_DEBUG_VIEW_RESPONSE])

    output = self.ad_selection.view_consented_debug()

    self.assertContainsSubset(
        utilities.split_adb_command(ad_selection._COMMAND_PREFIX)
        + [
            ad_selection._CONSENTED_DEBUG_COMMAND,
            ad_selection._CONSENTED_DEBUG_COMMAND_VIEW,
        ],
        self.adb.shell_calls[0],
    )
    json_output = json.dumps(json.loads(output))
    self.assertEqual(json_output, _VIEW_CONSENTED_DEBUG_VIEW_RESPONSE)

  def test_view_consented_debug_no_data(self):
    self.adb.set_shell_outputs([_VIEW_CONSENTED_DEBUG_NO_DATA])

    output = self.ad_selection.view_consented_debug()

    self.assertContainsSubset(
        utilities.split_adb_command(ad_selection._COMMAND_PREFIX)
        + [
            ad_selection._CONSENTED_DEBUG_COMMAND,
            ad_selection._CONSENTED_DEBUG_COMMAND_VIEW,
        ],
        self.adb.shell_calls[0],
    )
    self.assertEqual(output, _VIEW_CONSENTED_DEBUG_NO_DATA)

  def test_disable_consented_debug_happy_path(self):
    self.adb.set_shell_outputs([_DISABLED_CONSENTED_DEBUG_RESPONSE])

    output = self.ad_selection.disable_consented_debug()

    self.assertContainsSubset(
        utilities.split_adb_command(ad_selection._COMMAND_PREFIX)
        + [
            ad_selection._CONSENTED_DEBUG_COMMAND,
            ad_selection._CONSENTED_DEBUG_COMMAND_DISABLE,
        ],
        self.adb.shell_calls[0],
    )
    self.assertEqual(output, _DISABLED_CONSENTED_DEBUG_RESPONSE)

  def test_get_ad_selection_data_happy_path(self):
    self.adb.set_shell_outputs([_GET_AD_SELECTION_DATA_SHELL_CMD_RESPONSE])
    buyer = "test-buyer"

    output = self.ad_selection.get_ad_selection_data(buyer)

    self.assertContainsSubset(
        utilities.split_adb_command(ad_selection._COMMAND_PREFIX)
        + [
            ad_selection._GET_AD_SELECTION_DATA_COMMAND,
        ],
        self.adb.shell_calls[0],
    )
    json_output = json.loads(output)
    self.assertEqual(json_output, _GET_AD_SELECTION_DATA_EXPECTED_RESPONSE)

  def test_get_ad_selection_data_happy_path_for_seller(self):
    self.adb.set_shell_outputs(
        [_GET_AD_SELECTION_DATA_SHELL_CMD_RESPONSE_FOR_SELLER]
    )

    output = self.ad_selection.get_ad_selection_data()

    self.assertContainsSubset(
        utilities.split_adb_command(ad_selection._COMMAND_PREFIX)
        + [
            ad_selection._GET_AD_SELECTION_DATA_COMMAND,
        ],
        self.adb.shell_calls[0],
    )
    print("output: ")
    print(output)
    json_output = json.loads(output)
    self.assertEqual(
        json_output, _GET_AD_SELECTION_DATA_EXPECTED_RESPONSE_FOR_SELLER
    )

  def test_get_ad_selection_data_happy_path_for_seller_empty(self):
    self.adb.set_shell_outputs(
        [_GET_AD_SELECTION_DATA_SHELL_CMD_RESPONSE_FOR_SELLER_EMPTY]
    )

    output = self.ad_selection.get_ad_selection_data()

    self.assertContainsSubset(
        utilities.split_adb_command(ad_selection._COMMAND_PREFIX)
        + [
            ad_selection._GET_AD_SELECTION_DATA_COMMAND,
        ],
        self.adb.shell_calls[0],
    )
    json_output = json.loads(output)
    self.assertEqual(
        json_output, _GET_AD_SELECTION_DATA_EXPECTED_RESPONSE_FOR_SELLER_EMPTY
    )

  def test_get_ad_selection_data_invalid_proto(self):
    self.adb.set_shell_outputs(
        [_GET_AD_SELECTION_DATA_SHELL_CMD_INVALID_PROTO_RESPONSE]
    )

    output = self.ad_selection.get_ad_selection_data(buyer="test-buyer")

    self.assertStartsWith(output, ad_selection._FAILURE_TEMPLATE % "")
    self.assertContainsSubset(
        utilities.split_adb_command(ad_selection._COMMAND_PREFIX)
        + [
            ad_selection._GET_AD_SELECTION_DATA_COMMAND,
        ],
        self.adb.shell_calls[0],
    )

  def test_get_ad_selection_data_invalid_proto_seller(self):
    self.adb.set_shell_outputs(
        [_GET_AD_SELECTION_DATA_SHELL_CMD_INVALID_PROTO_RESPONSE]
    )

    output = self.ad_selection.get_ad_selection_data()

    self.assertStartsWith(output, ad_selection._FAILURE_TEMPLATE % "")
    self.assertContainsSubset(
        utilities.split_adb_command(ad_selection._COMMAND_PREFIX)
        + [
            ad_selection._GET_AD_SELECTION_DATA_COMMAND,
        ],
        self.adb.shell_calls[0],
    )

  def test_get_ad_selection_data_no_data_for_buyer(self):
    self.adb.set_shell_outputs(
        [_GET_AD_SELECTION_DATA_SHELL_CMD_NO_DATA_RESPONSE]
    )
    buyer = "test-buyer"

    output = self.ad_selection.get_ad_selection_data(buyer)

    self.assertContainsSubset(
        utilities.split_adb_command(ad_selection._COMMAND_PREFIX)
        + [
            ad_selection._GET_AD_SELECTION_DATA_COMMAND,
        ],
        self.adb.shell_calls[0],
    )
    self.assertEqual(output, _GET_AD_SELECTION_DATA_SHELL_CMD_NO_DATA_RESPONSE)

  def test_view_auction_result_happy_path(self):
    self.adb.set_shell_outputs([_VIEW_AUCTION_RESULT_SHELL_CMD_RESPONSE])
    ad_selection_id = _TEST_AD_SELECTION_ID

    output = self.ad_selection.view_auction_result(ad_selection_id)

    self.assertContainsSubset(
        utilities.split_adb_command(ad_selection._COMMAND_PREFIX)
        + [
            ad_selection._VIEW_AUCTION_RESULT_COMMAND,
        ],
        self.adb.shell_calls[0],
    )
    json_output = json.loads(output)
    self.assertEqual(json_output, _VIEW_AUCTION_RESULT_EXPECTED_RESPONSE)

  def test_view_auction_result_no_data_for_ad_selection_id(self):
    self.adb.set_shell_outputs(
        [_VIEW_AUCTION_RESULT_SHELL_CMD_NO_DATA_RESPONSE]
    )
    ad_selection_id = _TEST_AD_SELECTION_ID

    output = self.ad_selection.view_auction_result(ad_selection_id)

    self.assertContainsSubset(
        utilities.split_adb_command(ad_selection._COMMAND_PREFIX)
        + [
            ad_selection._VIEW_AUCTION_RESULT_COMMAND,
        ],
        self.adb.shell_calls[0],
    )
    self.assertEqual(output, _VIEW_AUCTION_RESULT_SHELL_CMD_NO_DATA_RESPONSE)


if __name__ == "__main__":
  absltest.main()
