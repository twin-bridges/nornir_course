from nornir import InitNornir
from nornir.core.task import Result
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command


def my_task(task):
    if task.host.groups[0] == "ios":
        cmd = "show run"
        task.run(task=netmiko_send_command, command_string=cmd)
    elif task.host.groups[0] == "junos":
        cmd = "show configuration"
        task.run(task=netmiko_send_command, command_string=cmd)


def new_task(task):
    result = "this task succeeded"
    return Result(host=task.host, result=result, failed=False, changed=True)


def main():
    nr = InitNornir(config_file="config.yaml", logging={"enabled": False})
    # result = nr.run(task=my_task)
    # print_result(result)
    nr = nr.filter(name="arista1")
    result = nr.run(task=new_task)

    # import pdbr
    # pdbr.set_trace()
    print_result(result)


if __name__ == "__main__":
    main()
