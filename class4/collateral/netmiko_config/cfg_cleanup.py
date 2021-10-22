from nornir import InitNornir
from nornir_netmiko import netmiko_send_config
from nornir.core.filter import F


def custom_config(task):

    print(task.host)
    hostname = task.host.name
    groupname = task.host.groups[0].name

    # From external file
    file_name = f"{groupname}/{hostname}-cleanup.txt"
    print(file_name)
    results = task.run(task=netmiko_send_config, config_file=file_name)
    print("-" * 40)
    print(results[0].result)
    print("-" * 40)


if __name__ == "__main__":

    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="nxos"))
    nr.run(task=custom_config)
