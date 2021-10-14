import os
from rich import print
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get


nr = InitNornir(config_file="nornir.yaml")

# Code so automated tests will run properly
nr.inventory.groups["nxos"].password = os.environ["NORNIR_PASSWORD"]

results = nr.run(task=napalm_get, getters=["bgp_neighbors"])
print()
for k, v in results.items():
    print("-" * 50)
    print(k)
    print(v[0].result)
    print("-" * 50)
print()
