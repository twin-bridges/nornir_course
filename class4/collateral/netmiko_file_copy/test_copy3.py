from nornir import InitNornir
from nornir_netmiko import netmiko_file_transfer


def file_copy(task):
    # Obtain the group_name
    group_name = task.host.groups[0].name

    # Set the filename based on the platform (ios, eos, et cetera)
    base_file = "test_file1.txt"
    source_file = f"{group_name}/{base_file}"
    dest_file = base_file

    # Transfer the file
    results = task.run(
        netmiko_file_transfer,
        source_file=source_file,
        dest_file=dest_file,
        direction="put",
    )

    print()
    print("-" * 40)
    print(task.host)
    print(source_file)
    print()
    if results[0].changed is False:
        print("File not transferred: correct file is already on the device")
    else:
        print("File transferred")

    if results[0].result is True:
        print("Remote file exists and is correct")
    print("-" * 40)
    print()


if __name__ == "__main__":

    nr = InitNornir(config_file="config.yaml")
    results = nr.run(task=file_copy)
