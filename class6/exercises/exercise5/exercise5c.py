import os
import random
import yaml
from ansible.parsing.vault import VaultLib, VaultSecret
from netmiko.ssh_exception import NetMikoAuthenticationException
from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import networking
from nornir.core.exceptions import NornirSubTaskError


BAD_PASSWORD = "bogus"
VAULT_PASSWORD = os.environ.get("NORNIR_VAULT_PASSWORD", "bogus")
COMMAND_MAPPER = {"junos": "show system uptime"}


def load_vaulted_pass():
    vault_secret = [([], VaultSecret(VAULT_PASSWORD.encode()))]
    vault = VaultLib(vault_secret)
    unencrypted_yaml = vault.decrypt(open("vaulted_password.yaml").read())
    unencrypted_yaml = yaml.safe_load(unencrypted_yaml)
    return unencrypted_yaml["password"]


def send_command(task):
    cmd = COMMAND_MAPPER.get(task.host.platform, "show clock")
    try:
        task.run(task=networking.netmiko_send_command, command_string=cmd)
    except NornirSubTaskError as e:
        if isinstance(e.result.exception, NetMikoAuthenticationException):
            task.results.pop()
            task.host.password = load_vaulted_pass()
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
