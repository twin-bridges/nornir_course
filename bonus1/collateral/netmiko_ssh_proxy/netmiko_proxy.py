"""
In order for this script to work properly:
1. ~/.ssh/config needs setup correctly
2. SSH trust needs established to the intermediate server.
"""
from nornir import InitNornir


def netmiko_direct(task):

    # Manually create Netmiko connection
    net_connect = task.host.get_connection("netmiko", task.nornir.config)
    print(net_connect.find_prompt())

    output = net_connect.send_command("show users")
    print(output)


if __name__ == "__main__":
    # Use a context-manager so connections are gracefully closed
    with InitNornir(config_file="config.yaml") as nr:
        nr = nr.filter(name="cisco4")
        nr.run(task=netmiko_direct)
