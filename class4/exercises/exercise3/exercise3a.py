from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_config


def configure_vlans(task, vlan_id, vlan_name):
    task.run(
        task=netmiko_send_config,
        config_commands=[f"vlan {vlan_id}", f"name {vlan_name}"],
    )


def main():

    VLAN_ID = "123"
    VLAN_NAME = "ntp_vlan"

    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="eos") | F(groups__contains="nxos"))
    result = nr.run(task=configure_vlans, vlan_id=VLAN_ID, vlan_name=VLAN_NAME)

    print_result(result)


if __name__ == "__main__":
    main()
