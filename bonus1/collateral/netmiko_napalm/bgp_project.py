import time
from nornir import InitNornir
from nornir.core.filter import F

from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_netmiko import netmiko_send_command


DEBUG = False


def render_configs(task):
    """Generate BGP configs from Jinja2 template."""
    template = "bgp.j2"
    result = task.run(task=template_file, template=template, path=".", **task.host)
    rendered_config = result[0].result
    task.host["rendered_config"] = rendered_config

    if DEBUG:
        print()
        print("*" * 40)
        print(task.host.name)
        print("-" * 8)
        print(rendered_config)
        print("*" * 40)
        print()


def napalm_merge_cfg(task):
    """Send BGP configs to devices using napalm-merge."""
    host = task.host
    bgp_config = host["rendered_config"]
    multi_result = task.run(
        task=napalm_configure, configuration=bgp_config, dry_run=False
    )

    if DEBUG:
        print()
        print("*" * 40)
        print(host.name)
        print("-" * 8)
        print(multi_result[0].diff)
        print("*" * 40)
        print()


def verify_bgp(task):
    multi_result = task.run(
        task=netmiko_send_command, command_string="show ip bgp summary | inc Estab"
    )
    output = multi_result[0].result
    bgp_peers = output.count("Estab")
    multi_result = task.run(
        task=netmiko_send_command, command_string="show ip route bgp | inc Vlan1"
    )
    output = multi_result[0].result
    bgp_route_count = output.count("Vlan1")

    if bgp_peers != 3:
        raise ValueError(f"Incorrect number of BGP peers: {bgp_peers}")
    elif bgp_route_count != 3:
        raise ValueError(f"Incorrect number of BGP routes: {bgp_route_count}")
    else:
        # Hide the router command output
        task.results.pop()
        task.results.pop()

        # Print a verification message
        msg = f"""
****************************************
Device: {task.host.name}
--------
Verified BGP Peer Count...OK
Verified BGP Route Count...OK
****************************************

"""
        return msg


if __name__ == "__main__":
    with InitNornir(config_file="config.yaml") as nr:
        eos_filter = F(groups__contains="eos")
        eos_devices = nr.filter(eos_filter)
        result = eos_devices.run(task=render_configs)
        print_result(result)
        result = eos_devices.run(task=napalm_merge_cfg)
        print_result(result)
        # BGP might take some time to reach Established State
        print("-" * 80)
        print("Sleeping 60 Seconds...")
        print("-" * 80)
        time.sleep(60)
        result = eos_devices.run(task=verify_bgp)
        print_result(result)
