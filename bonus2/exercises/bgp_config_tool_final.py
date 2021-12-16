import re

from ciscoconfparse import CiscoConfParse
from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file
from nornir_netmiko import netmiko_send_command, netmiko_send_config
from nornir_napalm.plugins.tasks import napalm_configure


def prepare_interfaces(task):
    """
    Nornir task to ensure routed interfaces and loopbacks are configured

    Not idempotent! Simply sends a list of configurations from the hosts inventory.

    Args:
        task: nornir task object

    """
    task.run(task=netmiko_send_config, config_commands=task.host["prep_configs"])


def ensure_config_flags(task):
    """
    Nornir task to ensure that config "flags" are present in running configuration

    Ensure that at least a single route-map starting with "RM_BGP_" a single prefix-list starting
    with "PL_BGP_" and an appropriate router bgp stanza exist in the configuration before
    capturing a checkpoint.

    As we want to be as idempotent as possible throughout this tool -- we don't want to make any
    configurations unless we absolutely need to. To wit, we check to see if there are any
    configuration items that match our required naming conventions, if so we don't need to make
    any changes. We use NAPALM merge to merge the BGP configurations as NAPALM will be idempotent
    by default!

    Args:
        task: nornir task object

    """
    route_map = task.run(
        task=netmiko_send_command, command_string="show route-map | i RM_BGP_"
    )
    if not route_map.result:
        task.run(
            task=netmiko_send_config,
            config_commands=["route-map RM_BGP_PLACEHOLDER permit 10"],
        )

    prefix_list = task.run(
        task=netmiko_send_command, command_string="show ip prefix-list | i PL_BGP_"
    )
    if not prefix_list.result:
        task.run(
            task=netmiko_send_config,
            config_commands=[
                "ip prefix-list PL_BGP_PLACEHOLDER seq 5 permit 1.1.1.1/32"
            ],
        )

    task.run(
        task=napalm_configure,
        replace=False,
        configuration=f"""
feature bgp
router bgp {task.host['bgp_config']['bgp_asn']}
""",
    )


def get_current_checkpoint(task):
    """
    Nornir task to get checkpoint of current device configuration

    Args:
        task: nornir task object

    """
    task.host.get_connection("napalm", None)
    current_checkpoint = task.host.connections[
        "napalm"
    ].connection._get_checkpoint_file()

    # Lesson videos used the above syntax, the next two commented out lines are an alternative
    # way to "grab" the underlying NAPALM connection that may be a bit easier to read.
    # napalm_conn = task.host.get_connection("napalm", task.nornir.config)
    # current_checkpoint = napalm_conn._get_checkpoint_file()

    task.host["current_checkpoint"] = current_checkpoint


def render_configurations(task):
    """
    Nornir task to render required configurations

    Renders configurations for:
        - prefix lists
        - route maps
        - bgp configuration

    Args:
        task: nornir task object

    """
    prefix_list_config = task.run(
        task=template_file, path="templates", template="prefix_lists.j2", **task.host
    )
    task.host["prefix_list_config"] = prefix_list_config.result

    route_map_config = task.run(
        task=template_file, path="templates", template="route_maps.j2", **task.host
    )
    task.host["route_map_config"] = route_map_config.result

    bgp_config = task.run(
        task=template_file, path="templates", template="bgp.j2", **task.host
    )
    task.host["bgp_router_config"] = bgp_config.result


def replace_prefix_list_config(task):
    """
    Insert final prefix list configurations into working checkpoint file

    Replaces the "ip prefix-list PL_BGP_*" lines in the previously captured checkpoint with the
    desired end state prefix-list configurations (only for prefix lists related to bgp!)

    Args:
        task: nornir task object

    """
    proposed_checkpoint = task.host["proposed_checkpoint"]
    remove_pattern = re.compile(r"^ip prefix-list PL_BGP_.+$", flags=re.M | re.I)
    prefix_list_config = task.host["prefix_list_config"]

    # find the total number of things we want to replace
    pattern_quantity = len(re.findall(remove_pattern, proposed_checkpoint))

    # replace all but one element
    if pattern_quantity > 1:
        proposed_checkpoint = re.sub(
            remove_pattern, "", proposed_checkpoint, count=pattern_quantity - 1
        )

    # replace final remaining pattern element with desired end config
    proposed_checkpoint = re.sub(
        remove_pattern, prefix_list_config, proposed_checkpoint
    )
    task.host["proposed_checkpoint"] = proposed_checkpoint


