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

_GET_AD_SELECTION_DATA_SHELL_CMD_RESPONSE = '{"output_proto":"EuoBCnEKCXdpbm5pbmdDQRIgYmEtYnV5ZXItNWp5eTV1bGFncS11Yy5hLnJ1bi5hcHASBGtleTES\\nBGtleTIaATEqAnt9Qi9jb20uZXhhbXBsZS5hZHNlcnZpY2VzLnNhbXBsZXMuZmxlZGdlLnNhbXBs\\nZWFwcAp1Cg1zaGlydHNfc2VydmVyEiBiYS1idXllci01anl5NXVsYWdxLXVjLmEucnVuLmFwcBIE\\na2V5MRIEa2V5MhoBMioCe31CL2NvbS5leGFtcGxlLmFkc2VydmljZXMuc2FtcGxlcy5mbGVkZ2Uu\\nc2FtcGxlYXBwGgJ7fSICe304AVICCgBYAQ==\\n"}'

_GET_AD_SELECTION_DATA_EXPECTED_RESPONSE = json.loads(
    '{"buyerInput":{"customAudiences":[{"name":"winningCA","biddingSignalsKeys":["ba-buyer-5jyy5ulagq-uc.a.run.app","key1","key2"],"adRenderIds":["1"],"userBiddingSignals":"{}","owner":"com.example.adservices.samples.fledge.sampleapp"},{"name":"shirts_server","biddingSignalsKeys":["ba-buyer-5jyy5ulagq-uc.a.run.app","key1","key2"],"adRenderIds":["2"],"userBiddingSignals":"{}","owner":"com.example.adservices.samples.fledge.sampleapp"}]},"auctionSignals":"{}","buyerSignals":"{}","enableDebugReporting":true,"protectedAppSignalsBuyerInput":{"protectedAppSignals":{}},"clientType":"CLIENT_TYPE_ANDROID"}'
)

_GET_AD_SELECTION_DATA_SHELL_CMD_NO_DATA_RESPONSE = (
    "could not find data for buyer: test-buyer"
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


if __name__ == "__main__":
  absltest.main()
