from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command
from nornir_netmiko import netmiko_send_config


def configure_vlans(task, vlan_id, vlan_name):

    # Check current VLAN configuration
    multi_result = task.run(
        task=netmiko_send_command, command_string=f"show vlan brief | i {vlan_id}"
    )

    # Inspect results and return if already correct
    vlan_out = multi_result[0].result
    if vlan_out:
        existing_vlan_id = vlan_out.split()[0]
        existing_vlan_name = vlan_out.split()[1]
        if existing_vlan_id == vlan_id and existing_vlan_name == vlan_name:
            return "No changes: configuration already correct."

    # Configuration not correct - make changes
    task.run(
        task=netmiko_send_config,
        config_commands=[f"vlan {vlan_id}", f"name {vlan_name}"],
    )
    return "Configuration changed!"


def main():

    VLAN_ID = "123"
    VLAN_NAME = "ntp_vlan"

    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="eos") | F(groups__contains="nxos"))
    result = nr.run(task=configure_vlans, vlan_id=VLAN_ID, vlan_name=VLAN_NAME)

    print_result(result)


if __name__ == "__main__":
    main()
