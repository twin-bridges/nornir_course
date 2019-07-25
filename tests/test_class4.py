import os
import subprocess
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks import networking


NORNIR_LOGGING = {"enabled": False}


def gen_inventory_dict(base_path):
    """Dynamically create an inventory dictionary using exercise path."""
    # BASE_PATH = "../class1/exercises/exercise1/"
    NORNIR_HOSTS = f"{base_path}/hosts.yaml"
    NORNIR_GROUPS = f"{base_path}/groups.yaml"
    NORNIR_DEFAULTS = f"{base_path}/defaults.yaml"
    NORNIR_INVENTORY = {
        "plugin": "nornir.plugins.inventory.simple.SimpleInventory",
        "options": {
            "host_file": NORNIR_HOSTS,
            "group_file": NORNIR_GROUPS,
            "defaults_file": NORNIR_DEFAULTS,
        },
    }
    return NORNIR_INVENTORY


def subprocess_runner(cmd_list, exercise_dir):
    with subprocess.Popen(
        cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=exercise_dir
    ) as proc:
        std_out, std_err = proc.communicate()
    return (std_out.decode(), std_err.decode(), proc.returncode)


def remove_ex2_flash_files():
    # prep to ensure test files do not exist on devices
    nornir_inventory = gen_inventory_dict("~/nornir_inventory/")
    nr = InitNornir(inventory=nornir_inventory, logging=NORNIR_LOGGING)
    eos = nr.filter(F(groups__contains="eos"))
    ios = nr.filter(F(groups__contains="ios"))

    # remove test files from eos flash
    eos.run(task=networking.netmiko_send_command, command_string="terminal dont-ask")
    eos.run(
        task=networking.netmiko_send_command, command_string="delete flash:arista.txt"
    )

    # remove test files from ios flash
    ios.run(
        task=networking.netmiko_send_command,
        use_timing=True,
        command_string="delete flash:cisco.txt",
    )
    ios.run(task=networking.netmiko_send_command, use_timing=True, command_string="\n")
    ios.run(task=networking.netmiko_send_command, use_timing=True, command_string="\n")


def remove_ex2_local_files(base_path):
    os.remove(f"{base_path}ios/cisco3_cisco.txt")
    os.remove(f"{base_path}ios/cisco4_cisco.txt")
    os.remove(f"{base_path}eos/arista1_arista.txt")
    os.remove(f"{base_path}eos/arista2_arista.txt")
    os.remove(f"{base_path}eos/arista3_arista.txt")
    os.remove(f"{base_path}eos/arista4_arista.txt")


def remove_vlan():
    nornir_inventory = gen_inventory_dict("~/nornir_inventory/")
    nr = InitNornir(inventory=nornir_inventory, logging=NORNIR_LOGGING)
    ex3_hosts = nr.filter(F(groups__contains="eos") | F(groups__contains="nxos"))

    ex3_hosts.run(task=networking.netmiko_send_config, config_commands=["no vlan 123"])


def remove_loopback():
    nornir_inventory = gen_inventory_dict("~/nornir_inventory/")
    nr = InitNornir(inventory=nornir_inventory, logging=NORNIR_LOGGING)
    ex5_host = nr.filter(name="arista4")

    ex5_host.run(
        task=networking.netmiko_send_config,
        config_commands=["no interface loopback 123"],
    )


