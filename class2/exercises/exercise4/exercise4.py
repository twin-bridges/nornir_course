import os
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks.networking import napalm_get


def main():
    nr = InitNornir(config_file="config.yaml")
    # Avoid storing lab password in GitHub, pull from environment variable
    nr.inventory.defaults.password = os.environ["NORNIR_PASSWORD"]
    ios_filt = F(groups__contains="ios")
    eos_filt = F(groups__contains="eos")
    nr = nr.filter(ios_filt | eos_filt)
    my_results = nr.run(task=napalm_get, getters=["arp_table"])
    parsed_results = []
    for host, data in my_results.items():
        output = data[0].result["arp_table"]
        desired_data = [line for line in output if line["ip"] == "10.220.88.1"][0]
        parsed_results.append((host, desired_data))
    for entry in parsed_results:
        print(f"Host: {entry[0]}, Gateway: {entry[1]}")


if __name__ == "__main__":
    main()
