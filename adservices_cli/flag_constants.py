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

"""AdServices kill swicthes and flag constants."""

## AdServices Kill switches
_GLOBAL_KILL_SWITCH = "global_kill_switch"
_CUSTOM_AUDIENCE_KILL_SWITCH = "fledge_custom_audience_service_kill_switch"
_SELECT_ADS_KILL_SWITCH = "fledge_select_ads_kill_switch"
_AD_ID_KILL_SWITCH = "adid_kill_switch"
_AUCTION_SERVER_KILL_SWITCH = "fledge_auction_server_kill_switch"
_ON_DEVICE_AUCTION_KILL_SWITCH = "fledge_on_device_auction_kill_switch"
KILL_SWITCHES = [
    _GLOBAL_KILL_SWITCH,
    _CUSTOM_AUDIENCE_KILL_SWITCH,
    _SELECT_ADS_KILL_SWITCH,
    _AD_ID_KILL_SWITCH,
    _AUCTION_SERVER_KILL_SWITCH,
    _ON_DEVICE_AUCTION_KILL_SWITCH,
]

## AdServices feature names
CUSTOM_AUDIENCE = "custom-audience"
APP_SIGNALS = "app-signals"
ON_DEVICE_AUCTION = "on-device-auction"
SERVER_AUCTION = "server-auction"
REPORTING = "reporting"
KANON = "kanon"
ON_DEVICE_AUCTION_V3 = "on-device-auction-v3"

FEATURE_ALL = "all"
FEATURE_NAMES = [
    CUSTOM_AUDIENCE,
    APP_SIGNALS,
    ON_DEVICE_AUCTION,
    SERVER_AUCTION,
    REPORTING,
    KANON,
    ON_DEVICE_AUCTION_V3,
]
## AdServices feature flags
### AdServices
_ENABLE_ADSERVICES_SYSTEM_SERVICE = "adservice_system_service_enabled"

ENABLE_DEFAULT_FLAGS = [_ENABLE_ADSERVICES_SYSTEM_SERVICE]

### Custom audience
_ENABLE_APP_INSTALL_FILTER = "fledge_app_install_filtering_enabled"
_ENABLE_FREQUENCEY_FILTER = "fledge_frequency_cap_filtering_enabled"
_ENABLE_FETCH_CUSTOM_AUDIENCE = "fledge_fetch_custom_audience_enabled"
_ENABLE_SCHEDULE_CUSTOM_AUDIENCE_UPDATE = (
    "fledge_schedule_custom_audience_update_enabled"
)
_ENABLE_SCHEDULE_CUSTOM_AUDIENCE_UPDATE_ADDITIONAL_SCHEDULE_REQUESTS = (
    "fledge_enable_schedule_custom_audience_update_additional_schedule_requests"
)

ENABLE_ALL_CUSTOM_AUDIENCE_FEATURE_FLAGS = [
    _ENABLE_APP_INSTALL_FILTER,
    _ENABLE_FREQUENCEY_FILTER,
    _ENABLE_FETCH_CUSTOM_AUDIENCE,
    _ENABLE_SCHEDULE_CUSTOM_AUDIENCE_UPDATE,
    _ENABLE_SCHEDULE_CUSTOM_AUDIENCE_UPDATE_ADDITIONAL_SCHEDULE_REQUESTS,
]

### On Device Auction
AD_SELECTION_BIDDING_LOGIC_V3 = "fledge_ad_selection_bidding_logic_js_version"
_ENABLE_AD_SELECTION_PREBUILT_URI = (
    "fledge_ad_selection_ad_selection_prebuilt_uri_enabled"
)
_ENABLE_EVENT_LEVEL_DEBUG_REPORTING = (
    "fledge_event_level_debug_reporting_enabled"
)
_ENABLE_EVENT_LEVEL_DEBUG_REPORT_SEND_IMMEDIATELY = (
    "fledge_event_level_debug_report_send_immediately"
)
_ENABLE_CONTEXTUAL_ADS_FILTER = "fledge_ad_selection_contextual_ads_enabled"
_ENABLE_HTTP_CACHE_ENABLE_JS_CACHING = "fledge_http_cache_enable_js_caching"
ENABLE_ALL_ON_DEVICE_AD_SELECTION_FLAGS = [
    _ENABLE_AD_SELECTION_PREBUILT_URI,
    _ENABLE_EVENT_LEVEL_DEBUG_REPORTING,
    _ENABLE_EVENT_LEVEL_DEBUG_REPORT_SEND_IMMEDIATELY,
    _ENABLE_CONTEXTUAL_ADS_FILTER,
    _ENABLE_HTTP_CACHE_ENABLE_JS_CACHING,
]

