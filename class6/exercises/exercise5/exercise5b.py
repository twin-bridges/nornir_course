import os
import random
from netmiko.ssh_exception import NetMikoAuthenticationException
from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import networking
from nornir.core.exceptions import NornirSubTaskError


BAD_PASSWORD = "bogus"
COMMAND_MAPPER = {"junos": "show system uptime"}


def send_command(task):
    cmd = COMMAND_MAPPER.get(task.host.platform, "show clock")
    try:
        task.run(task=networking.netmiko_send_command, command_string=cmd)
    except NornirSubTaskError as e:
        if isinstance(e.result.exception, NetMikoAuthenticationException):
            task.host.password = os.environ[
                "NORNIR_PASSWORD"
            ]  # set via env var for testing purposes
            try:
                task.host.close_connections()
            except ValueError:
                pass
            task.run(task=networking.netmiko_send_command, command_string=cmd)
        else:
            return f"Unhandled exception: {e}"


def main():
    nr = InitNornir(config_file="config.yaml")
    for host, data in nr.inventory.hosts.items():
        if random.choice([True, False]):
            data.password = BAD_PASSWORD
    agg_result = nr.run(task=send_command)
    print_result(agg_result)


if __name__ == "__main__":
    main()
