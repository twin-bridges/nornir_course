from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks import networking
from nornir.plugins.functions.text import print_result


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="eos"))

    agg_result = nr.run(task=networking.napalm_get, getters=["config"])
    print_result(agg_result)


if __name__ == "__main__":
    main()
