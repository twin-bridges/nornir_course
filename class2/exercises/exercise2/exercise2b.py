from rich import print
from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko import netmiko_send_command


def main():
    nr = InitNornir(config_file="config.yaml")
    filt = F(groups__contains="ios")
    nr = nr.filter(filt)
    my_results = nr.run(
        task=netmiko_send_command, command_string="show run | i hostname"
    )

    print()
    print(nr.inventory.hosts)
    print()
    print(f"my_results type: {type(my_results)}\n")
    print(f"items() method: {my_results.items()}\n")
    print(f"keys() method: {my_results.keys()}\n")
    print(f"values() method: {my_results.values()}\n")
    print()


if __name__ == "__main__":
    main()
