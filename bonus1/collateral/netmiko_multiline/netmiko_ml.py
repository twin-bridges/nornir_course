from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result  # noqa
from nornir_netmiko import netmiko_multiline


if __name__ == "__main__":

    commands = [
        ("ping", "Protocol"),
        ("\n", "Target IP"),
        ("8.8.8.8", "Repeat count"),
        ("30", "Datagram size"),
        ("\n", "Timeout"),
        ("\n", "Extended commands"),
        ("\n", "Sweep range"),
        ("\n", "#"),
    ]

    # Use a context-manager so connections are gracefully closed
    with InitNornir(config_file="config.yaml") as nr:
        ios_filt = F(groups__contains="ios")
        nr_ios = nr.filter(ios_filt)
        result = nr_ios.run(task=netmiko_multiline, commands=commands)
        print_result(result)
