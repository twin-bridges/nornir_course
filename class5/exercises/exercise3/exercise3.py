from nornir import InitNornir
from nornir_utils.plugins.tasks.data import load_yaml


def junos_acl(task):

    # Load the YAML-ACL entries
    in_yaml = task.run(task=load_yaml, file="acl.yaml")
    in_yaml = in_yaml[0].result
    rules = []

    for acl_name, acl_entries in in_yaml.items():
        for acl_entry in acl_entries:
            rules.append(
                f"set firewall family inet filter {acl_name} term {acl_entry['term_name']} "
                f"from protocol {acl_entry['protocol']}"
            )
            rules.append(
                f"set firewall family inet filter {acl_name} term {acl_entry['term_name']} "
                f"from destination-port {acl_entry['destination_port']}"
            )
            rules.append(
                f"set firewall family inet filter {acl_name} term {acl_entry['term_name']} "
                f"from destination-address {acl_entry['destination_address']}"
            )
            rules.append(
                f"set firewall family inet filter {acl_name} term {acl_entry['term_name']} "
                f"then {acl_entry['state']}"
            )

    print()
    print("#" * 80)
    for rule in rules:
        print(rule)
    print("#" * 80)
    print()


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="srx2")
    nr.run(task=junos_acl)


if __name__ == "__main__":
    main()
