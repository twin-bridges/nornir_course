from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import networking


def capture_default_route(task):
    cmd = "show ip route 0.0.0.0"
    result = task.run(task=networking.netmiko_send_command, command_string=cmd)
    for line in result.result.splitlines():
        if line.strip().startswith("*"):
            next_hop = line.strip()[2:]
    return f"Next hop: {next_hop}"


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="ios"))
    result = nr.run(task=capture_default_route)
    print_result(result)


if __name__ == "__main__":
    main()
