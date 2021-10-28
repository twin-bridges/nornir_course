from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_utils.plugins.tasks.data import load_json  # noqa


def custom_task(task):
    # injson = task.run(task=load_json, file=f"nxos/{task.host.name}.json")
    # print(injson.result)
    inyaml = task.run(task=load_yaml, file=f"nxos/{task.host.name}.yaml")
    print(inyaml.result)


def main():
    nr = InitNornir(config_file="config.yaml", logging={"enabled": False})
    nr = nr.filter(F(groups__contains="nxos"))
    result = nr.run(task=custom_task)
    print_result(result)


if __name__ == "__main__":
    main()
