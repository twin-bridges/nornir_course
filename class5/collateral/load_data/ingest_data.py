from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import data


def custom_task(task):
    inyaml = task.run(task=data.load_yaml, file=f"nxos/{task.host.name}.yaml")
    print(inyaml.result)


def main():
    nr = InitNornir(config_file="config.yaml", logging={"enabled": False})
    nr = nr.filter(groups=["nxos"])
    result = nr.run(task=custom_task)
    print_result(result)


if __name__ == "__main__":
    main()
