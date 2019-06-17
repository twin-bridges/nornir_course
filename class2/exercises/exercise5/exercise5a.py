import os
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command


def main():
    nr = InitNornir(config_file="config.yaml", core={"num_workers": 15})
    # Avoid storing lab password in GitHub, pull from environment variable
    nr.inventory.defaults.password = os.environ["NORNIR_PASSWORD"]
    # Set cisco3 password to environment variable -- leave hosts file with incorrect password
    # This is to ensure tests for exercise5a complete successfully
    nr.inventory.hosts["cisco3"].password = os.environ["NORNIR_PASSWORD"]
    ios_filt = F(groups__contains="ios")
    nr = nr.filter(ios_filt)
    my_results = nr.run(task=netmiko_send_command, command_string="show ip int brief")
    print_result(my_results)


if __name__ == "__main__":
    main()
