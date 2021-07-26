import os
from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko import netmiko_send_command


PASSWORD = os.environ.get("NORNIR_PASSWORD", "bogus")


def main():
    nr = InitNornir(config_file="config_serial.yaml")
    nr = nr.filter(F(groups__contains="nxos"))
    for hostname, host_obj in nr.inventory.hosts.items():
        host_obj.password = PASSWORD

    nr.run(task=netmiko_send_command, command_string="show mac address-table")


if __name__ == "__main__":
    main()
