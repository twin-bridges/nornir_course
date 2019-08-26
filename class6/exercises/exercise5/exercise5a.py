from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import networking


COMMAND_MAPPER = {"junos": "show system uptime"}


def send_command(task):
    cmd = COMMAND_MAPPER.get(task.host.platform, "show clock")
    task.run(task=networking.netmiko_send_command, command_string=cmd)


def main():
    nr = InitNornir(config_file="config.yaml")
    agg_result = nr.run(task=send_command)
    print_result(agg_result)


if __name__ == "__main__":
    main()
