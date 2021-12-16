from rich import print
from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko import netmiko_send_command


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="ios") | F(groups__contains="nxos"))
    agg_result = nr.run(
        task=netmiko_send_command, command_string="show version", use_genie=True
    )

    # Genie should be thread-safe now, just print the results
    # The type-returned now is a Genie-object that is dictionary-like
    for host, multi_result in agg_result.items():
        print(host)
        print("-" * 20)
        print(multi_result.result)
        print("-" * 20)
        print()


if __name__ == "__main__":
    main()
