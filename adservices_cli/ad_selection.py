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

"""Command for interacting with Protected Audience Ad Selection CLI Commands."""

import base64
import gzip
import json

from google.protobuf.json_format import MessageToJson
from google.protobuf.message import DecodeError

import adb
import bidding_auction_servers_pb2
import utilities

_COMMAND_PREFIX = "ad-selection"
_CONSENTED_DEBUG_COMMAND = "consented-debug"
_CONSENTED_DEBUG_COMMAND_ENABLE = "enable"
_CONSENTED_DEBUG_COMMAND_ENABLE_SECRET_DEBUG_TOKEN = "--secret-debug-token"
_CONSENTED_DEBUG_COMMAND_ENABLE_EXPIRY_IN_HOURS = "--expires-in-hours"
_CONSENTED_DEBUG_COMMAND_DISABLE = "disable"
_CONSENTED_DEBUG_COMMAND_VIEW = "view"
_FAILURE_TEMPLATE = "Failed to parse output: %s"
_GET_AD_SELECTION_DATA_COMMAND = "get-ad-selection-data"
_VIEW_AUCTION_RESULT_COMMAND = "view-auction-result"
_ARG_BUYER = "--buyer"
_ARG_AD_SELECTION_ID = "--ad-selection-id"


class AdSelection:
  """Interact with Ad Selection.

  Overview:
  https://developers.google.com/privacy-sandbox/relevance/protected-audience/android#ad-selection

  Bidding and Auction Servers Overview:
  https://developers.google.com/privacy-sandbox/relevance/protected-audience/android/bidding-and-auction-services
  """

  def __init__(
      self,
      adb_client: adb.AdbClient,
  ):
    self._adb = adb_client

  def view_consented_debug(self) -> str:
    """View adtech consented debugging information on the device.

    Returns:
      Textual output of consented debug view command.
    """
    view_output: str = self._adb.execute_adservices_shell_command(
        utilities.format_command(
            _COMMAND_PREFIX,
            _CONSENTED_DEBUG_COMMAND,
            _CONSENTED_DEBUG_COMMAND_VIEW,
            {},
        )
    )
    try:
      json_obj = json.loads(view_output)
      return json.dumps(json_obj, indent=4)
    except ValueError as unused_error:
      return view_output

  def enable_consented_debug(
      self,
      token: str,
      expiry_in_hours: int = 30 * 24,  # 30 days
  ) -> str:
    """Enable adtech consented debugging on the device.

    Args:
      token: Secret token which is also set on the TEE server.
      expiry_in_hours: Hours after which the consented debug will be disabled.

    Returns:
      Textual output of consented debug enable command.
    """

    enable_output: str = self._adb.execute_adservices_shell_command(
        utilities.format_command(
            _COMMAND_PREFIX,
            _CONSENTED_DEBUG_COMMAND,
            _CONSENTED_DEBUG_COMMAND_ENABLE,
            {
                _CONSENTED_DEBUG_COMMAND_ENABLE_SECRET_DEBUG_TOKEN: token,
                _CONSENTED_DEBUG_COMMAND_ENABLE_EXPIRY_IN_HOURS: (
                    expiry_in_hours
                ),
            },
        )
    )
    print(enable_output)
    return self.view_consented_debug()

  def disable_consented_debug(self) -> str:
    """Disable adtech consented debugging on the device.

    Returns:
      Textual output of consented debug disable command.
    """
    return self._adb.execute_adservices_shell_command(
        utilities.format_command(
            _COMMAND_PREFIX,
            _CONSENTED_DEBUG_COMMAND,
            _CONSENTED_DEBUG_COMMAND_DISABLE,
            {},
        )
    )

  def get_ad_selection_data(self, buyer: str = "") -> str:
    """Prints the JSON formatted input for usage with secure_invoke.

    Args:
      buyer: AdTech buyer used to generate the payload to a BuyerFrontend
        GetBids API. If omitted, then an "raw" SelectAdRequest will be returned
        for usage with an SellerFrontend SelectAds API. Note that this only
        works with secure_invoke.

    Returns:
      Textual output of get_ad_selection__data command.
    """
    command_output = self._adb.execute_adservices_shell_command(
        utilities.format_command(
            _COMMAND_PREFIX,
            _GET_AD_SELECTION_DATA_COMMAND,
            "",
            {_ARG_BUYER: buyer} if buyer else {},
        )
    )
    try:
      proto_json = json.loads(command_output.replace("\n", ""))
      base64_decoded_str = base64.b64decode(proto_json.get("output_proto"))
      if buyer:
        print("Querying for buyer: " + buyer)
        try:
          message = bidding_auction_servers_pb2.GetBidsRequest.GetBidsRawRequest.FromString(
              base64_decoded_str
          )
          return MessageToJson(message)
        except DecodeError as e:
          return _FAILURE_TEMPLATE % e
      else:
        print("Querying for seller")
        try:
          auction_input = (
              bidding_auction_servers_pb2.ProtectedAuctionInput.FromString(
                  base64_decoded_str
              )
          )
        except DecodeError as e:
          return _FAILURE_TEMPLATE % e
        decompressed_buyer_inputs = {}
        for buyer, compressed_buyer_input in auction_input.buyer_input.items():
          buyer_input_bytes = gzip.decompress(compressed_buyer_input)
          buyer_input = bidding_auction_servers_pb2.BuyerInput.FromString(
              buyer_input_bytes
          )
          interest_groups = []
          for interest_group in buyer_input.interest_groups:
            interest_groups.append({
                "name": interest_group.name,
                "origin": interest_group.origin,
                "bidding_signals_keys": list(
                    interest_group.bidding_signals_keys
                ),
                "ad_render_ids": list(interest_group.ad_render_ids),
                "component_ads": list(interest_group.component_ads),
                "user_bidding_signals": interest_group.user_bidding_signals,
            })
          raw_buyer_input = {
              "interest_groups": interest_groups,
          }
          if buyer_input.protected_app_signals.app_install_signals:
            raw_buyer_input["protected_app_signals"] = {
                "app_install_signals": base64.b64encode(
                    buyer_input.protected_app_signals.app_install_signals
                    or "{}"
                ).decode("utf-8"),
                "encoding_version": (
                    buyer_input.protected_app_signals.encoding_version
                ),
            }
          decompressed_buyer_inputs[buyer] = raw_buyer_input
        empty_per_buyer_config = {}
        for buyer in decompressed_buyer_inputs:
          empty_per_buyer_config[buyer] = {
              "buyer_signals": "Replace-With-Buyer-Signals",
              "auction_signals": "Replace-With-Auction-Signals",
          }
        return json.dumps({
            "auction_config": {
                "seller_signals": "Replace-With-Seller-Signals",
                "auction_signals": "Replace-With-Auction-Signals",
                "buyer_list": list(decompressed_buyer_inputs.keys()),
                "seller": "Replace-With-Seller",
                "per_buyer_config": empty_per_buyer_config,
            },
            "client_type": "CLIENT_TYPE_ANDROID",
            "raw_protected_audience_input": {
                "raw_buyer_input": decompressed_buyer_inputs,
                "publisher_name": auction_input.publisher_name,
                "enable_debug_reporting": auction_input.enable_debug_reporting,
                "generation_id": auction_input.generation_id,
                "consented_debug_config": {
                    "is_consented": (
                        auction_input.consented_debug_config.is_consented
                    ),
                    "token": auction_input.consented_debug_config.token,
                    "is_debug_info_in_response": (
                        auction_input.consented_debug_config.is_debug_info_in_response
                    ),
                },
            },
        })

    except ValueError as e:
      print("Failed to parse output: %s" % e)
      return command_output

  def view_auction_result(self, ad_selection_id: str) -> str:
    """View the result of an auction.

    Args:
      ad_selection_id: Identifier for the auction, sometimes called "Generation
        ID" in B&A terminology.

    Returns:
      Textual output of view_auction_result command.
    """
    command_output = self._adb.execute_adservices_shell_command(
        utilities.format_command(
            _COMMAND_PREFIX,
            _VIEW_AUCTION_RESULT_COMMAND,
            "",
            {_ARG_AD_SELECTION_ID: ad_selection_id},
        )
    )
    try:
      proto_json = json.loads(command_output)
      base64_decoded_str = base64.b64decode(proto_json.get("output_proto"))
      return MessageToJson(
          bidding_auction_servers_pb2.AuctionResult.FromString(
              base64_decoded_str
          )
      )
    except ValueError:
      return command_output
