import os
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command
from nornir_napalm.plugins.tasks import napalm_get


def main():
    nr = InitNornir(config_file="config.yaml", logging={"enabled": False})

    # Code so automated tests will run properly
    passwd_secret = os.environ["NORNIR_PASSWORD"]
    nr.inventory.groups["eos"].password = passwd_secret

    nr = nr.filter(name="arista4")

    netmiko_results = nr.run(task=netmiko_send_command, command_string="show ip arp")
    print_result(netmiko_results)
    netmiko_results = nr.run(
        task=netmiko_send_command, command_string="show run | i hostname", enable=True
    )
    print_result(netmiko_results)

    napalm_results = nr.run(task=napalm_get, getters=["interfaces"])
    print_result(napalm_results)


if __name__ == "__main__":
    main()
