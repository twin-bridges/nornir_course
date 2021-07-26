import os
from nornir import InitNornir
from nornir_netmiko import netmiko_save_config
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="nornir.yaml")

# Code so automated tests will run properly
nr.inventory.groups["cisco"].password = os.environ["NORNIR_PASSWORD"]

results = nr.run(task=netmiko_save_config)
print_result(results)
