import os
import random
from netmiko.ssh_exception import NetMikoAuthenticationException
from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import networking
from nornir.core.exceptions import NornirSubTaskError


BAD_PASSWORD = "bogus"


def send_command(task):
    command_mapper = {"junos": "show system uptime"}
    cmd = command_mapper.get(task.host.platform, "show clock")
    try:
        task.run(task=networking.netmiko_send_command, command_string=cmd)
    except NornirSubTaskError as e:
        if isinstance(e.result.exception, NetMikoAuthenticationException):
            # For failed devices reset the password to the correct value using environment var
            task.host.password = os.environ[
                "NORNIR_PASSWORD"
            ]

            # Force Nornir to close stale connections
            try:
                task.host.close_connections()
            except ValueError:
                pass

            task.run(task=networking.netmiko_send_command, command_string=cmd)
        else:
            return f"Unhandled exception: {e}"


def main():
    nr = InitNornir(config_file="config.yaml")
    for hostname, host_obj in nr.inventory.hosts.items():
        if random.choice([True, False]):
            host_obj.password = BAD_PASSWORD
    agg_result = nr.run(task=send_command)
    print_result(agg_result)


if __name__ == "__main__":
    main()
