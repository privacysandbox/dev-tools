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

import custom_audience
import fake_adb
import utilities

_TEST_NAME = 'test_name'
_TEST_INSTALLED_OWNER_PACKAGE = 'com.example.test'
_TEST_BUYER = 'com.example'

_TEST_CUSTOM_AUDIENCE = json.loads(
    '{"name":"shoes","owner":"com.example.adservices.samples.fledge.sampleapp","buyer":"buyer-example.com","daily_update":{"uri":"https://buyer-example.com/dailyupdate/shoes","eligible_update_time":"2025-01-16T14:13:23.245Z","num_validation_failures":0,"num_timeout_failures":0},"is_debuggable":true,"creation_time":"2025-01-15T14:13:23.245Z","activation_time":"2025-01-15T14:13:23.245Z","expiration_time":"2025-03-16T14:13:23.245Z","updated_time":"2025-01-15T14:13:23.245Z","bidding_logic_uri":"https://buyer-example.com/buyer/bidding/simple_logic","user_bidding_signals":"{}","is_eligible_for_on_device_auction":true,"is_eligible_for_server_auction":false,"uri":"https://buyer-example.com/dailyupdate/shoes","trusted_bidding_data":{"uri":"https://buyer-example.com/bidding/trusted","keys":["shoes","buyer-example.com","key1","key2"]},"ads":[{"render_uri":"https://buyer-example.com/buyer/bidding/render_shoes","metadata":"{}","ad_counter_keys":[]}]}'
)

_TEST_CUSTOM_AUDIENCE_MODIFIED = json.loads(
    '{"name":"shoes","owner":"com.example.adservices.samples.fledge.sampleapp","buyer":"buyer-example.com","daily_update":{"uri":"https://buyer-example.com/dailyupdate/shoes","eligible_update_time":"2025-01-16T14:15:28.050Z","num_validation_failures":0,"num_timeout_failures":0},"is_debuggable":true,"creation_time":"2025-01-15T14:13:23.245Z","activation_time":"2025-01-15T14:13:23.245Z","expiration_time":"2025-03-16T14:13:23.245Z","updated_time":"2025-01-15T14:15:28.050Z","bidding_logic_uri":"https://buyer-example.com/buyer/bidding/simple_logic","user_bidding_signals":{"valid":true,"arbitrary":"yes"},"is_eligible_for_on_device_auction":true,"is_eligible_for_server_auction":false,"uri":"https://buyer-example.com/dailyupdate/shoes","trusted_bidding_data":{"uri":"https://buyer-example.com/trusted/biddingsignals/simple","keys":["key1","key2"]},"ads":[{"render_uri":"https://buyer-example.com/render/shoes/ad0?date=2025-01-15","metadata":{"bid":1},"ad_counter_keys":[]},{"render_uri":"https://buyer-example.com/render/shoes/ad1?date=2025-01-15","metadata":{"bid":2},"ad_counter_keys":[]},{"render_uri":"https://buyer-example.com/render/shoes/ad2?date=2025-01-15","metadata":{"bid":3},"ad_counter_keys":[]},{"render_uri":"https://buyer-example.com/render/shoes/ad3?date=2025-01-15","metadata":{"bid":4},"ad_counter_keys":[]},{"render_uri":"https://buyer-example.com/render/shoes/ad4?date=2025-01-15","metadata":{"bid":5},"ad_counter_keys":[]}]}'
)

