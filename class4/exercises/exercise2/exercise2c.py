from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import networking


def file_copy(task, direction="put"):
    if task.host.platform == "eos":
        filename = "arista.txt"
    elif task.host.platform == "ios":
        filename = "cisco.txt"
    if direction == "put":
        source_file = f"{task.host.platform}/{filename}"
        dest_file = filename
    elif direction == "get":
        source_file = filename
        dest_file = f"{task.host.platform}/{task.host.name}_{filename}"
    task.run(
        task=networking.netmiko_file_transfer,
        source_file=source_file,
        dest_file=dest_file,
        direction=direction,
    )


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="ios") | F(groups__contains="eos"))
    result = nr.run(task=file_copy)
    print_result(result)
    result = nr.run(task=file_copy, direction="get")
    print_result(result)


if __name__ == "__main__":
    main()
