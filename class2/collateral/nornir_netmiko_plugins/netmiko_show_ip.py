from nornir import InitNornir
from nornir_netmiko import netmiko_send_command

# Switched to "nornir_test.yaml" so automated testing works (uses inventory files outside of Git)
# For more consistency with videos switch back to "nornir.yaml"
nr = InitNornir(config_file="nornir_test.yaml")
results = nr.run(task=netmiko_send_command, command_string="show ip int brief")

print()
for k, v in results.items():
    print("-" * 50)
    print(k)
    print(v[0].result)
    print("-" * 50)
print()
