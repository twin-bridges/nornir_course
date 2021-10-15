import pdbr  # noqa
from rich import print
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result


def main():
    nr = InitNornir(config_file="config.yaml")

    # pdbr.set_trace()

    nr = nr.filter(name="srx2")
    print(nr.inventory.hosts)

    results = nr.run(task=napalm_get, getters=["config"])
    print_result(results)

    results = nr.run(task=napalm_get, getters=["config"], retrieve="running")
    print_result(results)

    results = nr.run(task=napalm_get, getters=["config", "facts"], retrieve="running")
    print_result(results)

    print(nr.data.failed_hosts)
    nr.data.recover_host("srx2")

    results = nr.run(
        task=napalm_get,
        getters=["config", "facts"],
        getters_options={"config": {"retrieve": "running"}},
    )
    print_result(results)


if __name__ == "__main__":
    main()
