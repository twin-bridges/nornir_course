from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result  # noqa
from nornir_netmiko import netmiko_multiline


if __name__ == "__main__":

    commands = [
        "ping",
        "\n",
        "8.8.8.8",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
    ]

    # Use a context-manager so connections are gracefully closed
    with InitNornir(config_file="config.yaml") as nr:
        ios_filt = F(groups__contains="ios")
        nr_ios = nr.filter(ios_filt)
        result = nr_ios.run(task=netmiko_multiline, commands=commands, use_timing=True)
        print_result(result)
