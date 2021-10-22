from nornir import InitNornir
from nornir_netmiko import netmiko_send_config


def custom_config(task):

    # import pdbr
    # pdbr.set_trace()
    print(task.host)

    # To force enable mode
    net_connect = task.host.get_connection("netmiko", task.nornir.config)
    net_connect.enable()
    print(net_connect.global_delay_factor)
    print(net_connect.fast_cli)

    # Direct inline configs
    commands = ["interface loopback90", "ip address 172.31.90.1/32"]
    results = task.run(task=netmiko_send_config, config_commands=commands)
    print(results[0].result)


if __name__ == "__main__":

    nr = InitNornir(
        config_file="config.yaml", runner={"plugin": "serial", "options": {}}
    )
    nr = nr.filter(name="nxos1")
    nr.run(task=custom_config)