_REFRESH_COM_EXPECTED_OUTPUT = json.loads(
    '{"existing_custom_audience":{"name":"shoes","owner":"com.example.adservices.samples.fledge.sampleapp","buyer":"buyer-example.com","daily_update":{"uri":"https://buyer-example.com/dailyupdate/shoes","eligible_update_time":"2025-01-16T14:13:23.245Z","num_validation_failures":0,"num_timeout_failures":0},"is_debuggable":true,"creation_time":"2025-01-15T14:13:23.245Z","activation_time":"2025-01-15T14:13:23.245Z","expiration_time":"2025-03-16T14:13:23.245Z","updated_time":"2025-01-15T14:13:23.245Z","bidding_logic_uri":"https://buyer-example.com/buyer/bidding/simple_logic","user_bidding_signals":"{}","is_eligible_for_on_device_auction":true,"is_eligible_for_server_auction":false,"uri":"https://buyer-example.com/dailyupdate/shoes","trusted_bidding_data":{"uri":"https://buyer-example.com/bidding/trusted","keys":["shoes","buyer-example.com","key1","key2"]},"ads":[{"render_uri":"https://buyer-example.com/buyer/bidding/render_shoes","metadata":"{}","ad_counter_keys":[]}]},"updated_fields":{"$update":{"daily_update":{"$update":{"eligible_update_time":"2025-01-16T14:15:28.050Z"}},"updated_time":"2025-01-15T14:15:28.050Z","user_bidding_signals":{"valid":true,"arbitrary":"yes"},"trusted_bidding_data":{"$update":{"uri":"https://buyer-example.com/trusted/biddingsignals/simple","keys":{"$delete":[1,0]}}},"ads":{"4":{"$update":{"render_uri":"https://buyer-example.com/render/shoes/ad4?date=2025-01-15","metadata":{"bid":5}}},"$insert":[[0,{"render_uri":"https://buyer-example.com/render/shoes/ad0?date=2025-01-15","metadata":{"bid":1},"ad_counter_keys":[]}],[1,{"render_uri":"https://buyer-example.com/render/shoes/ad1?date=2025-01-15","metadata":{"bid":2},"ad_counter_keys":[]}],[2,{"render_uri":"https://buyer-example.com/render/shoes/ad2?date=2025-01-15","metadata":{"bid":3},"ad_counter_keys":[]}],[3,{"render_uri":"https://buyer-example.com/render/shoes/ad3?date=2025-01-15","metadata":{"bid":4},"ad_counter_keys":[]}]]}}}}'
)

_LIST_AUDIENCES_RESPONSE = {'audiences': [_TEST_CUSTOM_AUDIENCE]}
_LIST_AUDIENCES_RESPONSE_EMPTY = {'audiences': []}
_REFRESH_AUDIENCE_RESPONSE = {}
_GET_AUDIENCE_RESPONSE = _TEST_CUSTOM_AUDIENCE
_GET_AUDIENCE_RESPONSE_MODIFIED = _TEST_CUSTOM_AUDIENCE_MODIFIED
_GET_AUDIENCE_RESPONSE_EMPTY = {}


