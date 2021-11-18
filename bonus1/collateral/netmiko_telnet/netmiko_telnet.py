from nornir import InitNornir


def netmiko_direct(task):

    # Manually create Netmiko connection
    # import ipdb; ipdb.set_trace()
    net_connect = task.host.get_connection("netmiko", task.nornir.config)
    print(net_connect.find_prompt())
    output = net_connect.send_command("show ip int brief")
    print(output)


if __name__ == "__main__":
    # Use a context-manager so connections are gracefully closed
    with InitNornir(config_file="config.yaml") as nr:
        nr_cisco1 = nr.filter(name="cisco1")
        nr_cisco1.run(task=netmiko_direct)
