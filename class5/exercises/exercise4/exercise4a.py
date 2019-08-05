from nornir import InitNornir
from nornir.plugins.tasks import text
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import data


ACL_TEMPLATE = """{% for acl, rules in acls.items() %}
{% for entry in rules %}
set firewall family inet filter {{ acl }} term {{ entry['rule_name'] }} from protocol {{ entry['from_protocol'] }}
set firewall family inet filter {{ acl }} term {{ entry['rule_name'] }} from port {{ entry['from_port'] }}
set firewall family inet filter {{ acl }} term {{ entry['rule_name'] }} from destination-address {{ entry['to_address'] }}
set firewall family inet filter {{ acl }} term {{ entry['rule_name'] }} then {{ entry['state'] }}
{% endfor %}
{% endfor %}"""  # noqa


def junos_acl(task):
    in_yaml = task.run(task=data.load_yaml, file=f"acl.yaml")
    in_yaml = in_yaml[0].result
    task.run(task=text.template_string, template=ACL_TEMPLATE, acls=in_yaml)


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="srx2")
    agg_result = nr.run(task=junos_acl)
    print_result(agg_result)


if __name__ == "__main__":
    main()
