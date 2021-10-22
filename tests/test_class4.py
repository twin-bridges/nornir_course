import os
from pathlib import Path
import pytest

from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko import netmiko_send_command
from nornir_netmiko import netmiko_send_config

from utilities import subprocess_runner
from utilities import gen_inventory_dict

NORNIR_LOGGING = {"enabled": False}

TEST_CASES = [
    ("../class4/collateral/custom_tasks_and_results/custom_tasks_p1.py", None),
    ("../class4/collateral/custom_tasks_and_results/custom_tasks_p2.py", None),
    ("../class4/collateral/custom_tasks_and_results/custom_tasks_p3.py", None),
    ("../class4/collateral/custom_tasks_and_results/custom_tasks_p4.py", None),
    ("../class4/collateral/netmiko_file_copy/test_copy1.py", None),
    ("../class4/collateral/netmiko_file_copy/test_copy2.py", None),
    ("../class4/collateral/netmiko_file_copy/test_copy3.py", None),
    ("../class4/collateral/netmiko_file_copy/test_get.py", None),
    ("../class4/collateral/netmiko_config/test_cfg1.py", None),
    ("../class4/collateral/netmiko_config/test_cfg2.py", None),
    ("../class4/collateral/netmiko_config/test_cfg3.py", None),
    ("../class4/collateral/netmiko_config/cfg_cleanup.py", None),
    ("../class4/collateral/napalm_configure/napalm_configure.py", None),
]


@pytest.mark.parametrize("test_case_dir, inventory_check", TEST_CASES)
def test_runner_collateral(test_case_dir, inventory_check):
    path_obj = Path(test_case_dir)
    script = path_obj.name
    script_dir = path_obj.parents[0]

    # Inventory Checks
    if inventory_check is None:
        pass

    # Script Check
    cmd_list = ["python", script]
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=script_dir)
    assert return_code == 0
    assert std_err == ""


def remove_ex2_flash_files():
    # prep to ensure test files do not exist on devices
    nornir_inventory = gen_inventory_dict("~/nornir_inventory/")
    nr = InitNornir(inventory=nornir_inventory, logging=NORNIR_LOGGING)
    eos = nr.filter(F(groups__contains="eos"))

    # remove test files from eos flash
    eos.run(task=netmiko_send_command, command_string="terminal dont-ask")
    eos.run(task=netmiko_send_command, command_string="delete flash:arista_zzzzz.txt")


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

    ex3_hosts.run(task=netmiko_send_config, config_commands=["no vlan 123"])


def remove_loopback():
    nornir_inventory = gen_inventory_dict("~/nornir_inventory/")
    nr = InitNornir(inventory=nornir_inventory, logging=NORNIR_LOGGING)
    ex5_host = nr.filter(name="arista4")
    ex5_host.run(
        task=netmiko_send_config, config_commands=["no interface loopback 123"]
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

    # Ensure loopback is not currently configured
    remove_loopback()

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "+interface Loopback123\n+   description verycoolloopback\n+!" in std_out
    assert "-interface Loopback123\n-   description verycoolloopback\n-!" in std_out
    assert std_err == ""
