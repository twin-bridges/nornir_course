import os
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command


def main():
    nr = InitNornir(config_file="config.yaml", core={"num_workers": 15})
    # Avoid storing lab password in GitHub, pull from environment variable
    nr.inventory.defaults.password = os.environ["NORNIR_PASSWORD"]
    ios_filt = F(groups__contains="ios")
    nr = nr.filter(ios_filt)
    my_results = nr.run(task=netmiko_send_command, command_string="show ip int brief")
    print_result(my_results)
    print(f"Task failed hosts: {my_results.failed_hosts}")
    print(f"Global failed hosts: {nr.data.failed_hosts}")
    nr.inventory.hosts["cisco3"].password = os.environ["NORNIR_PASSWORD"]

    # Need to fix/improve this
    # Nornir doesnt reset connection for failed hosts causing issues
    print(nr.inventory.hosts["cisco3"].connections)
    try:
        nr.inventory.hosts["cisco3"].close_connections()
    except ValueError:
        pass
    except Exception as e:
        print(e)

    my_results = nr.run(
        task=netmiko_send_command,
        command_string="show ip int brief",
        on_good=False,
        on_failed=True,
    )
    print_result(my_results)
    print(f"Task failed hosts: {my_results.failed_hosts}")
    print(f"Global failed hosts: {nr.data.failed_hosts}")


if __name__ == "__main__":
    main()
