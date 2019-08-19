import yaml
from ansible.parsing.vault import VaultLib, VaultSecret
from ansible.cli import CLI
from ansible.parsing.dataloader import DataLoader
from nornir import InitNornir
from nornir.plugins.tasks import networking


def load_vaulted_pass(
    vault_password=None, vault_password_file=None, vault_prompt=False
):
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
    unencrypted_yaml = vault.decrypt(open("vaulted_password").read())
    unencrypted_yaml = yaml.safe_load(unencrypted_yaml)
    return unencrypted_yaml["password"]


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="arista1")
    for host, data in nr.inventory.hosts.items():
        data.password = load_vaulted_pass()
    agg_result = nr.run(
        task=networking.netmiko_send_command, command_string="show run | i hostname"
    )
    print(agg_result["arista1"].result)


if __name__ == "__main__":
    main()
