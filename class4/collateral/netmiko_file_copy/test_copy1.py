from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_file_transfer
from nornir.core.filter import F


def file_copy(task):
    # Obtain the group_name
    group_name = task.host.groups[0]

    # Set the filename based on the platform (ios, eos, et cetera)
    base_file = "test_file.txt"
    source_file = f"{group_name}/{base_file}"
    dest_file = base_file
    # print(source_file)

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
    if results[0].changed is False:
        print("File not transferred: correct file is already on the device")

    if results[0].result is True:
        print("Remote file exists and is correct")
    print("-" * 40)
    print()


if __name__ == "__main__":

    nr = InitNornir(config_file="config.yaml")
    ios = nr.filter(F(groups__contains="ios"))
    results = ios.run(task=file_copy, num_workers=1)
