import os
from nornir import InitNornir
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="nornir.yaml")

# Code so automated tests will run properly
nr.inventory.groups["cisco"].password = os.environ["NORNIR_PASSWORD"]

results = nr.run(task=netmiko_send_command, command_string="show ip int brief")
print_result(results)
