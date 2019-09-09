from nornir import InitNornir
import ipdb


def netmiko_direct(task):

    # Manually create Netmiko connection
    ipdb.set_trace()
    net_connect = task.host.get_connection("netmiko", task.nornir.config)
    print(net_connect.find_prompt())
    output = net_connect.send_command("show ip int brief")
    print(output)


if __name__ == "__main__":
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="cisco1")
    nr.run(task=netmiko_direct)
