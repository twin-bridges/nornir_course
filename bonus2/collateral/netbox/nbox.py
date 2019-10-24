import ipdb

from nornir import InitNornir


def transform_netbox_group_custom_field(host):
    if not host["Groups"]:
        return
    groups = host["Groups"].split()
    for group in groups:
        host.groups.append(group)


def main():
    nr = InitNornir(config_file="config.yaml")
    ipdb.set_trace()
    # return only to "use" nr variable to appease linters!
    return nr


if __name__ == "__main__":
    main()
