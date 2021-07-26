from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_file_transfer


def file_copy(task):
    host = task.host
    platform = host.platform
    filename = host["file_name"]
    source_file = f"{platform}/{filename}"
    task.run(
        task=netmiko_file_transfer,
        source_file=source_file,
        dest_file=filename,
        direction="put",
        overwrite_file=True,
    )


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="eos"))
    result = nr.run(task=file_copy)
    print_result(result)


if __name__ == "__main__":
    main()
