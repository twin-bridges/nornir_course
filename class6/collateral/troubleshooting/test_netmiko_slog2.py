import pdbr  # noqa
from nornir import InitNornir
from nornir_netmiko import netmiko_send_command


def uptime(task):

    # pdbr.set_trace()

    # Dynamically set the session_log to be unique per host
    filename = f"{task.host}-output.txt"
    group_object = task.host.groups[0]
    group_object.connection_options["netmiko"].extras["session_log"] = filename

    cmd_mapper = {
        "ios": "show version | inc uptime",
        "eos": "show version | inc Uptime",
        "nxos": "show version | inc uptime",
        "junos": "show system uptime | match System",
    }
    host = task.host
    platform = host.platform
    cmd = cmd_mapper[platform]
    multi_result = task.run(task=netmiko_send_command, command_string=cmd)
    print(multi_result)


def main():
    nr = InitNornir(config_file="config_serial.yaml")
    agg_result = nr.run(task=uptime)
    for hostname, multi_result in agg_result.items():
        print()
        print("-" * 40)
        print(f"{hostname}: {multi_result[1].result}")
        print("-" * 40)
        print()


if __name__ == "__main__":
    main()
