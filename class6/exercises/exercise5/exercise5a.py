from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import networking


def send_command(task):
    command_mapper = {"junos": "show system uptime"}
    cmd = command_mapper.get(task.host.platform, "show clock")
    task.run(task=networking.netmiko_send_command, command_string=cmd)


def main():
    nr = InitNornir(config_file="config.yaml")
    agg_result = nr.run(task=send_command)
    print_result(agg_result)


if __name__ == "__main__":
    main()
