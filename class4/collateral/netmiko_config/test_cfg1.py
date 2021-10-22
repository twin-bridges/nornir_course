from nornir import InitNornir
from nornir_netmiko import netmiko_send_config


if __name__ == "__main__":

    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="nxos1")

    # Direct inline configs
    commands = ["interface loopback90", "ip address 172.31.90.1/32"]

    # import pdbr
    # pdbr.set_trace()
    results = nr.run(task=netmiko_send_config, config_commands=commands)
    print(results["nxos1"][0].result)
