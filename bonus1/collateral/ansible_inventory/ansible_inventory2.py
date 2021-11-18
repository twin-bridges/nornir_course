import os
import pdbr  # noqa
from nornir import InitNornir


def main():
    nr = InitNornir(config_file="config.yaml")
    nr.inventory.hosts["nxos1"].password = os.environ["NORNIR_PASSWORD"]

    nxos = nr.inventory.hosts["nxos1"]  # noqa
    nxos_group = nr.inventory.groups["nxos"]  # noqa
    eos = nr.inventory.hosts["arista1"]  # noqa
    # pdbr.set_trace()


if __name__ == "__main__":
    main()
