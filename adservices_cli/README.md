# AdServices CLI

This directory contains a tool for interacting with the `adservices` module on
Android.

## Getting started

### Workstation setup

1.  Install dependencies with `pip3 install -r requirements.txt`
2.  Optionally add `alias=path/to/main.py` to your .bashrc
3.  Run `python3 main.py` to see the help screen

### Enable adservices features

This tool interacts with the device by using low-level ADB commands part of the
`adservices` module. These commands need to be explicitly enabled.

1.  Restart your device to kill the adservices process

2.  Confirm that adservices is not running:

```
adb shell ps -A | grep com.google.android.adservices.api
```

To enable a specific adservices feature, run the following command:

```
python3 main.py enable --feature-name <feature_name>
```

Allowed list of feature names is

*   **custom-audience** Enables all feature flags related to custom audience
    APIs.
*   **app-signals** Enables all feature flags related to protected app signals
    APIs.
*   **on-device-auction** Enables all feature flags related to on device auction
    APIs with bidding javascript version as 2.
*   **on-device-auction-v3** Enables all feature flags related to on device
    auctions APIs with bidding javascript version as 3.
*   **server-auction** Enables all feature flags related to APIs for protected
    auction on bidding and auction server.
*   **reporting** Enables all feature flags related to report impression and
    report event APIs.
*   **kanon** Enables all feature flags related to k-anonymity sing and join
    functionality.
*   **all** Enables all the above features.

If you interact with `adservices` before running `enable` then the flags will be
set into a disabled state until you reboot your device.

To disable a specific adservices feature, run the following command:

```
python3 main.py disable --feature-name <feature_name>
```

To check the current status of adservices process and features flags run the
following command:

```
python3 main.py status
```

## Inspecting custom audiences

**Note**: This documentation mirrors the low-level ADB command documentation
available in the Privacy Sandbox docs. The CLI in this repo is the recommended
way to interact with your device during testing.

The `custom_audience` command allows you to interact with custom audiences
created through the Protected Audience API on Android.

For security and privacy reasons, custom audiences are not visible by default,
and can only be directly inspected for debugging purposes. They are only visible
via these commands if the following requirements are true:

*   System-wide developer options are enabled

*   `android:debuggable=”true”` is declared in the `AndroidManifest.xml` file of
    the app where the `CusotmAudience` was joined from (using
    `joinCustomAudience` or `fetchAndJoinCustomAudience`)

*   Consent for app-suggested ads is toggled on

## List custom audiences

To view a specific custom audience, run the following command:

```
python3 main.py custom-audience list \
  --owner-app-package <package> \
  --buyer <buyer>
```

The output will be a JSON object containing an array custom_audiences. The
structure of the elements within this array match the output of the view custom
audience command (see below).

## View a specific custom audience

To view a specific custom audience, run the following command:

```
python3 main.py custom-audience get \
  --name <name> \
  --owner-app-package <package> \
  --buyer <buyer>
```

## Refresh a custom audience

To trigger daily update manually for a specific custom audience, run the
following command:

```
python3 main.py custom-audience refresh \
  --name <name> \
  --owner-app-package <package> \
  --buyer <buyer>
```

This command will show you a diff of the custom audience from before and after
the refresh.

## AdTech consented debugging

AdTech consented debugging enables AdTechs to debug Protected Audiences APIs on
Bidding and Auction Servers. More detail on how to setup AdTech consented
debugging on B&A servers please refer to
[this link](https://github.com/privacysandbox/protected-auction-services-docs/blob/main/debugging_protected_audience_api_services.md#adtech-consented-debugging).

### Enable AdTech consented debugging

To enable AdTech consented debugging on this device run the following command.

```
python3 main.py ad-selection enable-consented-debug \
    --token <secret-debug-token> \
    --expiry_in_hours <expiry in hours>
```

### Disable AdTech consented debugging

To disable AdTech consented debugging on this device run the following command.

```
python3 main.py ad-selection disable-consented-debug
```

### View AdTech consented debugging

To view AdTech consented debugging information on this device run the following
command.

```
python3 main.py ad-selection view-consented-debug
```

## Protected App Signals

### Trigger encoding for all buyers on the device.

To trigger the encoding logic for all buyers on the device, run the following
command:

```
python3 main.py app-signals trigger-encoding
```

## Ad Selection

### Get Ad Selection Data for a buyer.

This command provides plaintext output on the console which can be used to test
the GetBids request on Buyer FrontEnd service of Bidding and Auction
architecture using the
[Secure Invoke tool](https://github.com/privacysandbox/bidding-auction-servers/blob/main/tools/secure_invoke/README.md)

To generate the output run the following command:

```
python3 main.py ad-selection get-ad-selection-data \
  --buyer <buyer>
```
