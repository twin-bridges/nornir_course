import os
from nornir import InitNornir
from nornir.core.filter import F
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result


PASSWORD = os.environ.get("NORNIR_PASSWORD", None)  # for testing purposes


def transform_ansible_inventory(host):
    host.password = PASSWORD or host["ansible_ssh_pass"]
    netmiko_params = host.get_connection_parameters("netmiko")
    napalm_params = host.get_connection_parameters("napalm")
    if "nxos" in host.groups:
        netmiko_params.platform = "cisco_nxos"
        napalm_params.platform = "nxos"
        napalm_params.port = "8443"
    elif "cisco" in host.groups:
        netmiko_params.platform = "cisco_ios"
        napalm_params.platform = "ios"
    elif "arista" in host.groups:
        netmiko_params.platform = "arista_eos"
        netmiko_params.extras["global_delay_factor"] = 4
        napalm_params.platform = "eos"
    elif "juniper" in host.groups:
        netmiko_params.platform = "juniper_junos"
        napalm_params.platform = "junos"
    host.connection_options["netmiko"] = netmiko_params
    host.connection_options["napalm"] = napalm_params


def main():
    nr = InitNornir(config_file="config_b.yaml")
    nr = nr.filter(F(groups__contains="nxos"))
    agg_result = nr.run(task=napalm_get, getters=["facts"])
    print_result(agg_result)


if __name__ == "__main__":
    main()
