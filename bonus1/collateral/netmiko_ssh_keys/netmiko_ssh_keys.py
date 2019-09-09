from nornir import InitNornir


def netmiko_direct(task):

    # Manually create Netmiko connection
    net_connect = task.host.get_connection("netmiko", task.nornir.config)
    print(net_connect.find_prompt())

    output = net_connect.send_command("show ip int brief")
    print(output)


if __name__ == "__main__":
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="cisco4")
    nr.run(task=netmiko_direct)
