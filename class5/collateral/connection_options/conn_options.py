from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import networking


def main():
    nr = InitNornir(config_file="config.yaml", logging={"enabled": False})
    nr = nr.filter(name="arista4")

    netmiko_results = nr.run(
        task=networking.netmiko_send_command, command_string="show ip arp"
    )
    print_result(netmiko_results)
    netmiko_results = nr.run(
        task=networking.netmiko_send_command,
        command_string="show run | i hostname",
        enable=True,
    )
    print_result(netmiko_results)

    napalm_results = nr.run(task=networking.napalm_get, getters=["interfaces"])
    print_result(napalm_results)


if __name__ == "__main__":
    main()