### Server auctions
_ENABLE_AUCTION_SERVER = "fledge_auction_server_enabled"
_ENABLE_AUCTION_SERVER_FOR_REPORT_IMPRESSION = (
    "fledge_auction_server_enabled_for_report_impression"
)
_ENABLE_AUCTION_SERVER_FOR_REPORT_EVENT = (
    "fledge_auction_server_enabled_for_report_event"
)
_ENABLE_AUCTION_SERVER_FOR_UPDATE_HISTOGRAM = (
    "fledge_auction_server_enabled_for_update_histogram"
)
_ENABLE_AUCTION_SERVER_FOR_MEDIATION = (
    "fledge_auction_server_enabled_for_select_ads_mediation"
)
_ENABLE_AUCTION_SERVER_AD_RENDER_ID = (
    "fledge_auction_server_ad_render_id_enabled"
)
_ENABLE_AUCTION_SERVER_MULTI_CLOUD = "fledge_auction_server_multi_cloud_enabled"
_ENABLE_AUCTION_SERVER_OMIT_ADS = "fledge_auction_server_omit_ads_enabled"
_ENABLE_AUCTION_SERVER_REQUEST_FLAGS = (
    "fledge_auction_server_request_flags_enabled"
)
_ENABLE_AUCTION_SERVER_SELLER_CONFIGURATIONS = (
    "fledge_get_ad_selection_data_seller_configuration_enabled"
)

ENABLE_ALL_AUCTION_SERVER_FEATURE_FLAGS = [
    _ENABLE_AUCTION_SERVER,
    _ENABLE_AUCTION_SERVER_FOR_REPORT_IMPRESSION,
    _ENABLE_AUCTION_SERVER_FOR_REPORT_EVENT,
    _ENABLE_AUCTION_SERVER_FOR_UPDATE_HISTOGRAM,
    _ENABLE_AUCTION_SERVER_FOR_MEDIATION,
    _ENABLE_AUCTION_SERVER_AD_RENDER_ID,
    _ENABLE_AUCTION_SERVER_MULTI_CLOUD,
    _ENABLE_AUCTION_SERVER_OMIT_ADS,
    _ENABLE_AUCTION_SERVER_REQUEST_FLAGS,
    _ENABLE_AUCTION_SERVER_SELLER_CONFIGURATIONS,
]

### Protected app signals
_ENABLE_PROTECTED_APP_SIGNALS = "protected_signals_enabled"
_ENABLE_PROTECTED_APP_SIGNALS_ENCODING = (
    "protected_signals_periodic_encoding_enabled"
)

ENABLE_ALL_PROTECTED_APP_SIGNALS_FEATURE_FLAGS = [
    _ENABLE_PROTECTED_APP_SIGNALS,
    _ENABLE_PROTECTED_APP_SIGNALS_ENCODING,
]

### Reporting
_ENABLE_REPORT_EVENT_REGISTRATION = "fledge_register_ad_beacon_enabled"
_ENABLE_CPC_BILLING = "fledge_cpc_billing_enabled"
_ENABLE_DATA_VERSION_HEADER = "fledge_data_version_header_enabled"
_ENABLE_MEASUREMENT_REPORT_AND_REGISTER_EVENT_FOR_PA = (
    "fledge_measurement_report_and_register_event_api_enabled"
)

ENABLE_ALL_REPORTING_FEATURE_FLAGS = [
    _ENABLE_REPORT_EVENT_REGISTRATION,
    _ENABLE_CPC_BILLING,
    _ENABLE_DATA_VERSION_HEADER,
    _ENABLE_MEASUREMENT_REPORT_AND_REGISTER_EVENT_FOR_PA,
]

### KAnon
_ENABLE_KANON_SING_AND_JOIN = "fledge_kanon_sign_join_enabled"
_ENABLE_KANON_ON_DEVICE_AUCTION = (
    "fledge_kanon_sign_join_on_device_auction_enabled"
)
_ENABLE_KANON_AUCTION_SERVER = "fledge_kanon_sign_join_auction_server_enabled"
_ENABLE_KANON_BACKGROUND_PROCESS = "fledge_kanon_background_process_enabled"
_ENABLE_KANON_KEY_ATTESTATION = "fledge_kanon_key_attestation_enabled"

