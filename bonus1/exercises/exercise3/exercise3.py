from nornir import InitNornir
from nornir_utils.plugins.functions import print_result


def netmiko_direct(task):

    # Manually create Netmiko connection
    net_connect = task.host.get_connection("netmiko", task.nornir.config)
    return net_connect.find_prompt()


if __name__ == "__main__":
    with InitNornir(config_file="config.yaml") as nr:
        agg_result = nr.run(task=netmiko_direct)
        print_result(agg_result)
