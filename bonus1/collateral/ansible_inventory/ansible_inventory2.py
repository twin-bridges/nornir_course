import os
import pdbr  # noqa
from nornir import InitNornir
from nornir_netmiko import netmiko_send_command


def main():
    nr = InitNornir(config_file="config.yaml")
    nr.inventory.hosts["nxos1"].password = os.environ["NORNIR_PASSWORD"]

    nxos = nr.inventory.hosts["nxos1"]
    nxos_group = nr.inventory.groups["nxos"]
    eos = nr.inventory.hosts["arista1"]
    # pdbr.set_trace()


if __name__ == "__main__":
    main()
