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
    print(host_obj.connections)
    host_obj.close_connection("netmiko")
    print(host_obj.connections)


if __name__ == "__main__":
    # Use a context-manager so connections are gracefully closed
    with InitNornir(config_file="config.yaml") as nr:
        ios_filt = F(groups__contains="ios")
        nr_ios = nr.filter(ios_filt)
        nr_ios.run(task=netmiko_direct)
        # pdbr.set_trace()

    # pdbr.set_trace()