def test_class4_ex1a():
    base_path = "../class4/exercises/exercise1/"
    cmd_list = ["python", "exercise1a.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("Next hop: 10.220.88.1") == 2
    assert "* cisco3 ** changed : False" in std_out
    assert "* cisco4 ** changed : False" in std_out
    assert std_err == ""


def test_class4_ex1b():
    base_path = "../class4/exercises/exercise1/"
    cmd_list = ["python", "exercise1b.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("Command not executed on platform eos") == 4
    assert std_out.count("Command not executed on platform nxos") == 2
    assert "Next hop:  10.220.88.1 via vlan.0" in std_out
    assert "Next hop: 10.220.88.1" in std_out
    assert std_err == ""


def test_class4_ex2a():
    base_path = "../class4/exercises/exercise2/"
    cmd_list = ["python", "exercise2a.py"]

    remove_ex2_flash_files()

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("True") == 18
    assert std_out.count("False") == 6
    assert std_out.count("---- netmiko_file_transfer **") == 6
    assert std_err == ""


def test_class4_ex2b():
    base_path = "../class4/exercises/exercise2/"
    cmd_list = ["python", "exercise2b.py"]

    remove_ex2_flash_files()

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("---- netmiko_file_transfer **") == 12
    assert os.path.exists(f"{base_path}ios/get_cisco.txt")
    assert os.path.exists(f"{base_path}eos/get_arista.txt")
    assert std_err == ""

    os.remove(f"{base_path}eos/get_arista.txt")
    os.remove(f"{base_path}ios/get_cisco.txt")


def test_class4_ex2c():
    base_path = "../class4/exercises/exercise2/"
    cmd_list = ["python", "exercise2c.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert os.path.exists(f"{base_path}ios/cisco3_cisco.txt")
    assert os.path.exists(f"{base_path}ios/cisco4_cisco.txt")
    assert os.path.exists(f"{base_path}eos/arista1_arista.txt")
    assert os.path.exists(f"{base_path}eos/arista2_arista.txt")
    assert os.path.exists(f"{base_path}eos/arista3_arista.txt")
    assert os.path.exists(f"{base_path}eos/arista4_arista.txt")
    assert std_err == ""

    remove_ex2_local_files(base_path)


def test_class4_ex3a():
    base_path = "../class4/exercises/exercise3/"
    cmd_list = ["python", "exercise3a.py"]

    exercise_hosts = ["arista1", "arista2", "arista3", "arista4", "nxos1", "nxos2"]

    remove_vlan()

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    for host in exercise_hosts:
        if host.startswith("arista"):
            assert f"{host}(config)#vlan 123" in std_out
        else:
            assert f"{host}(config)# vlan 123" in std_out
    assert std_err == ""


def test_class4_ex3b():
    base_path = "../class4/exercises/exercise3/"
    cmd_list = ["python", "exercise3b.py"]

    exercise_hosts = ["arista1", "arista2", "arista3", "arista4", "nxos1", "nxos2"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("Nothing to do") == 6
    assert std_err == ""

    remove_vlan()

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    for host in exercise_hosts:
        if host.startswith("arista"):
            assert f"{host}(config)#vlan 123" in std_out
        else:
            assert f"{host}(config)# vlan 123" in std_out
    assert std_err == ""


def test_class4_ex3c():
    base_path = "../class4/exercises/exercise3/"
    cmd_list = ["python", "exercise3c.py"]

    exercise_hosts = ["arista1", "arista2", "arista3", "arista4", "nxos1", "nxos2"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("Vlan 123 with name ntp_vlan exists, nothing to do!") == 6
    assert std_err == ""

    remove_vlan()

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    for host in exercise_hosts:
        if host.startswith("arista"):
            assert f"{host}(config)#vlan 123" in std_out
        else:
            assert f"{host}(config)# vlan 123" in std_out
    assert std_err == ""


def test_class4_ex4a():
    base_path = "../class4/exercises/exercise4/"
    cmd_list = ["python", "exercise4a.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("False") == 18
    assert std_err == ""

    remove_vlan()

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("+!\n+vlan 123\n+   name ntp_vlan") == 4
    assert std_out.count("vlan 123\n  name ntp_vlan") == 2
    assert std_err == ""


def test_class4_ex4b():
    base_path = "../class4/exercises/exercise4/"
    cmd_list = ["python", "exercise4b.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("False") == 18
    assert std_err == ""

    remove_vlan()

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("+!\n+vlan 123\n+   name ntp_vlan") == 4
    assert std_out.count("vlan 123\n  name ntp_vlan") == 2
    assert std_err == ""


def test_class4_ex5a():
    base_path = "../class4/exercises/exercise5/"
    cmd_list = ["python", "exercise5a.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "! Command: show running-config" in std_out
    assert std_err == ""


def test_class4_ex5b():
    base_path = "../class4/exercises/exercise5/"
    cmd_list = ["python", "exercise5b.py"]

    remove_loopback()

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "+interface Loopback123\n+   description verycoolloopback\n+!" in std_out
    assert std_err == ""


def test_class4_ex5c():
    base_path = "../class4/exercises/exercise5/"
    cmd_list = ["python", "exercise5c.py"]

    remove_loopback()

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "+interface Loopback123\n+   description verycoolloopback\n+!" in std_out
    assert "-interface Loopback123\n-   description verycoolloopback\n-!" in std_out
    assert std_err == ""
