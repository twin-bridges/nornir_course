from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.files import write_file
from nornir_napalm.plugins.tasks import napalm_configure


def render_configs(task):
    template_path = f"templates/{task.host.platform}/"
    template = "interfaces.j2"
    result = task.run(
        task=template_file, template=template, path=template_path, **task.host
    )
    rendered_config = result[0].result
    task.host["rendered_config"] = rendered_config


def write_configs(task):
    cfg_path = f"configs/{task.host.platform}/"
    filename = f"{cfg_path}{task.host.name}_interfaces"
    content = task.host["rendered_config"]
    task.run(task=write_file, filename=filename, content=content)


def deploy_configs(task):
    filename = f"configs/{task.host.platform}/{task.host.name}_interfaces"
    with open(filename, "r") as f:
        cfg = f.read()
    result = task.run(task=napalm_configure, configuration=cfg)
    return result


def main():
    nr = InitNornir(config_file="config.yaml", logging={"enabled": False})
    nr = nr.filter(F(groups__contains="ios"))
    render_result = nr.run(task=render_configs)
    print_result(render_result)
    write_result = nr.run(task=write_configs)
    print_result(write_result)
    deploy_result = nr.run(task=deploy_configs)
    print_result(deploy_result)


if __name__ == "__main__":
    main()
