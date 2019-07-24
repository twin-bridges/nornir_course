from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import networking


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="arista4")
    result = nr.run(task=networking.napalm_get, getters=["config"], retrieve="running")
    print_result(result)
    arista4_running_config = result["arista4"][0].result["config"]["running"]
    print(arista4_running_config)


if __name__ == "__main__":
    main()
