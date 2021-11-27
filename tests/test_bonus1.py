import os
from pathlib import Path
import pytest

from utilities import subprocess_runner
from utilities import gen_inventory_dict

import nornir
from nornir import InitNornir


NORNIR_LOGGING = {"enabled": False}

TEST_CASES = [
    ("../bonus1/collateral/ansible_inventory/ansible_inventory.py", None),
    ("../bonus1/collateral/ansible_inventory/ansible_inventory2.py", None),
    ("../bonus1/collateral/transform_function/simple/nornir_transform.py", None),
    ("../bonus1/collateral/transform_function/simple/nornir_transform2.py", None),
    ("../bonus1/collateral/transform_function/ansible/nornir_transform.py", None),
    ("../bonus1/collateral/transform_function/ansible/nornir_transform2.py", None),
    ("../bonus1/collateral/netmiko_direct_task/netmiko_direct.py", None),
    ("../bonus1/collateral/netmiko_prompting/netmiko_prompting.py", None),
    ("../bonus1/collateral/netmiko_telnet/netmiko_telnet.py", None),
    ("../bonus1/collateral/netmiko_ssh_keys/netmiko_ssh_keys.py", None),
    ("../bonus1/collateral/netmiko_ssh_proxy/netmiko_proxy.py", None),
    ("../bonus1/collateral/napalm_direct_task/napalm_direct_jnpr.py", None),
    ("../bonus1/collateral/napalm_direct_task/napalm_direct_eapi.py", None),
    ("../bonus1/collateral/napalm_nxos_ssh/napalm_nxos.py", None),
    ("../bonus1/collateral/netmiko_napalm/bgp_project.py", None),
]


@pytest.mark.parametrize("test_case_dir, inventory_check", TEST_CASES)
def test_runner_collateral(test_case_dir, inventory_check):

    # Needed for ansible-vault test
    os.environ["VAULT_PASSWORD"] = "password"

    path_obj = Path(test_case_dir)
    script = path_obj.name
    script_dir = path_obj.parents[0]

    # Inventory Checks
    if inventory_check is None:
        pass
    else:
        nornir_inventory = gen_inventory_dict(script_dir)
        nr = InitNornir(inventory=nornir_inventory, logging=NORNIR_LOGGING)
        assert isinstance(nr, nornir.core.Nornir)
        assert isinstance(nr.inventory.hosts, nornir.core.inventory.Hosts)
        if inventory_check == "all":
            assert nr.inventory.hosts
            assert nr.inventory.groups
            assert nr.inventory.defaults
        elif inventory_check == "hosts":
            assert nr.inventory.hosts
        elif inventory_check == "hosts-groups":
            assert nr.inventory.hosts
            assert nr.inventory.groups

    # Script Check
    cmd_list = ["python", script]
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=script_dir)
    assert return_code == 0
    assert std_err == ""


def test_class_bonus1_ex1a():
    base_path = "../bonus1/exercises/exercise1/"
    cmd_list = ["python", "exercise1a.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "{'nxos1': Host: nxos1, 'nxos2': Host: nxos2}" in std_out
    assert "pyclass" in std_out
    assert "bogus" in std_out
    assert "None" in std_out
    assert "8443" in std_out
    assert std_err == ""


def test_class_bonus1_ex1b():
    base_path = "../bonus1/exercises/exercise1/"
    cmd_list = ["python", "exercise1b.py"]

    os.environ["PYTHONWARNINGS"] = "ignore::Warning"
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "{'nxos1': Host: nxos1, 'nxos2': Host: nxos2}" in std_out
    assert "pyclass" in std_out
    assert "None" in std_out
    assert "8443" in std_out
    assert std_out.count("{'ntp_servers': {'") == 2
    assert std_err == ""


def test_class_bonus1_ex2a():
    base_path = "../bonus1/exercises/exercise2/"
    cmd_list = ["python", "exercise2a.py"]

    os.environ["PYTHONWARNINGS"] = "ignore::Warning"
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("Arista vEOS") == 4
    assert std_out.count("Cisco IOS XE Software, Version 16.") == 2
    assert std_out.count("Cisco Nexus Operating System (NX-OS) Software") == 2
    assert "Hostname: srx" in std_out
    assert std_err == ""


def test_class_bonus1_ex2b():
    base_path = "../bonus1/exercises/exercise2/"
    cmd_list = ["python", "exercise2b.py"]

    os.environ["PYTHONWARNINGS"] = "ignore::Warning"
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("'facts'") == 2
    assert std_err == ""


def test_class_bonus1_ex3():
    base_path = "../bonus1/exercises/exercise3/"
    cmd_list = ["python", "exercise3.py"]

    os.environ["PYTHONWARNINGS"] = "ignore::Warning"
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("netmiko_direct") == 19
    assert std_out.count("cisco3") == 2
    assert std_out.count("cisco4") == 2
    assert std_out.count("arista") == 8
    assert std_out.count("nxos") == 4
    assert std_err == ""


def test_class_bonus1_ex4():
    base_path = "../bonus1/exercises/exercise4/"
    cmd_list = ["python", "exercise4.py"]

    os.environ["PYTHONWARNINGS"] = "ignore::Warning"
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("netmiko_file_transfer") == 3
    assert std_out.count("del bootflash:/bonus1") == 1
    assert std_out.count("Do you want to delete") == 1
    assert std_out.count("nxos1") == 3
    assert std_err == ""


def test_class_bonus1_ex5a():
    base_path = "../bonus1/exercises/exercise5/"
    cmd_list = ["python", "exercise5a.py"]

    os.environ["PYTHONWARNINGS"] = "ignore::Warning"
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "hostname nxos1" in std_out
    assert "hostname nxos2" in std_out
    assert std_err == ""


def test_class_bonus1_ex5b():
    base_path = "../bonus1/exercises/exercise5/"
    cmd_list = ["python", "exercise5b.py"]

    backups_dir = Path(f"{base_path}backups")
    nxos1_checkpoint = Path(f"{base_path}backups/nxos1_checkpoint")
    nxos2_checkpoint = Path(f"{base_path}backups/nxos2_checkpoint")

    os.environ["PYTHONWARNINGS"] = "ignore::Warning"
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "hostname nxos1" in std_out
    assert "hostname nxos2" in std_out
    assert nxos1_checkpoint.is_file()
    assert nxos2_checkpoint.is_file()
    assert std_err == ""

    nxos1_checkpoint.unlink()
    nxos2_checkpoint.unlink()
    backups_dir.rmdir()


def test_class_bonus1_ex6():
    base_path = "../bonus1/exercises/exercise6/"
    cmd_list = ["python", "exercise6.py"]

    os.environ["PYTHONWARNINGS"] = "ignore::Warning"
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "<napalm.nxos_ssh.nxos_ssh.NXOSSSHDriver" in std_out
    assert "<netmiko.cisco.cisco_nxos_ssh.CiscoNxosSSH" in std_out
    assert "nxos1#" in std_out
    assert std_err == ""