class CustomAudienceTest(absltest.TestCase):

  def setUp(self):
    super().setUp()
    self.adb = fake_adb.FakeAdb()
    self.custom_audience = custom_audience.CustomAudience(self.adb)

  def tearDown(self):
    super().tearDown()
    self.adb.reset()

  def test_list_audiences_happy_path(self):
    self.adb.set_shell_output(json.dumps(_LIST_AUDIENCES_RESPONSE))

    output = self.custom_audience.list(
        owner_app_package=_TEST_INSTALLED_OWNER_PACKAGE,
        buyer=_TEST_BUYER,
    )

    self.assertContainsSubset(
        utilities.split_adb_command(custom_audience._COMMAND_PREFIX)
        + [
            custom_audience._LIST_COMMAND,
            custom_audience._ARG_OWNER,
            _TEST_INSTALLED_OWNER_PACKAGE,
            custom_audience._ARG_BUYER,
            _TEST_BUYER,
        ],
        self.adb.shell_calls[0],
    )
    self.assertEqual(json.loads(output), _LIST_AUDIENCES_RESPONSE)

  def test_list_audiences_empty_response(self):
    self.adb.set_shell_output(json.dumps(_LIST_AUDIENCES_RESPONSE_EMPTY))

    output = self.custom_audience.list(
        owner_app_package=_TEST_INSTALLED_OWNER_PACKAGE,
        buyer=_TEST_BUYER,
    )

    self.assertTrue(self.adb.shell_called)
    self.assertEqual(json.loads(output), _LIST_AUDIENCES_RESPONSE_EMPTY)

  def test_list_audiences_bad_adb_response(self):
    self.adb.set_shell_output('bad_response #%%@')

    output = self.custom_audience.list(
        owner_app_package=_TEST_INSTALLED_OWNER_PACKAGE,
        buyer=_TEST_BUYER,
    )

    self.assertTrue(self.adb.shell_called)
    self.assertStartsWith(output, custom_audience.ERROR_FAILED_TO_PARSE)

  def test_get_audiences_happy_path(self):
    self.adb.set_shell_output(json.dumps(_GET_AUDIENCE_RESPONSE))

    output = self.custom_audience.get(
        name=_TEST_NAME,
        owner_app_package=_TEST_INSTALLED_OWNER_PACKAGE,
        buyer=_TEST_BUYER,
    )

    self.assertContainsSubset(
        utilities.split_adb_command(custom_audience._COMMAND_PREFIX)
        + [
            custom_audience._GET_COMMAND,
            custom_audience._ARG_OWNER,
            _TEST_INSTALLED_OWNER_PACKAGE,
            custom_audience._ARG_BUYER,
            _TEST_BUYER,
            custom_audience._ARG_NAME,
            _TEST_NAME,
        ],
        self.adb.shell_calls[0],
    )
    self.assertEqual(json.loads(output), _GET_AUDIENCE_RESPONSE)

  def test_get_audiences_empty_response(self):
    self.adb.set_shell_output(json.dumps(_GET_AUDIENCE_RESPONSE_EMPTY))

    output = self.custom_audience.get(
        name=_TEST_NAME,
        owner_app_package=_TEST_INSTALLED_OWNER_PACKAGE,
        buyer=_TEST_BUYER,
    )

    self.assertTrue(self.adb.shell_called)
    self.assertEqual(json.loads(output), _GET_AUDIENCE_RESPONSE_EMPTY)

  def test_get_audiences_bad_adb_response(self):
    self.adb.set_shell_output('bad_response #%%@')

    output = self.custom_audience.get(
        name=_TEST_NAME,
        owner_app_package=_TEST_INSTALLED_OWNER_PACKAGE,
        buyer=_TEST_BUYER,
    )

    self.assertStartsWith(output, custom_audience.ERROR_FAILED_TO_PARSE)

  def test_refresh_happy_path(self):
    self.adb.set_shell_outputs([
        json.dumps(_GET_AUDIENCE_RESPONSE),
        json.dumps(_REFRESH_AUDIENCE_RESPONSE),
        json.dumps(_GET_AUDIENCE_RESPONSE_MODIFIED),
    ])

    diffed_json = json.loads(
        self.custom_audience.refresh(
            name=_TEST_NAME,
            owner_app_package=_TEST_INSTALLED_OWNER_PACKAGE,
            buyer=_TEST_BUYER,
        )
    )
    self.assertEqual(diffed_json, _REFRESH_COM_EXPECTED_OUTPUT)
    parts = utilities.split_adb_command(custom_audience._COMMAND_PREFIX) + [
        custom_audience._ARG_OWNER,
        _TEST_INSTALLED_OWNER_PACKAGE,
        custom_audience._ARG_BUYER,
        _TEST_BUYER,
        custom_audience._ARG_NAME,
        _TEST_NAME,
    ]
    self.assertContainsSubset(
        parts + [custom_audience._GET_COMMAND],
        self.adb.shell_calls[0],
    )
    self.assertContainsSubset(
        parts + [custom_audience._REFRESH_COMMAND],
        self.adb.shell_calls[1],
    )
    self.assertContainsSubset(
        parts + [custom_audience._GET_COMMAND],
        self.adb.shell_calls[2],
    )


if __name__ == '__main__':
  absltest.main()
