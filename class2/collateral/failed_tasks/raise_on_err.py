from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result


def main():
    nr = InitNornir(config_file="config.yaml")
    result = nr.run(task=netmiko_send_command, command_string="show run | i pid")
    print_result(result)
    result = nr.run(
        task=netmiko_send_command,
        on_failed=True,
        command_string="show run | i hostname",
    )
    print_result(result)


if __name__ == "__main__":
    main()
