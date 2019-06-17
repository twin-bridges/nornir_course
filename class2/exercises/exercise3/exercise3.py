import os
import re
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks.networking import netmiko_send_command


def main():
    nr = InitNornir(config_file="config.yaml")
    # Avoid storing lab password in GitHub, pull from environment variable
    nr.inventory.defaults.password = os.environ["NORNIR_PASSWORD"]
    ios_filt = F(groups__contains="ios")
    eos_filt = F(groups__contains="eos")
    nr = nr.filter(ios_filt | eos_filt)
    my_results = nr.run(task=netmiko_send_command, command_string="show ip arp")
    parsed_results = []
    for host, data in my_results.items():
        output = data[0].result
        desired_data = [line for line in output.splitlines() if "10.220.88.1" in line][
            0
        ]
        parsed_results.append((host, desired_data))
    for entry in parsed_results:
        gw = re.sub(r"\s+", " ", entry[1])
        print(f"Host: {entry[0]}, Gateway: {gw}")


if __name__ == "__main__":
    main()
