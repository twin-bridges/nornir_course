from nornir import InitNornir
from nornir_jinja2.plugins.tasks import template_file
from nornir_jinja2.plugins.tasks import template_string  # noqa


TEMPLATE_STR = """interface loopback{{ int_num }}
  description {{ descr | reverse }}
  no shut"""


def my_task(task):
    # import pdbr; pdbr.set_trace()
    result = task.run(
        task=template_file, template="interfaces.j2", path=".", **task.host
    )
    print(result[0].result)


def main():
    nr = InitNornir(config_file="config.yaml", logging={"enabled": False})
    nr = nr.filter(name="srx2")
    # import pdbr; pdbr.set_trace()
    # result = nr.run(task=template_string, template=TEMPLATE_STR, int_num="1234", descr="loopy")

    # This step requires host.interfaces in interfaces.j2
    # result = nr.run(task=template_file, template="interfaces.j2", path=".")

    nr.run(task=my_task)


if __name__ == "__main__":
    main()
