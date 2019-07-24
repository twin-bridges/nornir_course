from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import networking


def capture_default_route(task):
    if task.host.platform == "ios":
        cmd = "show ip route 0.0.0.0"
        result = task.run(task=networking.netmiko_send_command, command_string=cmd)
        for line in result.result.splitlines():
            if line.strip().startswith("*"):
                return_data = f"Next hop: {line.strip()[2:]}"
    elif task.host.platform == "junos":
        cmd = "show route 0.0.0.0"
        result = task.run(task=networking.netmiko_send_command, command_string=cmd)
        for line in result.result.splitlines():
            if line.strip().startswith(">"):
                return_data = f"Next hop: {line.strip()[4:]}"
    else:
        return_data = f"Command not executed on platform {task.host.platform}"
    return return_data


def main():
    nr = InitNornir(config_file="config.yaml")
    result = nr.run(task=capture_default_route, num_workers=1)
    print_result(result)


if __name__ == "__main__":
    main()
