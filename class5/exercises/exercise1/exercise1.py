from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks import networking
from nornir.plugins.functions.text import print_result


def set_snmp_id(task):
    if task.host.platform == "eos":
        snmp_config = [f"snmp chassis-id {task.host['snmp_id']}"]
    elif task.host.platform == "ios":
        snmp_config = [f"snmp-server chassis-id {task.host['snmp_id']}"]
    else:
        return False
    task.run(task=networking.netmiko_send_config, config_commands=snmp_config)


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="eos") | F(groups__contains="ios"))
    agg_result = nr.run(task=set_snmp_id)
    print_result(agg_result)


if __name__ == "__main__":
    main()
