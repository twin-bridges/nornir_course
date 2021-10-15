import ipdb  # noqa
from rich import print
from nornir import InitNornir
from nornir_netmiko import netmiko_send_command
from nornir.core.filter import F

nr = InitNornir(config_file="config.yaml")
# ipdb.set_trace()
ios = nr.filter(F(groups__contains="ios"))
results = ios.run(
    task=netmiko_send_command, command_string="show ip int brief", use_textfsm=True
)

print()
print(results["cisco3"][0].result)
print()
