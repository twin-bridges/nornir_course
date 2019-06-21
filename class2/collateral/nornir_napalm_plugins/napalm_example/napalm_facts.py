from nornir import InitNornir
from nornir.plugins.tasks.networking import napalm_get

nr = InitNornir(config_file="nornir.yaml")
results = nr.run(task=napalm_get, getters=["facts"])

print()
for k, v in results.items():
    print("-" * 50)
    print(k)
    print(v[0].result)
    print("-" * 50)
print()
