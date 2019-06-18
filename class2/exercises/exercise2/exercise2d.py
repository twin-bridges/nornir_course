import os
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks.networking import netmiko_send_command


def main():
    nr = InitNornir(config_file="config.yaml")
    # Avoid storing lab password in GitHub, pull from environment variable
    nr.inventory.defaults.password = os.environ["NORNIR_PASSWORD"]
    filt = F(groups__contains="ios")
    nr = nr.filter(filt)
    print(nr.inventory.hosts)
    my_results = nr.run(
        task=netmiko_send_command, command_string="show run | i hostname"
    )
    print(type(my_results))
    print(dir(my_results))
    print(my_results.items())
    print(my_results.keys())
    print(my_results.values())
    host_results = my_results["cisco3"]
    print(type(host_results))
    print(dir(host_results))
    print(host_results[0])
    print(host_results.__iter__)
    task_result = host_results[0]
    print(type(task_result))
    print(dir(task_result))
    print(
        f"Host: {task_result.host}\n"
        f"Task Name: {task_result.name}\n"
        f"Failed: {task_result.failed}\n"
        f"Result: {task_result.result}"
    )


if __name__ == "__main__":
    main()
