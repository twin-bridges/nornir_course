import os
from nornir import InitNornir
from rich import print
from nornir_napalm.plugins.tasks import napalm_get

nr = InitNornir(config_file="nornir.yaml")

# Code so automated tests will run properly
passwd_secret = os.environ["NORNIR_PASSWORD"]
nr.inventory.groups["cisco"].password = passwd_secret
nr.inventory.groups["cisco"].connection_options["napalm"].extras["optional_args"][
    "secret"
] = passwd_secret

results = nr.run(task=napalm_get, getters=["config"])
print()
for k, v in results.items():
    print("-" * 50)
    print(k)
    print(v[0].result)
    print("-" * 50)
print()
