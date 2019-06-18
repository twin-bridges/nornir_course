from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command

nr = InitNornir(config_file="nornir.yaml")
results = nr.run(task=netmiko_send_command, command_string="show ip int brief")

print()
for k, v in results.items():
    print("-" * 50)
    print(k)
    print(v[0].result)
    print("-" * 50)
print()
