from pprint import pprint
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.functions.text import print_result


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="nxos"))
    agg_result = nr.run(
        task=napalm_get,
        getters=["config"],
        getters_options={"config": {"retrieve": "running"}},
    )
    print_result(agg_result)


if __name__ == "__main__":
    main()
