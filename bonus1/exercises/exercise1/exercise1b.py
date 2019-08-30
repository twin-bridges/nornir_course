import os
from nornir import InitNornir
from nornir.plugins.tasks import networking
from nornir.plugins.functions.text import print_result

PASSWORD = os.environ.get("NORNIR_PASSWORD", None)  # for testing purposes


def main():
    nr = InitNornir(config_file="config.yaml")
    for host, host_obj in nr.inventory.hosts.items():
        host_obj.password = PASSWORD
    print(nr.inventory.hosts)
    nxos1 = nr.inventory.hosts["nxos1"]
    print(nxos1.username)
    print(nxos1.password)
    print(nxos1.port)
    print(nxos1.platform)
    print(nxos1.get_connection_parameters("napalm").port)

    agg_results = nr.run(task=networking.napalm_get, getters=["ntp_servers"])
    print_result(agg_results)


if __name__ == "__main__":
    main()
