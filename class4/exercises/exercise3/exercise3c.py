from nornir import InitNornir
from nornir.core.task import Result
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command
from nornir_netmiko import netmiko_send_config


def configure_vlan(task, vlan_id, vlan_name):

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
            changed = False
            failed = False
            result = f"Vlan {vlan_id} with name {vlan_name} exists, nothing to do!"
            return Result(host=task.host, result=result, changed=changed, failed=failed)

    changed = True
    multi_result = task.run(
        task=netmiko_send_config,
        config_commands=[f"vlan {vlan_id}", f"name {vlan_name}"],
    )
    if (
        "%Invalid command" in multi_result[0].result
        or "% Invalid input" in multi_result[0].result
    ):
        failed = True
        result_msg = "An invalid configuration command was used."
    else:
        # Note task still could be marked at failed from the "netmiko_send_config"
        # execution i.e. at the MultiResult level.
        failed = False
        result_msg = f"Configured vlan {vlan_id} with name {vlan_name}!"

    return Result(host=task.host, result=result_msg, changed=changed, failed=failed)


def main():

    VLAN_ID = "123"
    VLAN_NAME = "ntp_vlan"

    nr = InitNornir(
        config_file="config.yaml", runner={"plugin": "serial", "options": {}}
    )
    nr = nr.filter(F(groups__contains="eos") | F(groups__contains="nxos"))
    result = nr.run(task=configure_vlan, vlan_id=VLAN_ID, vlan_name=VLAN_NAME)
    print_result(result)


if __name__ == "__main__":
    main()
