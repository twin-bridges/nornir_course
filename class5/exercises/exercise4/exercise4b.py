from nornir import InitNornir
from nornir.plugins.tasks import text
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import data


def junos_acl(task):
    in_yaml = task.run(task=data.load_yaml, file=f"acl.yaml")
    in_yaml = in_yaml[0].result
    task.run(task=text.template_file, template="acl.j2", path=".", acls=in_yaml)


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="srx2")
    agg_result = nr.run(task=junos_acl)
    print_result(agg_result)


if __name__ == "__main__":
    main()
