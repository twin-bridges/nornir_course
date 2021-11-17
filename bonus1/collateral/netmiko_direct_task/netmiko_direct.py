import pdbr  # noqa
from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result  # noqa


def netmiko_direct(task):

    # Manually create Netmiko connection
    net_connect = task.host.get_connection("netmiko", task.nornir.config)
    print()
    print("#" * 80)
    print(net_connect.find_prompt())
    output = net_connect.send_command("show ip int brief")
    print(output)
    print("#" * 80)
    print()


if __name__ == "__main__":
    # Use a context-manager so connections are gracefully closed
    with InitNornir(config_file="config.yaml") as nr:
        ios_filt = F(groups__contains="ios")
        nr_ios = nr.filter(ios_filt)
        nr_ios.run(task=netmiko_direct)
