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

# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bidding_auction_servers.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x1d\x62idding_auction_servers.proto\x12<com.android.adservices.service.proto.bidding_auction_servers"\xaf\x03\n\x15ProtectedAuctionInput\x12x\n\x0b\x62uyer_input\x18\x01'
    b' \x03(\x0b\x32\x63.com.android.adservices.service.proto.bidding_auction_servers.ProtectedAuctionInput.BuyerInputEntry\x12\x16\n\x0epublisher_name\x18\x02'
    b' \x01(\t\x12\x1e\n\x16\x65nable_debug_reporting\x18\x03'
    b' \x01(\x08\x12\x15\n\rgeneration_id\x18\x04'
    b' \x01(\t\x12y\n\x16\x63onsented_debug_config\x18\x05'
    b' \x01(\x0b\x32Y.com.android.adservices.service.proto.bidding_auction_servers.ConsentedDebugConfiguration\x12\x1f\n\x17\x65nable_unlimited_egress\x18\x06'
    b' \x01(\x08\x1a\x31\n\x0f\x42uyerInputEntry\x12\x0b\n\x03key\x18\x01'
    b' \x01(\t\x12\r\n\x05value\x18\x02'
    b' \x01(\x0c:\x02\x38\x01"L\n\x13ProtectedAppSignals\x12\x1b\n\x13\x61pp_install_signals\x18\x01'
    b' \x01(\x0c\x12\x18\n\x10\x65ncoding_version\x18\x02'
    b' \x01(\x05"\x89\x04\n\nBuyerInput\x12o\n\x0finterest_groups\x18\x01'
    b' \x03(\x0b\x32V.com.android.adservices.service.proto.bidding_auction_servers.BuyerInput.InterestGroup\x12p\n\x15protected_app_signals\x18\x02'
    b' \x01(\x0b\x32Q.com.android.adservices.service.proto.bidding_auction_servers.ProtectedAppSignals\x1a\x97\x02\n\rInterestGroup\x12\x0c\n\x04name\x18\x01'
    b' \x01(\t\x12\x0e\n\x06origin\x18\x08'
    b' \x01(\t\x12\x1c\n\x14\x62idding_signals_keys\x18\x02'
    b' \x03(\t\x12\x15\n\rad_render_ids\x18\x03'
    b' \x03(\t\x12\x15\n\rcomponent_ads\x18\x04'
    b' \x03(\t\x12\x1c\n\x14user_bidding_signals\x18\x05'
    b' \x01(\t\x12g\n\x0f\x61ndroid_signals\x18\x06'
    b' \x01(\x0b\x32L.com.android.adservices.service.proto.bidding_auction_servers.AndroidSignalsH\x00\x42\x0f\n\rDeviceSignalsJ\x04\x08\x07\x10\x08"\x10\n\x0e\x41ndroidSignals"\xff\x08\n\rAuctionResult\x12\x15\n\rad_render_url\x18\x01'
    b' \x01(\t\x12 \n\x18\x61\x64_component_render_urls\x18\x02'
    b' \x03(\t\x12\x1b\n\x13interest_group_name\x18\x03'
    b' \x01(\t\x12\x1d\n\x15interest_group_origin\x18\r'
    b' \x01(\t\x12\x1c\n\x14interest_group_owner\x18\x04'
    b' \x01(\t\x12\r\n\x05score\x18\x05 \x01(\x02\x12\x0b\n\x03\x62id\x18\x06'
    b' \x01(\x02\x12\x10\n\x08is_chaff\x18\x07'
    b' \x01(\x08\x12j\n\x12win_reporting_urls\x18\x08'
    b' \x01(\x0b\x32N.com.android.adservices.service.proto.bidding_auction_servers.WinReportingUrls\x12n\n\x17\x62uyer_debug_report_urls\x18\t'
    b' \x01(\x0b\x32M.com.android.adservices.service.proto.bidding_auction_servers.DebugReportUrls\x12o\n\x18seller_debug_report_urls\x18\n'
    b' \x01(\x0b\x32M.com.android.adservices.service.proto.bidding_auction_servers.DebugReportUrls\x12v\n\x0e\x62idding_groups\x18\x0b'
    b' \x03(\x0b\x32^.com.android.adservices.service.proto.bidding_auction_servers.AuctionResult.BiddingGroupsEntry\x12`\n\x05\x65rror\x18\x0c'
    b' \x01(\x0b\x32Q.com.android.adservices.service.proto.bidding_auction_servers.AuctionResult.Error\x12\x63\n\x07\x61\x64_type\x18\x0e'
    b' \x01(\x0e\x32R.com.android.adservices.service.proto.bidding_auction_servers.AuctionResult.AdType\x1a#\n\x12InterestGroupIndex\x12\r\n\x05index\x18\x01'
    b' \x03(\x05\x1a\x94\x01\n\x12\x42iddingGroupsEntry\x12\x0b\n\x03key\x18\x01'
    b' \x01(\t\x12m\n\x05value\x18\x02'
    b' \x01(\x0b\x32^.com.android.adservices.service.proto.bidding_auction_servers.AuctionResult.InterestGroupIndex:\x02\x38\x01\x1a&\n\x05\x45rror\x12\x0c\n\x04\x63ode\x18\x01'
    b' \x01(\x05\x12\x0f\n\x07message\x18\x02'
    b' \x01(\t"=\n\x06\x41\x64Type\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x12\n\x0eREMARKETING_AD\x10\x01\x12\x12\n\x0e\x41PP_INSTALL_AD\x10\x02"\xa9\x05\n\x10WinReportingUrls\x12z\n\x14\x62uyer_reporting_urls\x18\x01'
    b' \x01(\x0b\x32\\.com.android.adservices.service.proto.bidding_auction_servers.WinReportingUrls.ReportingUrls\x12\x85\x01\n\x1f\x63omponent_seller_reporting_urls\x18\x02'
    b' \x01(\x0b\x32\\.com.android.adservices.service.proto.bidding_auction_servers.WinReportingUrls.ReportingUrls\x12\x85\x01\n\x1ftop_level_seller_reporting_urls\x18\x03'
    b' \x01(\x0b\x32\\.com.android.adservices.service.proto.bidding_auction_servers.WinReportingUrls.ReportingUrls\x1a\x88\x02\n\rReportingUrls\x12\x15\n\rreporting_url\x18\x01'
    b' \x01(\t\x12\x9e\x01\n\x1ainteraction_reporting_urls\x18\x02'
    b' \x03(\x0b\x32z.com.android.adservices.service.proto.bidding_auction_servers.WinReportingUrls.ReportingUrls.InteractionReportingUrlsEntry\x1a?\n\x1dInteractionReportingUrlsEntry\x12\x0b\n\x03key\x18\x01'
    b' \x01(\t\x12\r\n\x05value\x18\x02'
    b' \x01(\t:\x02\x38\x01"P\n\x0f\x44\x65\x62ugReportUrls\x12\x1d\n\x15\x61uction_debug_win_url\x18\x01'
    b' \x01(\t\x12\x1e\n\x16\x61uction_debug_loss_url\x18\x02'
    b' \x01(\t"e\n\x1b\x43onsentedDebugConfiguration\x12\x14\n\x0cis_consented\x18\x01'
    b' \x01(\x08\x12\r\n\x05token\x18\x02'
    b' \x01(\t\x12!\n\x19is_debug_info_in_response\x18\x03'
    b' \x01(\x08"<\n\nLogContext\x12\x15\n\rgeneration_id\x18\x01'
    b' \x01(\t\x12\x17\n\x0f\x61\x64tech_debug_id\x18\x02'
    b' \x01(\t"d\n!ContextualProtectedAppSignalsData\x12\x15\n\rad_render_ids\x18\x01'
    b' \x03(\t\x12(\n fetch_ads_from_retrieval_service\x18\x02'
    b' \x01(\x08"\xa2\x02\n\x1dProtectedAppSignalsBuyerInput\x12p\n\x15protected_app_signals\x18\x01'
    b' \x01(\x0b\x32Q.com.android.adservices.service.proto.bidding_auction_servers.ProtectedAppSignals\x12\x8e\x01\n%contextual_protected_app_signals_data\x18\x02'
    b' \x01(\x0b\x32_.com.android.adservices.service.proto.bidding_auction_servers.ContextualProtectedAppSignalsData"\x84\x07\n\x0eGetBidsRequest\x12\x1a\n\x12request_ciphertext\x18\x01'
    b' \x01(\x0c\x12\x0e\n\x06key_id\x18\x02'
    b' \x01(\t\x1a\xc5\x06\n\x11GetBidsRawRequest\x12\x10\n\x08is_chaff\x18\x01'
    b' \x01(\x08\x12]\n\x0b\x62uyer_input\x18\x02'
    b' \x01(\x0b\x32H.com.android.adservices.service.proto.bidding_auction_servers.BuyerInput\x12\x17\n\x0f\x61uction_signals\x18\x03'
    b' \x01(\t\x12\x15\n\rbuyer_signals\x18\x04'
    b' \x01(\t\x12\x0e\n\x06seller\x18\x05'
    b' \x01(\t\x12\x16\n\x0epublisher_name\x18\x06'
    b' \x01(\t\x12\x1e\n\x16\x65nable_debug_reporting\x18\x07'
    b' \x01(\x08\x12]\n\x0blog_context\x18\x08'
    b' \x01(\x0b\x32H.com.android.adservices.service.proto.bidding_auction_servers.LogContext\x12y\n\x16\x63onsented_debug_config\x18\t'
    b' \x01(\x0b\x32Y.com.android.adservices.service.proto.bidding_auction_servers.ConsentedDebugConfiguration\x12\x86\x01\n!protected_app_signals_buyer_input\x18\n'
    b' \x01(\x0b\x32[.com.android.adservices.service.proto.bidding_auction_servers.ProtectedAppSignalsBuyerInput\x12]\n\x0b\x63lient_type\x18\x0b'
    b' \x01(\x0e\x32H.com.android.adservices.service.proto.bidding_auction_servers.ClientType\x12\x18\n\x10top_level_seller\x18\x0c'
    b' \x01(\t\x12)\n\x1c\x62uyer_kv_experiment_group_id\x18\r'
    b' \x01(\x05H\x00\x88\x01\x01\x12\x1f\n\x17\x65nable_unlimited_egress\x18\x0e'
    b' \x01(\x08\x42\x1f\n\x1d_buyer_kv_experiment_group_id*W\n\nClientType\x12\x17\n\x13\x43LIENT_TYPE_UNKNOWN\x10\x00\x12\x17\n\x13\x43LIENT_TYPE_ANDROID\x10\x01\x12\x17\n\x13\x43LIENT_TYPE_BROWSER\x10\x02\x62\x06proto3'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR, 'bidding_auction_servers_pb2', globals()
)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _PROTECTEDAUCTIONINPUT_BUYERINPUTENTRY._options = None
  _PROTECTEDAUCTIONINPUT_BUYERINPUTENTRY._serialized_options = b'8\001'
  _AUCTIONRESULT_BIDDINGGROUPSENTRY._options = None
  _AUCTIONRESULT_BIDDINGGROUPSENTRY._serialized_options = b'8\001'
  _WINREPORTINGURLS_REPORTINGURLS_INTERACTIONREPORTINGURLSENTRY._options = None
  _WINREPORTINGURLS_REPORTINGURLS_INTERACTIONREPORTINGURLSENTRY._serialized_options = (
      b'8\001'
  )
  _CLIENTTYPE._serialized_start = 4532
  _CLIENTTYPE._serialized_end = 4619
  _PROTECTEDAUCTIONINPUT._serialized_start = 96
  _PROTECTEDAUCTIONINPUT._serialized_end = 527
  _PROTECTEDAUCTIONINPUT_BUYERINPUTENTRY._serialized_start = 478
  _PROTECTEDAUCTIONINPUT_BUYERINPUTENTRY._serialized_end = 527
  _PROTECTEDAPPSIGNALS._serialized_start = 529
  _PROTECTEDAPPSIGNALS._serialized_end = 605
  _BUYERINPUT._serialized_start = 608
  _BUYERINPUT._serialized_end = 1129
  _BUYERINPUT_INTERESTGROUP._serialized_start = 850
  _BUYERINPUT_INTERESTGROUP._serialized_end = 1129
  _ANDROIDSIGNALS._serialized_start = 1131
  _ANDROIDSIGNALS._serialized_end = 1147
  _AUCTIONRESULT._serialized_start = 1150
  _AUCTIONRESULT._serialized_end = 2301
  _AUCTIONRESULT_INTERESTGROUPINDEX._serialized_start = 2012
  _AUCTIONRESULT_INTERESTGROUPINDEX._serialized_end = 2047
  _AUCTIONRESULT_BIDDINGGROUPSENTRY._serialized_start = 2050
  _AUCTIONRESULT_BIDDINGGROUPSENTRY._serialized_end = 2198
  _AUCTIONRESULT_ERROR._serialized_start = 2200
  _AUCTIONRESULT_ERROR._serialized_end = 2238
  _AUCTIONRESULT_ADTYPE._serialized_start = 2240
  _AUCTIONRESULT_ADTYPE._serialized_end = 2301
  _WINREPORTINGURLS._serialized_start = 2304
  _WINREPORTINGURLS._serialized_end = 2985
  _WINREPORTINGURLS_REPORTINGURLS._serialized_start = 2721
  _WINREPORTINGURLS_REPORTINGURLS._serialized_end = 2985
  _WINREPORTINGURLS_REPORTINGURLS_INTERACTIONREPORTINGURLSENTRY._serialized_start = (
      2922
  )
  _WINREPORTINGURLS_REPORTINGURLS_INTERACTIONREPORTINGURLSENTRY._serialized_end = (
      2985
  )
  _DEBUGREPORTURLS._serialized_start = 2987
  _DEBUGREPORTURLS._serialized_end = 3067
  _CONSENTEDDEBUGCONFIGURATION._serialized_start = 3069
  _CONSENTEDDEBUGCONFIGURATION._serialized_end = 3170
  _LOGCONTEXT._serialized_start = 3172
  _LOGCONTEXT._serialized_end = 3232
  _CONTEXTUALPROTECTEDAPPSIGNALSDATA._serialized_start = 3234
  _CONTEXTUALPROTECTEDAPPSIGNALSDATA._serialized_end = 3334
  _PROTECTEDAPPSIGNALSBUYERINPUT._serialized_start = 3337
  _PROTECTEDAPPSIGNALSBUYERINPUT._serialized_end = 3627
  _GETBIDSREQUEST._serialized_start = 3630
  _GETBIDSREQUEST._serialized_end = 4530
  _GETBIDSREQUEST_GETBIDSRAWREQUEST._serialized_start = 3693
  _GETBIDSREQUEST_GETBIDSRAWREQUEST._serialized_end = 4530
# @@protoc_insertion_point(module_scope)