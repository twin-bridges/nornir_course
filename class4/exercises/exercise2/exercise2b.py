from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import networking


def file_put(task):
    if task.host.platform == "eos":
        filename = "arista.txt"
    elif task.host.platform == "ios":
        filename = "cisco.txt"
    task.run(
        task=networking.netmiko_file_transfer,
        source_file=f"{task.host.platform}/{filename}",
        dest_file=filename,
        direction="put",
    )


def file_get(task):
    if task.host.platform == "eos":
        filename = "arista.txt"
    elif task.host.platform == "ios":
        filename = "cisco.txt"
    task.run(
        task=networking.netmiko_file_transfer,
        source_file=filename,
        dest_file=f"{task.host.platform}/get_{filename}",
        direction="get",
    )


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="ios") | F(groups__contains="eos"))
    result = nr.run(task=file_put)
    print_result(result)
    result = nr.run(task=file_get)
    print_result(result)


if __name__ == "__main__":
    main()
