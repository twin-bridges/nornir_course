import os
from nornir import InitNornir
from nornir_netmiko import netmiko_send_command


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="cisco3")

    # Pass in passwd-secret from environment variable so automated tests work properly
    passwd_secret = os.environ["NORNIR_PASSWORD"]
    nr.inventory.defaults.password = passwd_secret
    nr.inventory.defaults.connection_options["netmiko"].extras["secret"] = passwd_secret

    agg_result = nr.run(
        task=netmiko_send_command, command_string="show run | i hostname", enable=True
    )
    print(agg_result["cisco3"].result)


if __name__ == "__main__":
    main()
