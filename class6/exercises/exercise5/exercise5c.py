import os
import random
import yaml
from ansible.parsing.vault import VaultLib, VaultSecret
from ansible.cli import CLI
from ansible.parsing.dataloader import DataLoader
from netmiko.ssh_exception import NetMikoAuthenticationException
from nornir import InitNornir
from nornir.core.exceptions import NornirSubTaskError
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command


BAD_PASSWORD = "bogus"
# Encrypted YAML file
VAULT_FILE = "vaulted_password.yaml"
VAULT_PASSWORD = os.environ["NORNIR_VAULT_PASSWORD"]


def decrypt_vault(
    filename, vault_password=None, vault_password_file=None, vault_prompt=False
):
    """
    filename: name of your encrypted file that needs decrypted.
    vault_password: key that will decrypt the vault.
    vault_password_file: file containing key that will decrypt the vault.
    vault_prompt: Force vault to prompt for a password if everything else fails.
    """

    loader = DataLoader()
    if vault_password:
        vault_secret = [([], VaultSecret(vault_password.encode()))]
    elif vault_password_file:
        vault_secret = CLI.setup_vault_secrets(
            loader=loader, vault_ids=[vault_password_file]
        )
    else:
        vault_secret = CLI.setup_vault_secrets(
            loader=loader, vault_ids=[], auto_prompt=vault_prompt
        )

    vault = VaultLib(vault_secret)

    with open(filename) as f:
        unencrypted_yaml = vault.decrypt(f.read())
        unencrypted_yaml = yaml.safe_load(unencrypted_yaml)
        return unencrypted_yaml


def send_command(task):
    command_mapper = {"junos": "show system uptime"}
    cmd = command_mapper.get(task.host.platform, "show clock")
    try:
        task.run(task=netmiko_send_command, command_string=cmd)
    except NornirSubTaskError as e:
        if isinstance(e.result.exception, NetMikoAuthenticationException):
            task.results.pop()
            vault_contents = decrypt_vault(
                filename=VAULT_FILE, vault_password=VAULT_PASSWORD
            )
            task.host.password = vault_contents["password"]
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
