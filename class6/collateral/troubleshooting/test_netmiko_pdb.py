from nornir import InitNornir
from nornir.plugins.tasks import networking


def uptime(task):
    cmd_mapper = {
        "ios": "show version | inc uptime",
        "eos": "show version | inc Uptime",
        "nxos": "show version | inc uptime",
        "junos": "show system uptime | match System",
    }
    host = task.host
    platform = host.platform
    cmd = cmd_mapper[platform]
    # import ipdb
    # ipdb.set_trace()
    multi_result = task.run(task=networking.netmiko_send_command, command_string=cmd)
    print(multi_result)
    print(multi_result)
    print(multi_result)


def main():
    nr = InitNornir(config_file="config.yaml")
    agg_result = nr.run(task=uptime, num_workers=1)
    for hostname, multi_result in agg_result.items():
        print()
        print("-" * 40)
        print(f"{hostname}: {multi_result[1].result}")
        print("-" * 40)
        print()


if __name__ == "__main__":
    main()
