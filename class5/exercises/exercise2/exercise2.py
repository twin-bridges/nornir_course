import os
from nornir import InitNornir
from nornir.core.filter import F
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result

# Storing password in environment variable to avoid storing in Git
PASSWORD = os.environ.get("NORNIR_PASSWORD", "bogus")


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="eos"))
    for hostname, host_obj in nr.inventory.hosts.items():
        host_obj.password = PASSWORD
    agg_result = nr.run(task=napalm_get, getters=["config"])
    print_result(agg_result)


if __name__ == "__main__":
    main()
