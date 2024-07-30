"""AdServices kill swicthes and flag constants."""

## AdServices Kill switches
_GLOBAL_KILL_SWITCH = "global_kill_switch"
_CUSTOM_AUDIENCE_KILL_SWITCH = "fledge_custom_audience_service_kill_switch"
_SELECT_ADS_KILL_SWITCH = "fledge_select_ads_kill_switch"
_AD_ID_KILL_SWITCH = "adid_kill_switch"
_SERVER_AUCTIONS_KILL_SWITCH = "fledge_auction_server_kill_switch"
KILL_SWITCHES = [
    _GLOBAL_KILL_SWITCH,
    _CUSTOM_AUDIENCE_KILL_SWITCH,
    _SELECT_ADS_KILL_SWITCH,
    _AD_ID_KILL_SWITCH,
    _SERVER_AUCTIONS_KILL_SWITCH,
]

## AdServices feature flags
### AdServices
_ENABLE_ADSERVICES_SYSTEM_SERVICE = "adservice_system_service_enabled"
### Custom audience
_ENABLE_APP_INSTALL_FILTER = "fledge_app_install_filtering_enabled"
_ENABLE_FREQUENCEY_FILTER = "fledge_frequency_cap_filtering_enabled"
_ENABLE_AD_RENDER_ID = "fledge_auction_server_ad_render_id_enabled"

### Protected app signals
_ENABLE_PROTECTED_APP_SIGNALS = "protected_signals_enabled"
_ENABLE_PROTECTED_APP_SIGNALS_ENCODING = (
    "protected_signals_periodic_encoding_enabled"
)

### Reporting
_ENABLE_REPORT_EVENT_REGISTRATION = "fledge_register_ad_beacon_enabled"

FEATURE_FLAGS = [
    _ENABLE_ADSERVICES_SYSTEM_SERVICE,
    _ENABLE_APP_INSTALL_FILTER,
    _ENABLE_AD_RENDER_ID,
    _ENABLE_FREQUENCEY_FILTER,
    _ENABLE_PROTECTED_APP_SIGNALS,
    _ENABLE_PROTECTED_APP_SIGNALS_ENCODING,
    _ENABLE_REPORT_EVENT_REGISTRATION,
]

## AdServices debug flags
_DISABLE_FLEDGE_ENROLLMENT_CHECK = "disable_fledge_enrollment_check"
_CONSENT_MANAGER_DEBUG_MODE = "consent_manager_debug_mode"
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

DEBUG_FLAGS = [
    _DISABLE_FLEDGE_ENROLLMENT_CHECK,
    _CONSENT_MANAGER_DEBUG_MODE,
    _ENABLE_ADSERVICES_SHELL,
    _ENABLE_AD_SELECTION_CLI,
    _ENABLE_CONSENTED_DEBUGGING,
    _ENABLE_SERVER_AUCTION_CONSENTED_DEBUGGING,
    _ENABLE_JS_COLSOLE_LOGS,
    _ENABLE_CUSTOM_AUDIENCE_CLI,
    _ENABLE_PROTECTED_APP_SIGNALS_CLI,
]

# AdServices allow lists
_PP_API_ALLOW_LIST = "ppapi_app_allow_list"
_PAS_API_ALLOW_LIST = "pas_app_allow_list"
ALLOW_LISTS = [_PP_API_ALLOW_LIST, _PAS_API_ALLOW_LIST]
