from getpass import getpass
import logging
import os
from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko import netmiko_send_command


LOGGER = logging.getLogger("nornir")

# Environment variable for automated testing purposes
if os.environ.get("NORNIR_PASSWORD", False):
    PASSWORD = os.environ["NORNIR_PASSWORD"]
else:
    PASSWORD = getpass()


def main():
    LOGGER.info("Script initalizing...")
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="eos"))
    for hostname, host_obj in nr.inventory.hosts.items():
        host_obj.password = PASSWORD
    LOGGER.critical("Passwords set, commence automation!")
    nr.run(task=netmiko_send_command, command_string="show mac address-table")
    LOGGER.error("Oh no! We're all out of automation tasks :(")
    LOGGER.debug("Hey, what are you still doing here?")


if __name__ == "__main__":
    main()
