from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file
from nornir.core.exceptions import NornirSubTaskError


def render_configurations(task):
    try:
        task.run(task=template_file, template="loopback.j2", path=".", **task.host)
    except NornirSubTaskError:
        return "Templating error occurred, but its okay...."


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="nxos"))
    agg_result = nr.run(task=render_configurations)
    print_result(agg_result)


if __name__ == "__main__":
    main()