def replace_route_map_config(task):
    """
    Insert final route map configurations into working checkpoint file

    Replaces the "ip prefix-list RM_BGP_*" lines in the previously captured checkpoint with the
    desired end state route-map configurations (only for route maps related to bgp!)

    Args:
        task: nornir task object

    """
    proposed_checkpoint = task.host["proposed_checkpoint"]
    remove_pattern = re.compile(
        r"^route-map RM_BGP_.+$\n(?:^  .+$\n)*", flags=re.M | re.I
    )
    route_map_config = task.host["route_map_config"]

    # find the total number of things we want to replace
    pattern_quantity = len(re.findall(remove_pattern, proposed_checkpoint))

    # replace all but one element
    if pattern_quantity > 1:
        proposed_checkpoint = re.sub(
            remove_pattern, "", proposed_checkpoint, count=pattern_quantity - 1
        )

    # replace final remaining pattern element with desired end config
    proposed_checkpoint = re.sub(remove_pattern, route_map_config, proposed_checkpoint)
    task.host["proposed_checkpoint"] = proposed_checkpoint


# example using using regex instead of ciscoconfparse to replace bgp config
# def replace_bgp_config(task, in_progress_checkpoint):
#    pattern = re.compile(
#        r"^router bgp 22$\n(?:(^  .+)$\n)*", flags=re.M | re.I
#    )
#    bgp_config = task.host["bgp_router_config"]
#    in_progress_checkpoint = re.sub(pattern, bgp_config, in_progress_checkpoint)
#    return in_progress_checkpoint


def replace_bgp_config(task):
    """
    Insert final bgp configurations into working checkpoint file

    Replaces the entire "router bgp" configurationin the previously captured checkpoint with the
    desired end state bgp configurations

    Args:
        task: nornir task object

    """
    proposed_checkpoint = task.host["proposed_checkpoint"]
    bgp_config = task.host["bgp_router_config"]
    conf = CiscoConfParse(proposed_checkpoint.splitlines())
    bgp = conf.find_objects(f"router bgp {task.host['bgp_config']['bgp_asn']}")[0]
    conf.insert_before(
        f"router bgp {task.host['bgp_config']['bgp_asn']}", insertstr=bgp_config
    )
    bgp.delete()
    proposed_checkpoint = "\n".join(conf.ioscfg)
    task.host["proposed_checkpoint"] = proposed_checkpoint


def create_new_checkpoint(task):
    """
    Nornir task to create a proposed checkpoint file based on desired changes to config

    Args:
        task: nornir task object

    """
    task.host["proposed_checkpoint"] = task.host["current_checkpoint"]
    replace_prefix_list_config(task)
    replace_route_map_config(task)
    replace_bgp_config(task)


def push_updated_checkpoint(task, dry_run=False, diff=True):
    """
    Nornir task to deploy updated checkpoint file

    Args:
        task: nornir task object
        dry_run: True/False use dry_run or not (dry run does not push configuration changes!)
        diff: produce a diff to write to disk or not

    """
    result = task.run(
        task=napalm_configure,
        configuration=task.host["proposed_checkpoint"],
        replace=True,
        dry_run=False,
    )
    with open(f"{task.host.name}_config_diff", "w") as f:
        f.write(result.diff)


def main():
    """
    Nornir Bonus 2 "BGP Peer Configuration Utility"

    The purpose of this script is to manage all BGP configurations for the NXOS devices.
    This includes prefix lists, route maps and the actual bgp routing configurations. Other config
    items should be left alone. This tool replaces the entire configuration using NAPALM, in order
    to do that safely a configuration checkpoint is taken, and this checkpoint file is copied and
    modified to reflect the desired end state.

    """
    task_list = [
        prepare_interfaces,
        ensure_config_flags,
        get_current_checkpoint,
        render_configurations,
        create_new_checkpoint,
        push_updated_checkpoint,
    ]
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="nxos"))
    for task in task_list:
        result = nr.run(task=task)
        if any(v.changed for k, v in result.items()):
            print(f">>> Task '{result.name.upper()}' changed...")
        if result.failed:
            print(f">>> Task '{result.name.upper()}' failed... result:")
            print_result(result)
        else:
            print(f">>> Task '{result.name.upper()}' completed successfully!")


if __name__ == "__main__":
    main()
