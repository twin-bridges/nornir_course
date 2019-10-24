from datetime import datetime

from nornir import InitNornir
from nornir.core.inventory import Host
from nornir.core.filter import F
from nornir.core.task import AggregatedResult, MultiResult, Result, Task
from nornir.plugins.tasks.networking import netmiko_send_command


class PrintResult:
    def task_started(self, task: Task) -> None:
        self.parent_task_start = datetime.now()

    def task_completed(self, task: Task, result: AggregatedResult) -> None:
        parent_task_end = datetime.now()
        print(
            f">>> Parent Task Completed! Duration: {parent_task_end - self.parent_task_start}"
        )

    def task_instance_started(self, task: Task, host: Host) -> None:
        task.task_start = datetime.now()

    def task_instance_completed(
        self, task: Task, host: Host, result: MultiResult
    ) -> None:
        task_end = datetime.now()
        print(
            f"  - {host.name} Result: - {result.result}\n\t"
            f">>> Duration: {task_end - task.task_start}"
        )

    def subtask_instance_started(self, task: Task, host: Host) -> None:
        pass

    def subtask_instance_completed(
        self, task: Task, host: Host, result: MultiResult
    ) -> None:
        pass


def get_version(task: Task) -> Result:
    result = task.run(task=netmiko_send_command, command_string="show version")
    return Result(host=task.host, result=result)


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="eos"))
    nr_with_processors = nr.with_processors([PrintResult()])

    nr_with_processors.run(task=get_version, num_workers=2)


if __name__ == "__main__":
    main()
