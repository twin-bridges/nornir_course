import os
from nornir import InitNornir
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="nornir.yaml")

# Code so automated tests will run properly
passwd_secret = os.environ["NORNIR_PASSWORD"]
nr.inventory.groups["cisco"].password = passwd_secret
nr.inventory.groups["cisco"].connection_options["netmiko"].extras[
    "secret"
] = passwd_secret

results = nr.run(task=netmiko_send_command, command_string="show run", enable=True)
print_result(results)
