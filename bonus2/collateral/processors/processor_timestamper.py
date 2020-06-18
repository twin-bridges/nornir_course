from datetime import datetime

from nornir import InitNornir
from nornir.core.filter import F
from nornir.core.task import Result
from nornir_netmiko import netmiko_send_command


class PrintResult:
    def task_started(self, task):
        self.parent_task_start = datetime.now()

    def task_completed(self, task, result):
        parent_task_end = datetime.now()
        print(
            f">>> Parent Task Completed! Duration: {parent_task_end - self.parent_task_start}"
        )

    def task_instance_started(self, task, host):
        task.task_start = datetime.now()

    def task_instance_completed(self, task, host, result):
        task_end = datetime.now()
        print(
            f"  - {host.name} Result: - {result.result}\n\t"
            f">>> Duration: {task_end - task.task_start}"
        )

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
    nr_with_processors = nr.with_processors([PrintResult()])
    nr_with_processors.run(task=get_version)


if __name__ == "__main__":
    main()
