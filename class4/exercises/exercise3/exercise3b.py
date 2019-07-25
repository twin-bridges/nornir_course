from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import networking


def configure_vlan(task, vlan_id, vlan_name):
    result = task.run(
        task=networking.netmiko_send_command,
        command_string=f"show vlan brief | i {vlan_id}",
    )
    if result.result:
        existing_vlan_id = result.result.split()[0]
        existing_vlan_name = result.result.split()[1]
        if existing_vlan_id == vlan_id and existing_vlan_name == vlan_name:
            return "Nothing to do"
    result = task.run(
        task=networking.netmiko_send_config,
        config_commands=[f"vlan {vlan_id}", f"name {vlan_name}"],
    )


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="eos") | F(groups__contains="nxos"))
    result = nr.run(task=configure_vlan, vlan_id="123", vlan_name="ntp_vlan")
    print_result(result)


if __name__ == "__main__":
    main()
