import pdbr  # noqa
from nornir import InitNornir
from nornir_netmiko import netmiko_send_command


def test_task(task):
    print(task)
    print(task.host)
    results = task.run(task=netmiko_send_command, command_string="show ip int brief")
    print(results)


if __name__ == "__main__":

    # pdbr.set_trace()

    # config.yaml is using the "serial" runner
    nr = InitNornir(config_file="config.yaml")
    results = nr.run(task=test_task)
    print(nr)
