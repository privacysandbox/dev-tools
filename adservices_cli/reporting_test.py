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

import fake_adb
import reporting
import utilities


_TEST_REPORTING_NAME = 'test_reporting_name'
_TEST_REPORTING = {
    'name': _TEST_REPORTING_NAME,
    'field': 'test_data',
}

_LIST_REPORTING_RESPONSE = {'attribution_reporting': [_TEST_REPORTING]}
_LIST_REPORTING_RESPONSE_EMPTY = {'attribution_reporting': []}


class ReportingTest(absltest.TestCase):

  def setUp(self):
    super().setUp()
    self.adb = fake_adb.FakeAdb()
    self.reporting = reporting.Reporting(self.adb)

  def tearDown(self):
    super().tearDown()
    self.adb.reset()

  def test_list_source_registrations_reporting_happy_path(self):
    self.adb.set_shell_output(json.dumps(_LIST_REPORTING_RESPONSE))

    output = self.reporting.list_source_registrations()

    self.assertContainsSubset(
        utilities.split_adb_command(reporting._COMMAND_PREFIX)
        + [
            reporting._LIST_COMMAND
        ],
        self.adb.shell_calls[0],
    )
    self.assertEqual(json.loads(output), _LIST_REPORTING_RESPONSE)

  def test_list_source_registrations_audiences_empty_response(self):
    self.adb.set_shell_output(json.dumps(_LIST_REPORTING_RESPONSE_EMPTY))

    output = self.reporting.list_source_registrations()

    self.assertTrue(self.adb.shell_called)
    self.assertEqual(json.loads(output), _LIST_REPORTING_RESPONSE_EMPTY)

  def test_list_source_registrations_audiences_bad_adb_response(self):
    self.adb.set_shell_output('bad_response #%%@')

    output = self.reporting.list_source_registrations()

    self.assertTrue(self.adb.shell_called)
    self.assertStartsWith(output, reporting.ERROR_FAILED_TO_PARSE)

if __name__ == '__main__':
  absltest.main()
