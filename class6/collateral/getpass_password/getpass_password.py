import os
from getpass import getpass
from nornir import InitNornir
from nornir_netmiko import netmiko_send_command


# The environment variable is for automated testing (else use getpass())
PASSWORD = os.getenv("NORNIR_PASSWORD") if os.getenv("NORNIR_PASSWORD") else getpass()


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="arista1")
    for hostname, host_obj in nr.inventory.hosts.items():
        host_obj.password = PASSWORD
    agg_result = nr.run(
        task=netmiko_send_command, command_string="show run | i hostname"
    )
    print(agg_result["arista1"].result)


if __name__ == "__main__":
    main()
