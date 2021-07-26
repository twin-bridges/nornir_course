from nornir import InitNornir
from nornir.core.filter import F
from nornir.core.task import Result
from nornir_netmiko import netmiko_send_command


class SimpleProcessor:
    def task_started(self, task):
        pass

    def task_completed(self, task, result):
        pass

    def task_instance_started(self, task, host):
        print(f"starting task instance for host {task.host}")

    def task_instance_completed(self, task, host, result):
        print(f"task instance completed for host {task.host}")

    def subtask_instance_started(self, task, host):
        pass

    def subtask_instance_completed(self, task, host, result):
        pass


def get_version(task):
    result = task.run(task=netmiko_send_command, command_string="show version")
    return Result(host=task.host, result=result)


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="eos"))
    nr_with_processors = nr.with_processors([SimpleProcessor()])
    nr_with_processors.run(task=get_version)


if __name__ == "__main__":
    main()
