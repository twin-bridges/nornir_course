from nornir import InitNornir
from nornir.core.filter import F
from nornir_napalm.tasks import napalm_get
from nornir_netmiko.tmp_glue import print_result

# Disable SSL Warnings
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="nxos"))
    agg_result = nr.run(task=napalm_get, getters=["config"])
    print_result(agg_result)


if __name__ == "__main__":
    main()
