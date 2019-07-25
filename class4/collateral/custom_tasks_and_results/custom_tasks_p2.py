from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import networking


def my_task(task):
    if task.host.groups[0] == "ios":
        cmd = "show run"
        task.run(task=networking.netmiko_send_command, command_string=cmd)
    elif task.host.groups[0] == "junos":
        cmd = "show configuration"
        task.run(task=networking.netmiko_send_command, command_string=cmd)


def main():
    nr = InitNornir(config_file="config.yaml", logging={"enabled": False})
    result = nr.run(task=my_task)
    print_result(result)


if __name__ == "__main__":
    main()
