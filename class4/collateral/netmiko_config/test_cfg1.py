from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_config


def custom_config(task):

    print(task.host)

    # To force enable mode
    net_connect = task.host.get_connection("netmiko", task.nornir.config)
    net_connect.enable()

    # Direct inline configs
    commands = [
        "interface loopback90",
        "ip address 172.31.90.1/32",
    ]
    results = task.run(task=netmiko_send_config, config_commands=commands)

    # From external file
    file_name = f"{task.host.name}-intf.txt"
    print(file_name)
    results = task.run(task=netmiko_send_config, config_file=file_name)
    ipdb.set_trace()


if __name__ == "__main__":

    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="nxos1")
    import ipdb; ipdb.set_trace()
    results = nr.run(task=custom_config, num_workers=1)
