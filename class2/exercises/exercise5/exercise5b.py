from rich import print
from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command


def main():
    nr = InitNornir(config_file="config.yaml")
    ios_filt = F(groups__contains="ios")
    nr = nr.filter(ios_filt)
    nr.inventory.hosts["cisco3"].password = "bogus"
    my_results = nr.run(task=netmiko_send_command, command_string="show ip int brief")
    print_result(my_results)
    print()
    print(f"Task failed hosts: {my_results.failed_hosts}")
    print(f"Global failed hosts: {nr.data.failed_hosts}")
    print()


if __name__ == "__main__":
    main()
