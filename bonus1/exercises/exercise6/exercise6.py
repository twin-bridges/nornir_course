from nornir import InitNornir
from nornir.plugins.functions.text import print_result


def verify_napalm_nxos_ssh_connection(task):
    napalm_conn = task.host.get_connection("napalm", task.nornir.config)
    print(napalm_conn)
    netmiko_conn = napalm_conn.device
    print(netmiko_conn)
    print(dir(netmiko_conn))
    print(netmiko_conn.find_prompt())


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="nxos1")
    agg_result = nr.run(task=verify_napalm_nxos_ssh_connection)
    print_result(agg_result)


if __name__ == "__main__":
    main()
