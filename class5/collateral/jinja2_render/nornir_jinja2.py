from nornir import InitNornir
from nornir.plugins.tasks import text


TEMPLATE_STR = """interface loopback{{ int_num }}
  description {{ descr | reverse }}
  no shut"""


def my_task(task):
    result = task.run(
        task=text.template_file, template="interfaces.j2", path=".", **task.host
    )
    print(result[0].result)


def main():
    nr = InitNornir(config_file="config.yaml", logging={"enabled": False})
    nr = nr.filter(name="srx2")
    nr.run(task=my_task)


if __name__ == "__main__":
    main()
