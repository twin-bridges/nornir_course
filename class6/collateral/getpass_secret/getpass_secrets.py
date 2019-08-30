from getpass import getpass
from nornir import InitNornir
from nornir.plugins.tasks import networking


SECRET = getpass()


def set_secret(nr, group):
    group = nr.inventory.groups[group]
    group.connection_options["netmiko"].extras["secret"] = SECRET


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="arista1")
    set_secret(nr, "eos")
    agg_result = nr.run(
        task=networking.netmiko_send_command,
        command_string="show run | i hostname",
        enable=True,
    )
    print(agg_result["arista1"].result)


if __name__ == "__main__":
    main()
