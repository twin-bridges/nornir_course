from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import networking


def uptime(task):

    host = task.host
    platform = host.platform

    cmd_mapper = {
        "ios": "show version | inc uptime",
        "eos": "show version | inc Uptime",
        "nxos": "show version | inc uptime",
        "junos": "show system uptime | match System"
    }
    cmd = cmd_mapper[platform]
    print(cmd)
    result = task.run(task=networking.netmiko_send_command, command_string=cmd)


def main():
    nr = InitNornir(config_file="config.yaml")
    result = nr.run(task=uptime)
    print_result(result)


if __name__ == "__main__":
    main()
