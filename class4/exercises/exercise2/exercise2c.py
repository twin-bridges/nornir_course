from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_file_transfer


def file_copy(task):
    host = task.host
    platform = host.platform
    filename = host["file_name"]
    dest_file = f"{platform}/{host.name}-saved.txt"
    multi_result = task.run(
        task=netmiko_file_transfer,
        source_file=filename,
        dest_file=dest_file,
        direction="get",
        overwrite_file=True,
    )
    if multi_result[0].result is True:
        return f"SCP get completed: {dest_file}"
    else:
        return "Failure...SCP get failed!!!"


def main():
    nr = InitNornir(
        config_file="config.yaml",
        runner={"plugin": "threaded", "options": {"num_workers": 10}},
    )
    nr = nr.filter(F(groups__contains="eos"))
    result = nr.run(task=file_copy)
    print_result(result)


if __name__ == "__main__":
    main()
