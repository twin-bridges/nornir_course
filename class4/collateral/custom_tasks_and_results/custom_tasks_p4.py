from nornir import InitNornir
from nornir.core.task import Result
from nornir_netmiko.tmp_glue import print_result
from nornir_netmiko import netmiko_send_command


def my_task(task):
    changed = False
    if task.host.groups[0] == "ios":
        cmd = "show run | i hostname"
        task.run(task=netmiko_send_command, command_string=cmd)
        changed = True
    elif task.host.groups[0] == "junos":
        cmd = "show configuration system host-name "
        task.run(task=netmiko_send_command, command_string=cmd)
        changed = True
    return Result(host=task.host, changed=changed, failed=False, result="ran command")


def main():
    nr = InitNornir(config_file="config.yaml", logging={"enabled": False})
    nr = nr.filter(name="srx2")
    result = nr.run(task=my_task, num_workers=1)
    print_result(result)
    import ipdb

    ipdb.set_trace()


if __name__ == "__main__":
    main()
