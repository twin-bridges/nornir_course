from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get
from nornir_napalm.plugins.tasks import napalm_configure


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="arista4")

    # Capture current running configuration
    agg_result = nr.run(task=napalm_get, getters=["config"], retrieve="running")
    arista4_result = agg_result["arista4"][0].result
    arista4_running_config = arista4_result["config"]["running"]

    # Configure a new loopback
    config = """interface loopback123
  description verycoolloopback"""
    agg_result = nr.run(task=napalm_configure, configuration=config)
    print_result(agg_result)

    print()

    # Completely resture the configuration using configure replace
    agg_result = nr.run(
        task=napalm_configure, configuration=arista4_running_config, replace=True
    )
    print_result(agg_result)


if __name__ == "__main__":
    main()
