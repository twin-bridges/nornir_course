from nornir import InitNornir

from nornir.core.inventory import ConnectionOptions
from nornir.plugins.tasks import networking
from nornir.plugins.functions.text import print_result

from copy import deepcopy


def transform_slog(host):
    """
    Create ConnectionOptions > Extras in the transform function.

    This pattern presupposes, however, that there is nothing else
    in existing inventory inside extras that needs retained.

    The five primary attributes would still get recursively retrieved
    including inside of connection options.
    """

    # Dynamically set the session_log to be unique per host
    filename = f"{host}-output.txt"
    host.connection_options["netmiko"] = ConnectionOptions(
        extras={"session_log": filename}
    )
    netmiko_params = host.get_connection_parameters("netmiko")
    print(netmiko_params)


def transform_slog2(host):
    """
    This pattern retrieves the entire set of connection parameters recursively.

    It then makes an update to extras.

    Finally, it re-assigns this updated set of connection parameters back at the
    host level.
    """

    # Dynamically set the session_log to be unique per host
    filename = f"{host}-output.txt"

    # Retrieve the current set of connection parameters recursively
    netmiko_params = host.get_connection_parameters("netmiko")

    # Dictionaries are mutable so we can run into issues with the dictionary
    # being shared across hosts (i.e. we grab the dict from the group-level
    # and then keep using it). Make a copy instead.
    extras = deepcopy(netmiko_params.extras)
    extras["session_log"] = filename
    netmiko_params.extras = extras

    # Re-assign the entire set of connection options back at the host-level
    host.connection_options["netmiko"] = netmiko_params


def main():
    nr = InitNornir(config_file="config.yaml")
    agg_result = nr.run(
        task=networking.netmiko_send_command, command_string="show version"
    )
    print_result(agg_result)


if __name__ == "__main__":
    main()
