from getpass import getpass
from nornir import InitNornir
from nornir.plugins.tasks import networking


PASSWORD = getpass()


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="arista1")
    for hostname, host_obj in nr.inventory.hosts.items():
        host_obj.password = PASSWORD
    agg_result = nr.run(
        task=networking.netmiko_send_command, command_string="show run | i hostname"
    )
    print(agg_result["arista1"].result)


if __name__ == "__main__":
    main()
