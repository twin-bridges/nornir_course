from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="arista4")
    agg_result = nr.run(task=napalm_get, getters=["config"], retrieve="running")
    arista4_result = agg_result["arista4"][0].result
    arista4_running_config = arista4_result["config"]["running"]

    file_name = "arista4-running.txt"
    with open(file_name, "w") as f:
        f.write(arista4_running_config)
    print()
    print("#" * 40)
    print(arista4_running_config)
    print("#" * 40)
    print()


if __name__ == "__main__":
    main()
