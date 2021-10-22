from nornir import InitNornir
from nornir.core.task import Result
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command


def my_task(task):
    changed = False
    if task.host.groups[0].name == "ios":
        cmd = "show run | i hostname"
        task.run(task=netmiko_send_command, command_string=cmd)
        changed = True
    elif task.host.groups[0].name == "junos":
        cmd = "show configuration system host-name "
        task.run(task=netmiko_send_command, command_string=cmd)
        changed = True
    return Result(host=task.host, changed=changed, failed=False, result="ran command")


def main():
    nr = InitNornir(
        config_file="config.yaml",
        logging={"enabled": False},
        runner={"plugin": "threaded", "options": {"num_workers": 15}},
    )
    nr = nr.filter(name="srx2")
    result = nr.run(task=my_task)
    print_result(result)

    # import pdbr
    # pdbr.set_trace()


if __name__ == "__main__":
    main()
