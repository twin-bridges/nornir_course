from nornir import InitNornir
from nornir.plugins.functions.text import print_result


def netmiko_direct(task):

    # Manually create Netmiko connection
    net_connect = task.host.get_connection("netmiko", task.nornir.config)
    return net_connect.find_prompt()


if __name__ == "__main__":
    nr = InitNornir(config_file="config.yaml")
    agg_result = nr.run(task=netmiko_direct)
    print_result(agg_result)
