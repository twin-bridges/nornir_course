from nornir import InitNornir
from nornir.plugins.tasks import networking
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import data


def junos_acl(task):
    in_yaml = task.run(task=data.load_yaml, file=f"acl.yaml")
    in_yaml = in_yaml[0].result
    acl_names = in_yaml.keys()
    rules = []
    for acl in acl_names:
        for acl_entry in in_yaml[acl]:
            rules.append(
                f"set firewall family inet filter {acl} term {acl_entry['rule_name']} "
                f"from protocol {acl_entry['from_protocol']}"
            )
            rules.append(
                f"set firewall family inet filter {acl} term {acl_entry['rule_name']} "
                f"from port {acl_entry['from_port']}"
            )
            rules.append(
                f"set firewall family inet filter {acl} term {acl_entry['rule_name']} "
                f"from destination-address {acl_entry['to_address']}"
            )
            rules.append(
                f"set firewall family inet filter {acl} term {acl_entry['rule_name']} "
                f"then {acl_entry['state']}"
            )
    task.run(task=networking.netmiko_send_config, config_commands=rules)


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="srx2")
    agg_result = nr.run(task=junos_acl)
    print_result(agg_result)


if __name__ == "__main__":
    main()
