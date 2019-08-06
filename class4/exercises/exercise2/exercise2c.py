from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import networking


def file_copy(task):

    host = task.host
    platform = host.platform
    filename = host['file_name']
    dest_file = f"{platform}/{filename}-saved.txt"
    multi_result = task.run(
        task=networking.netmiko_file_transfer,
        source_file=filename,
        dest_file=dest_file,
        direction="get",
    )
    import ipdb; ipdb.set_trace()
    print()

def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="eos"))
    result = nr.run(task=file_copy, num_workers=1)
    print_result(result)


if __name__ == "__main__":
    main()
