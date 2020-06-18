from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko import netmiko_send_command


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="ios") | F(groups__contains="nxos"))
    agg_result = nr.run(
        task=netmiko_send_command, command_string="show version", use_genie=True,
    )
    for host, multi_result in agg_result.items():
        print(host, type(multi_result.result))
    print(agg_result["cisco3"].result)


if __name__ == "__main__":
    main()
