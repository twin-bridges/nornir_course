from nornir import InitNornir


def netmiko_prompting(task):
    """
    Some commands prompt for confirmation:

    cisco4#del flash:/test_file1.txt
    Delete filename [test_file1.txt]?
    Delete bootflash:/test_file1.txt? [confirm]y
    """

    # Manually create Netmiko connection
    net_connect = task.host.get_connection("netmiko", task.nornir.config)

    filename = "test_file.txt"
    del_cmd = f"del flash:/{filename}"

    cmd_list = [del_cmd, "\n", "y"]
    output = ""

    import ipdb

    ipdb.set_trace()
    for cmd in cmd_list:
        # Use timing mode
        output += net_connect.send_command_timing(
            cmd, strip_prompt=False, strip_command=False
        )

    print()
    print("#" * 80)
    print(task.host.name)
    print("---")
    print(output)
    print("#" * 80)
    print()


if __name__ == "__main__":
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="cisco4")
    nr.run(task=netmiko_prompting, num_workers=1)
