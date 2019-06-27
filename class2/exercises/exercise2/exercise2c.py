import os
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks.networking import netmiko_send_command


def main():
    nr = InitNornir(config_file="config.yaml")
    filt = F(groups__contains="ios")
    nr = nr.filter(filt)
    my_results = nr.run(
        task=netmiko_send_command, command_string="show run | i hostname"
    )
    host_results = my_results["cisco3"]

    print()
    print(nr.inventory.hosts)
    print(type(host_results))
    print(host_results[0])
    print(host_results.__iter__)
    print()


if __name__ == "__main__":
    main()
