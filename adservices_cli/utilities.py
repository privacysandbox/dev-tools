"""Common Utilities for executing AdServices CLI commands."""


def format_command(
    command_prefix: str,
    command_name: str,
    sub_command_name: str,
    args_dict: dict[str, str],
) -> str:
  """Formats a command to run on the device.

  Args:
    command_prefix: The command prefix.
    command_name: Raw command name to execute.
    sub_command_name: Sub command name to execute
    args_dict: arguments to be passed to the command.

  Returns:
    (str) formatted to run via ADB.
  """
  args = [command_prefix, command_name, sub_command_name]
  if not args_dict:
    return " ".join(args)
  for arg_name in args_dict:
    args.append(arg_name)
    args.append(args_dict.get(arg_name))
  return " ".join([str(elem) for elem in args])


def split_adb_command(command: str) -> list[str]:
  """Splits the provided command string.

  Args:
    command: the command separated by space.

  Returns:
   (list[str]) list of strings from the command.
  """
  return command.split(" ")
