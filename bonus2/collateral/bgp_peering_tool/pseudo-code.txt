# Saving as .txt to avoid having linters complain!

from nornir import InitNornir


def config_interfaces(task):
    use netmiko send_config to config interfaces/loopbacks
    return Result


def set_config_flags(task):
    if prefix-list exist:
        pass
    else:
        configure dummy prefixlist (netmiko send_config)

    if route-maps exist:
        pass
    else:
        configure dummy prefixlist (netmiko send_config)

    bgp_base_config(napalm_merge) # merge feature bgp, router bgp 22


def get_checkpoint(task):
    chkpt = napalm_get_checkpoint()
    task.host['chkpt'] == chkpt


def render_configs(task):
    bgp_configs = template_file(blah)
    prefix_list_configs = template_file(blah)
    route_map_configs = template_file(blah)

    task.host["configs"] = myconfigs


def merge_configs(task):
    ciscoconfparse / re
    merge my configurations here!


def push_configs(task):
    napalm_merge(replace=True)


def main():
    nr = initnornir()
    nr = nr.filter(justnxos)
    nr.run(config_interfaces)


if __name__ == "__main__":
    main()

