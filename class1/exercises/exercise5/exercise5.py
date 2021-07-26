from nornir import InitNornir


def my_task(task):
    host = task.host
    print()
    print(host.hostname)
    print("-" * 12)
    print(f"DNS1: {host['dns1']}")
    print(f"DNS2: {host['dns2']}")
    print()


if __name__ == "__main__":
    nr = InitNornir(config_file="config.yaml")
    nr.run(task=my_task)
