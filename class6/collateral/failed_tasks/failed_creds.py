from nornir import InitNornir
from nornir_netmiko import netmiko_send_config
from nornir.core.exceptions import NornirSubTaskError


def netmiko_configure(task):
    # Note, you can control whether the task.run exception shows up on standard error
    # by enabling/disabling logging. If logging is enabled, it will show up in the
    # log, but not on std_err.
    try:
        print(task.host["loopback_config"])
        task.run(task=netmiko_send_config, config_commands=["interface lopback 123"])
    except NornirSubTaskError:
        print("sad, we hit a subtask error.... :(")
    except Exception as e:
        print("we hit a non Nornir subtask error... my bad!")


def main():
    nr = InitNornir(config_file="config_creds.yaml")
    nr = nr.filter(name="cisco3")
    agg_result = nr.run(task=netmiko_configure)
    # print(agg_result["cisco3"].result)
    print("Complete!")


if __name__ == "__main__":
    main()
