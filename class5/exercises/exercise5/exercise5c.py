from nornir import InitNornir
from nornir.core.filter import F
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.files import write_file
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get, napalm_configure


def render_configurations(task):
    bgp = task.run(task=template_file, template="bgp.j2", path="nxos/", **task.host)
    intf = task.run(
        task=template_file, template="routed_int.j2", path="nxos/", **task.host
    )
    task.host["bgp_config"] = bgp.result
    task.host["intf_config"] = intf.result


def write_configurations(task):
    task.run(
        task=write_file,
        filename=f"rendered_configs/{task.host}_bgp",
        content=task.host["bgp_config"],
    )
    task.run(
        task=write_file,
        filename=f"rendered_configs/{task.host}_intf",
        content=task.host["intf_config"],
    )


def deploy_configurations(task):
    task.run(task=napalm_configure, configuration=task.host["intf_config"])
    task.run(task=napalm_configure, configuration=task.host["bgp_config"])


def validate_bgp(task):
    bgp_result = task.run(task=napalm_get, getters=["bgp_neighbors"])
    print()
    print("*" * 80)
    if not bgp_result.result["bgp_neighbors"]["global"]["peers"][task.host["bgp_peer"]][
        "is_up"
    ]:
        print("Failed BGP peer is not up...")
    else:
        print("It's alive...success BGP is up!")
    print("*" * 80)
    print()


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="nxos"))
    agg_result = nr.run(task=render_configurations)
    print_result(agg_result)
    agg_result = nr.run(task=write_configurations)
    print_result(agg_result)
    agg_result = nr.run(task=deploy_configurations)
    print_result(agg_result)
    nr.run(task=validate_bgp)


if __name__ == "__main__":
    main()
