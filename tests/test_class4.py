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

    # remove test files from eos flash
    eos.run(task=networking.netmiko_send_command, command_string="terminal dont-ask")
    eos.run(
        task=networking.netmiko_send_command, command_string="delete flash:arista_test.txt"
    )


def remove_ex2_local_files(base_path):
    """Remove files (if they exist)."""
    files_to_remove = [
        f"{base_path}/eos/arista1-saved.txt",
        f"{base_path}/eos/arista2-saved.txt",
        f"{base_path}/eos/arista3-saved.txt",
        f"{base_path}/eos/arista4-saved.txt",
    ]
    for a_file in files_to_remove:
        try:
            os.remove(a_file)
        except FileNotFoundError:
            pass
    return None


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
    assert std_out.count("uptime") == 4
    assert std_out.count("Uptime") == 4
    assert std_out.count("System booted") == 1
    assert std_err == ""


def test_class4_ex1b():
    base_path = "../class4/exercises/exercise1/"
    cmd_list = ["python", "exercise1b.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "srx2: device rebooted recently" in std_out
    assert std_out.count("uptime") == 8
    assert std_err == ""


def test_class4_ex2a():
    base_path = "../class4/exercises/exercise2/"
    cmd_list = ["python", "exercise2a.py"]

    remove_ex2_flash_files()

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("True") == 12
    assert std_out.count("False") == 4
    assert std_out.count("---- netmiko_file_transfer **") == 4
    assert std_err == ""


def test_class4_ex2b():
    base_path = "../class4/exercises/exercise2/"
    cmd_list = ["python", "exercise2b.py"]

    remove_ex2_flash_files()

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("nornir test file") == 4
    assert std_err == ""


def test_class4_ex2c():
    base_path = "../class4/exercises/exercise2"
    cmd_list = ["python", "exercise2c.py"]

    remove_ex2_local_files(base_path)

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert os.path.exists(f"{base_path}/eos/arista1-saved.txt")
    assert os.path.exists(f"{base_path}/eos/arista2-saved.txt")
    assert os.path.exists(f"{base_path}/eos/arista3-saved.txt")
    assert os.path.exists(f"{base_path}/eos/arista4-saved.txt")
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
    assert std_out.count("onfiguration already correct") == 6
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


#def test_class4_ex5a():
#    base_path = "../class4/exercises/exercise5/"
#    cmd_list = ["python", "exercise5a.py"]
#
#    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
#    assert return_code == 0
#    assert "! Command: show running-config" in std_out
#    assert std_err == ""
#
#
#def test_class4_ex5b():
#    base_path = "../class4/exercises/exercise5/"
#    cmd_list = ["python", "exercise5b.py"]
#
#    remove_loopback()
#
#    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
#    assert return_code == 0
#    assert "+interface Loopback123\n+   description verycoolloopback\n+!" in std_out
#    assert std_err == ""
#
#
#def test_class4_ex5c():
#    base_path = "../class4/exercises/exercise5/"
#    cmd_list = ["python", "exercise5c.py"]
#
#    remove_loopback()
#
#    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
#    assert return_code == 0
#    assert "+interface Loopback123\n+   description verycoolloopback\n+!" in std_out
#    assert "-interface Loopback123\n-   description verycoolloopback\n-!" in std_out
#    assert std_err == ""
