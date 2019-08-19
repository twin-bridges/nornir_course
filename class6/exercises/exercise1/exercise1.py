from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import networking


def send_command(task):
    mul_result = task.run(
        task=networking.netmiko_send_command, command_string="show ip interface brief"
    )
    if "syntax error" in mul_result.result:
        raise ValueError


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="srx2")
    agg_result = nr.run(task=send_command)
    print_result(agg_result)


if __name__ == "__main__":
    main()
