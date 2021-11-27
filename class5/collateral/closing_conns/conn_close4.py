import pdbr  # noqa
from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result  # noqa


def netmiko_direct(task):

    # Manually create Netmiko connection
    host_obj = task.host
    net_connect = host_obj.get_connection("netmiko", task.nornir.config)
    print(net_connect.find_prompt())


if __name__ == "__main__":
    # No context-manager
    nr = InitNornir(config_file="config.yaml")
    ios_filt = F(groups__contains="ios")
    nr = nr.filter(ios_filt)
    nr.run(task=netmiko_direct)
    # pdbr.set_trace()
    print(nr.inventory.hosts["cisco3"].connections)
    nr.close_connections()
    print(nr.inventory.hosts["cisco3"].connections)
