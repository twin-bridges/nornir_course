from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.core.filter import F
from pprint import pprint
import ipdb

nr = InitNornir(config_file="config.yaml")
ipdb.set_trace()
ios = nr.filter(F(groups__contains="ios"))
results = ios.run(
    task=netmiko_send_command, command_string="show ip int brief", use_textfsm=True
)

print()
pprint(results["cisco3"][0].result)
print()
