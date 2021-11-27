import pdbr  # noqa
from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result  # noqa


def netmiko_direct(task):

    # Manually create Netmiko connection
    host_obj = task.host
    net_connect = host_obj.get_connection("netmiko", task.nornir.config)
    print(net_connect.find_prompt())
    # pdbr.set_trace()


def netmiko_direct2(task):
    host_obj = task.host
    net_connect = host_obj.get_connection("netmiko", task.nornir.config)
    print(net_connect.find_prompt())
    # pdbr.set_trace()


if __name__ == "__main__":
    with InitNornir(config_file="config.yaml") as nr:
        ios_filt = F(groups__contains="ios")
        nr_ios = nr.filter(ios_filt)
        nr_ios.run(task=netmiko_direct)
        nr_ios.run(task=netmiko_direct2)

    # pdbr.set_trace()
    print("Outside context manager")
