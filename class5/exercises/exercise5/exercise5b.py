from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks import text
from nornir.plugins.tasks import files
from nornir.plugins.functions.text import print_result


def render_configurations(task):
    bgp = task.run(
        task=text.template_file, template="bgp.j2", path="nxos/", **task.host
    )
    intf = task.run(
        task=text.template_file, template="routed_int.j2", path="nxos/", **task.host
    )
    task.host["bgp_config"] = bgp.result
    task.host["intf_config"] = intf.result


def write_configurations(task):
    task.run(
        task=files.write_file,
        filename=f"rendered_configs/{task.host}_bgp",
        content=task.host["bgp_config"],
    )
    task.run(
        task=files.write_file,
        filename=f"rendered_configs/{task.host}_intf",
        content=task.host["intf_config"],
    )


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="nxos"))
    agg_result = nr.run(task=render_configurations)
    print_result(agg_result)
    agg_result = nr.run(task=write_configurations)
    print_result(agg_result)


if __name__ == "__main__":
    main()
