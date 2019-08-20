import os
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks import networking


PASSWORD = os.environ.get("NORNIR_PASSWORD", "bogus")


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="nxos"))
    for host, data in nr.inventory.hosts.items():
        data.password = PASSWORD
    nr.run(
        task=networking.netmiko_send_command,
        command_string="show mac address-table",
        num_workers=1,
    )


if __name__ == "__main__":
    main()
