from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_file_transfer


def delete_file(task, filename):
    """
    nxos1# del bootflash:/testx.txt
    Do you want to delete "/testx.txt" ? (yes/no/abort)   [y] y
    """

    # Connection should already exist at this point.
    net_connect = task.host.get_connection("netmiko", task.nornir.config)

    # Delete the file
    file_system = "bootflash:"
    cmd = f"del {file_system}/{filename}"
    output = net_connect.send_command_timing(
        cmd, strip_prompt=False, strip_command=False
    )
    if "Do you want to delete" and filename in output:
        output += net_connect.send_command_timing(
            "y", strip_prompt=False, strip_command=False
        )

    # Verify the file is actually gone.
    cmd = f"dir {filename}"
    new_output = net_connect.send_command_timing(
        cmd, strip_prompt=False, strip_command=False
    )
    if "No such file or directory" not in new_output:
        raise ValueError("The file was not properly deleted")
    return output


if __name__ == "__main__":
    with InitNornir(config_file="config.yaml") as nr:
        nr = nr.filter(name="nxos1")

        # Transfer test file to NX-OS devices
        source_file = "bonus1_ex4.txt"
        dest_file = source_file
        agg_result = nr.run(
            netmiko_file_transfer,
            source_file=source_file,
            dest_file=dest_file,
            direction="put",
        )
        print_result(agg_result)

        agg_result = nr.run(task=delete_file, filename=source_file)
        print_result(agg_result)
