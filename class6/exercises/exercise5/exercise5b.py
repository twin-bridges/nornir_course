import os
import random
from netmiko.ssh_exception import NetMikoAuthenticationException
from nornir import InitNornir
from nornir.core.exceptions import NornirSubTaskError
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command


BAD_PASSWORD = "bogus"


def send_command(task):
    command_mapper = {"junos": "show system uptime"}
    cmd = command_mapper.get(task.host.platform, "show clock")
    try:
        task.run(task=netmiko_send_command, command_string=cmd)
    except NornirSubTaskError as e:
        if isinstance(e.result.exception, NetMikoAuthenticationException):
            # Remove the failed task (so ultimately the Nornir print output is cleaner)
            task.results.pop()

            # For failed devices reset the password to the correct value using environment var
            task.host.password = os.environ["NORNIR_PASSWORD"]
            # Try again (with the correct password)
            task.run(task=netmiko_send_command, command_string=cmd)
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
