from nornir import InitNornir
from nornir_netmiko.tmp_glue import load_yaml
from nornir_netmiko.tmp_glue import template_file
 


def junos_acl(task):
    in_yaml = task.run(task=load_yaml, file="acl.yaml")
    in_yaml = in_yaml[0].result
    multi_result = task.run(
        task=template_file, template="acl.j2", path=".", acls=in_yaml
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
