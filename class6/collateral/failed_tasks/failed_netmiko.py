from nornir import InitNornir
from nornir_netmiko import netmiko_send_config


def netmiko_configure(task):
    output = task.run(
        task=netmiko_send_config, config_commands=["interface lopback 123"]
    )
    if "% Invalid input detected" in output.result:
        raise ValueError("Bad things happening!")


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="cisco3")
    agg_result = nr.run(task=netmiko_configure)
    print(agg_result["cisco3"].result)


if __name__ == "__main__":
    main()
