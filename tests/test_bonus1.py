import os
from pathlib import Path
import subprocess


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
    assert (
        std_out.count("{'ntp_servers': {'130.126.24.24': {}, '152.2.21.1': {}}}") == 2
    )
    assert std_err == ""


def test_class_bonus1_ex2a():
    base_path = "../bonus1/exercises/exercise2/"
    cmd_list = ["python", "exercise2a.py"]

    os.environ["PYTHONWARNINGS"] = "ignore::Warning"
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("Arista vEOS") == 4
    assert std_out.count("Cisco IOS XE Software, Version 16.08.01") == 2
    assert std_out.count("Cisco Nexus Operating System (NX-OS) Software") == 2
    assert "Hostname: srx2" in std_out
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
    assert std_out.count("srx2") == 2
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
    assert "['RESPONSE_RETURN', 'RETURN', 'TELNET_RETURN'" in std_out
    assert "nxos1#" in std_out
    assert std_err == ""
