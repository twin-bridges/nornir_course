import os
import re
import subprocess
import time


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


def replace_inventory_password(filename, find_str, replace_str):
    with open(f"{filename}", "r") as f:
        contents = f.read()
        contents = re.sub(find_str, replace_str, contents, flags=re.M)
    with open(f"{filename}", "w") as f:
        f.write(contents)


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

    filename = f"{base_path}group_vars/all.yaml"
    replace_inventory_password(
        filename,
        find_str=r"^password: bogus$",
        replace_str=f"password: {os.environ['NORNIR_PASSWORD']}",
    )

    os.environ["PYTHONWARNINGS"] = "ignore::Warning"
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    replace_inventory_password(
        filename,
        find_str=rf"^password: {os.environ['NORNIR_PASSWORD']}$",
        replace_str="password: bogus",
    )

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

    filename = f"{base_path}ansible-hosts"
    replace_inventory_password(
        filename,
        find_str=r"^ansible_ssh_pass=bogus$",
        replace_str=f"ansible_ssh_pass={os.environ['NORNIR_PASSWORD']}",
    )

    os.environ["PYTHONWARNINGS"] = "ignore::Warning"
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    replace_inventory_password(
        filename,
        find_str=rf"^ansible_ssh_pass={os.environ['NORNIR_PASSWORD']}$",
        replace_str="ansible_ssh_pass=bogus",
    )

    assert return_code == 0
    assert std_out.count("Arista vEOS") == 4
    assert std_out.count("Cisco IOS XE Software, Version 16.08.01") == 2
    assert std_out.count("Cisco Nexus Operating System (NX-OS) Software") == 2
    assert "Hostname: srx2" in std_out
    assert std_err == ""


def test_class_bonus1_ex2b():
    base_path = "../bonus1/exercises/exercise2/"
    cmd_list = ["python", "exercise2b.py"]

    filename = f"{base_path}ansible-hosts"
    replace_inventory_password(
        filename,
        find_str=r"^ansible_ssh_pass=bogus$",
        replace_str=f"ansible_ssh_pass={os.environ['NORNIR_PASSWORD']}",
    )

    os.environ["PYTHONWARNINGS"] = "ignore::Warning"
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    replace_inventory_password(
        filename,
        find_str=rf"^ansible_ssh_pass={os.environ['NORNIR_PASSWORD']}$",
        replace_str="ansible_ssh_pass=bogus",
    )

    assert return_code == 0
    assert std_out.count("'pyclass'") == 9
    assert std_err == ""
