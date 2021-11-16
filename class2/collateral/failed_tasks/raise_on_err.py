import os
import pdbr  # noqa
from nornir import InitNornir
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.functions import print_result


def main():
    nr = InitNornir(config_file="config.yaml")
    # Code so automated tests will run properly
    nr.inventory.groups["cisco"].password = os.environ["NORNIR_PASSWORD"]

    result = nr.run(task=netmiko_send_command, command_string="show run | i pid")
    print_result(result)
    # pdbr.set_trace()
    result = nr.run(
        task=netmiko_send_command,
        # on_failed=True,
        command_string="show run | i hostname",
    )
    print_result(result)


if __name__ == "__main__":
    main()
