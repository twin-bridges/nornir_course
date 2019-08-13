from nornir import InitNornir
from nornir.core.task import Result
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
            result = f"Vlan {vlan_id} with name {vlan_name} exists, nothing to do!"
            changed = False
            failed = False
            return Result(host=task.host, result=result, changed=changed, failed=failed)
    else:
        multi_result = task.run(
            task=networking.netmiko_send_config,
            config_commands=[f"vlan {vlan_id}", f"name {vlan_name}"],
        )
        changed = True
        if "%Invalid command" in multi_result[0].result or "% Invalid input" in multi_result[0].result:
            failed = True
            result_msg = "An invalid configuration command was used."
        else:
            # Note task still could be marked at failed from the "netmiko_send_config"
            # execution i.e. at the MultiResult level.
            failed = False
            result_msg = f"Configured vlan {vlan_id} with name {vlan_name}!"
        return Result(host=task.host, result=result_msg, changed=changed, failed=failed)


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="eos") | F(groups__contains="nxos"))
    result = nr.run(task=configure_vlan, vlan_id="123", vlan_name="ntp_vlan", num_workers=1)
    print_result(result)


if __name__ == "__main__":
    main()
