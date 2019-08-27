from nornir import InitNornir
from nornir.plugins.tasks import text
from nornir.plugins.tasks import data


ACL_TEMPLATE = """{%- for acl, rules in acls.items() %}
  {%- for entry in rules %}

set firewall family inet filter {{ acl }} term {{ entry['term_name'] }} from protocol {{ entry['protocol'] }}
set firewall family inet filter {{ acl }} term {{ entry['term_name'] }} from destination-port {{ entry['destination_port'] }}
set firewall family inet filter {{ acl }} term {{ entry['term_name'] }} from destination-address {{ entry['destination_address'] }}
set firewall family inet filter {{ acl }} term {{ entry['term_name'] }} then {{ entry['state'] }}
  {%- endfor %}
{%- endfor %}"""  # noqa


def junos_acl(task):
    in_yaml = task.run(task=data.load_yaml, file=f"acl.yaml")
    in_yaml = in_yaml[0].result
    multi_result = task.run(
        task=text.template_string, template=ACL_TEMPLATE, acls=in_yaml
    )

    print()
    print("#" * 80, end="")
    print(multi_result[0].result)
    print("#" * 80)
    print()


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="srx2")
    nr.run(task=junos_acl)


if __name__ == "__main__":
    main()
