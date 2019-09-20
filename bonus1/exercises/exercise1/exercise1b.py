import os
from nornir import InitNornir
from nornir.plugins.tasks import networking
from nornir.plugins.functions.text import print_result

PASSWORD = os.environ.get("NORNIR_PASSWORD", None)  # for testing purposes


def main():
    nr = InitNornir(config_file="config.yaml")
    for host, host_obj in nr.inventory.hosts.items():
        host_obj.password = PASSWORD
    nxos1 = nr.inventory.hosts["nxos1"]

    print()
    print(nr.inventory.hosts)
    print(f"Username: {nxos1.username}")
    print(f"Password: {nxos1.password}")
    print(f"Port: {nxos1.port}")
    print(f"Platform: {nxos1.platform}")
    print(f"NAPALM Port: {nxos1.get_connection_parameters('napalm').port}")
    print()

    agg_results = nr.run(task=networking.napalm_get, getters=["ntp_servers"])
    print_result(agg_results)
    print()


if __name__ == "__main__":
    main()
