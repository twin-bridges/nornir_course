import os
from getpass import getpass
from nornir import InitNornir
from nornir_netmiko import netmiko_send_command


# The environment variable is for automated testing (else use getpass())
SECRET = os.getenv("NORNIR_PASSWORD") if os.getenv("NORNIR_PASSWORD") else getpass()


def set_secret(nr, group):
    group = nr.inventory.groups[group]
    group.connection_options["netmiko"].extras["secret"] = SECRET


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="cisco3")

    set_secret(nr, "ios")
    agg_result = nr.run(
        task=netmiko_send_command, command_string="show run | i hostname", enable=True
    )
    print(agg_result["cisco3"].result)


if __name__ == "__main__":
    main()
