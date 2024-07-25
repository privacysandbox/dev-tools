# AdServices CLI

This directory contains a tool for interacting with the `adservices` module on
Android.

## Getting started

### Workstation setup

1.  Install dependencies with `pip3 install -r requirements.txt`
2.  Optionally add `alias=path/to/main.py` to your .bashrc
3.  Run `python3 main.py` to see the help screen

### Enable adservices shell commands

This tool interacts with the device by using low-level ADB commands part of the
`adservices` module. These commands need to be explicitly enabled.

1.  Restart your device to kill the adservices process

2.  Confirm that adservices is not running:

```
adb shell ps -A | grep com.google.android.adservices.api
```

To enable adservices shell commands, run the following command:

```
python3 main.py enable
```

If you interact with `adservices` before running `enable` then the flags will be
set into a disabled state until you reboot your device.

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
python3 main.py custom-audience list
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
python3 main.py custom-audience refresh
  --name <name> \
  --owner-app-package <package> \
  --buyer <buyer>
```

This command will show you a diff of the custom audience from before and after
the refresh.
