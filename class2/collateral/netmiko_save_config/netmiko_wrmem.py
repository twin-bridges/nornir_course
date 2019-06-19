from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_save_config
from nornir.plugins.functions.text import print_result

nr = InitNornir(config_file="nornir.yaml")
results = nr.run(task=netmiko_save_config)

print_result(results)
