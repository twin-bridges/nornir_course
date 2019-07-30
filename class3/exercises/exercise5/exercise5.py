from pprint import pprint
from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(groups=["eos"])
    result = nr.run(
        task=netmiko_send_command, command_string="show int status", use_textfsm=True
    )
    combined_data = {}
    for res in result:
        combined_data[res] = {}
        for interface in result[res].result:
            combined_data[res][interface["port"]] = {}
            combined_data[res][interface["port"]]["status"] = interface["status"]
            combined_data[res][interface["port"]]["vlan"] = interface["vlan"]
    pprint(combined_data)


if __name__ == "__main__":
    main()
