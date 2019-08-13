from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import networking


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="arista4")
    agg_result = nr.run(task=networking.napalm_get, getters=["config"], retrieve="running")
    arista4_result = agg_result["arista4"][0].result
    arista4_running_config = arista4_result["config"]["running"]
    print(arista4_running_config)


if __name__ == "__main__":
    main()