ENABLE_ALL_KANON_FEATURE_FLAGS = [
    _ENABLE_KANON_SING_AND_JOIN,
    _ENABLE_KANON_ON_DEVICE_AUCTION,
    _ENABLE_KANON_AUCTION_SERVER,
    _ENABLE_KANON_BACKGROUND_PROCESS,
    _ENABLE_KANON_KEY_ATTESTATION,
]

FEATURE_FLAGS_MAP = {
    CUSTOM_AUDIENCE: ENABLE_ALL_CUSTOM_AUDIENCE_FEATURE_FLAGS,
    APP_SIGNALS: ENABLE_ALL_PROTECTED_APP_SIGNALS_FEATURE_FLAGS,
    SERVER_AUCTION: ENABLE_ALL_AUCTION_SERVER_FEATURE_FLAGS,
    ON_DEVICE_AUCTION: ENABLE_ALL_ON_DEVICE_AD_SELECTION_FLAGS,
    REPORTING: ENABLE_ALL_REPORTING_FEATURE_FLAGS,
    KANON: ENABLE_ALL_KANON_FEATURE_FLAGS,
    ON_DEVICE_AUCTION_V3: ENABLE_ALL_ON_DEVICE_AD_SELECTION_FLAGS,
}

## AdServices debug flags
_DISABLE_FLEDGE_ENROLLMENT_CHECK = "disable_fledge_enrollment_check"
_CONSENT_MANAGER_DEBUG_MODE = "consent_manager_debug_mode"
_CONSENT_NOTIFICATION_DEBUG_MODE = "consent_notification_debug_mode"
_ENABLE_ADSERVICES_SHELL = "adservices_shell_command_enabled"
_ENABLE_CUSTOM_AUDIENCE_CLI = "fledge_is_custom_audience_cli_enabled"
_ENABLE_JS_COLSOLE_LOGS = (
    "ad_services_js_isolate_console_messages_in_logs_enabled"
)
_ENABLE_AD_SELECTION_CLI = "fledge_is_ad_selection_cli_enabled"
_ENABLE_CONSENTED_DEBUGGING = "fledge_is_consented_debugging_cli_enabled"
_ENABLE_SERVER_AUCTION_CONSENTED_DEBUGGING = (
    "fledge_auction_server_consented_debugging_enabled"
)
_ENABLE_PROTECTED_APP_SIGNALS_CLI = "fledge_is_app_signals_cli_enabled"
_ENABLE_MEASUREMENT_ATTRIBUTION_REPORTING_CLI = "measurement_attribution_reporting_cli_enabled"
_ENABLE_DEV_SESSION_FEATURE = "developer_session_feature_enabled"

DEBUG_FLAGS = [
    _DISABLE_FLEDGE_ENROLLMENT_CHECK,
    _CONSENT_MANAGER_DEBUG_MODE,
    _CONSENT_NOTIFICATION_DEBUG_MODE,
    _ENABLE_ADSERVICES_SHELL,
    _ENABLE_AD_SELECTION_CLI,
    _ENABLE_CONSENTED_DEBUGGING,
    _ENABLE_SERVER_AUCTION_CONSENTED_DEBUGGING,
    _ENABLE_JS_COLSOLE_LOGS,
    _ENABLE_CUSTOM_AUDIENCE_CLI,
    _ENABLE_PROTECTED_APP_SIGNALS_CLI,
    _ENABLE_MEASUREMENT_ATTRIBUTION_REPORTING_CLI,
    _ENABLE_DEV_SESSION_FEATURE,
]

# AdServices allow lists
_PP_API_ALLOW_LIST = "ppapi_app_allow_list"
_PAS_API_ALLOW_LIST = "pas_app_allow_list"
ALLOW_LISTS = [_PP_API_ALLOW_LIST, _PAS_API_ALLOW_LIST]

LOG_TAGS_FOR_VERBOSE_LOGGING = [
    "adservices",
    "adservices.fledge",
    "adservices.topics",
    "adservices.kanon",
    "adservices.measurement",
    "adservices.ui",
    "adservices.adid",
    "adservices.appsetid",
    "AdServicesShellCmd",
    "FledgeSample",
]
