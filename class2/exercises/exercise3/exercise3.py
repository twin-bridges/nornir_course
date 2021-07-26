import os
import re
from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko import netmiko_send_command

# Default to "10.220.88.1", but let us have envvar for different pods for internal use
DEFAULT_GATEWAY = os.environ.get("EOS_GATEWAY", "10.220.88.1")


def main():
    nr = InitNornir(config_file="config.yaml")
    # Filtering - will be explained in detail in later lessons.
    ios_filt = F(groups__contains="ios")
    eos_filt = F(groups__contains="eos")
    nr = nr.filter(ios_filt | eos_filt)
    my_results = nr.run(task=netmiko_send_command, command_string="show ip arp")

    parsed_results = []
    for host, multi_result in my_results.items():
        # multi_result is a list and in this example only has one element
        output = multi_result[0].result
        desired_data = ""
        for line in output.splitlines():
            if DEFAULT_GATEWAY in line:
                desired_data = line
                break
        parsed_results.append((host, desired_data))

    print()
    for host, gw_data in parsed_results:
        gw = re.sub(r"\s+", " ", gw_data)
        print(f"Host: {host}, Gateway: {gw}")
    print()


if __name__ == "__main__":
    main()
