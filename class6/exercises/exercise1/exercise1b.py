from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command


def send_command(task):
    mul_result = task.run(task=netmiko_send_command, command_string="show ip interface")
    if "syntax error" in mul_result.result:
        raise ValueError("Invalid Junos command")


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="srx2")
    agg_result = nr.run(task=send_command)
    print_result(agg_result)


if __name__ == "__main__":
    main()
