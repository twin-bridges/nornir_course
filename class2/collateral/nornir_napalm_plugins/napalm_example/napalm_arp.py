from nornir import InitNornir
from nornir.plugins.tasks.networking import napalm_get
from pprint import pprint

nr = InitNornir(config_file="nornir.yaml")
results = nr.run(task=napalm_get, getters=["facts", "arp_table"])

print()
for k, v in results.items():
    print("-" * 50)
    print(k)
    pprint(v[0].result)
    print("-" * 50)
print()
