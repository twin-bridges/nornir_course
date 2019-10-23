import os
import subprocess
from nornir import InitNornir


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


def test_class2_ex1a():
    base_path = "../class2/exercises/exercise1/"
    cmd_list = ["python", "exercise1a.py"]

    nornir_inventory = gen_inventory_dict(base_path)
    nr = InitNornir(inventory=nornir_inventory, logging=NORNIR_LOGGING)
    assert nr.config.core.num_workers == 20
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "20" in std_out
    assert std_err == ""


def test_class2_ex1b():
    base_path = "../class2/exercises/exercise1/"
    cmd_list = ["python", "exercise1b.py"]

    nornir_inventory = gen_inventory_dict(base_path)
    nr = InitNornir(
        inventory=nornir_inventory,
        logging=NORNIR_LOGGING,
        config_file=f"{base_path}/config.yaml",
    )
    assert nr.config.core.num_workers == 5
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "5" in std_out
    assert std_err == ""


def test_class2_ex1c():
    base_path = "../class2/exercises/exercise1/"
    cmd_list = ["python", "exercise1c.py"]

    nornir_inventory = gen_inventory_dict(base_path)
    nr = InitNornir(
        inventory=nornir_inventory,
        logging=NORNIR_LOGGING,
        config_file=f"{base_path}/config.yaml",
    )
    assert nr.config.core.num_workers == 5
    os.environ["NORNIR_CORE_NUM_WORKERS"] = "10"
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "10" in std_out
    assert std_err == ""
    del os.environ["NORNIR_CORE_NUM_WORKERS"]


def test_class2_ex1d():
    base_path = "../class2/exercises/exercise1/"
    cmd_list = ["python", "exercise1d.py"]

    nornir_inventory = gen_inventory_dict(base_path)
    nr = InitNornir(
        inventory=nornir_inventory,
        logging=NORNIR_LOGGING,
        config_file=f"{base_path}/config.yaml",
    )
    assert nr.config.core.num_workers == 5
    os.environ["NORNIR_CORE_NUM_WORKERS"] = "10"
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "15" in std_out
    assert std_err == ""
    del os.environ["NORNIR_CORE_NUM_WORKERS"]


def test_class2_ex2a():
    base_path = "../class2/exercises/exercise2/"
    cmd_list = ["python", "exercise2a.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "{'cisco3': Host: cisco3, 'cisco4': Host: cisco4}" in std_out
    assert std_err == ""


def test_class2_ex2b():
    base_path = "../class2/exercises/exercise2/"
    cmd_list = ["python", "exercise2b.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "{'cisco3': Host: cisco3, 'cisco4': Host: cisco4}" in std_out
    assert "nornir.core.task.AggregatedResult" in std_out
    assert "dict_keys(['cisco3', 'cisco4'])" in std_out
    assert 'dict_values([MultiResult: [Result: "netmiko_send_command"]' in std_out
    assert std_err == ""


def test_class2_ex2c():
    base_path = "../class2/exercises/exercise2/"
    cmd_list = ["python", "exercise2c.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "nornir.core.task.MultiResult" in std_out
    assert """Result: "netmiko_send_command""" in std_out
    assert "<method-wrapper '__iter__' of MultiResult object at " in std_out
    assert std_err == ""


def test_class2_ex2d():
    base_path = "../class2/exercises/exercise2/"
    cmd_list = ["python", "exercise2d.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "<class 'nornir.core.task.Result'>" in std_out
    assert "Failed: False" in std_out
    assert "Result: hostname cisco3" in std_out
    assert std_err == ""


def test_class2_ex3():
    base_path = "../class2/exercises/exercise3/"
    cmd_list = ["python", "exercise3.py"]

    os.environ["PYTHONWARNINGS"] = "ignore::Warning"
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "Host: cisco3, Gateway: Internet 10.220.88.1" in std_out
    assert "Host: cisco3, Gateway: Internet 10.220.88.1" in std_out
    assert "Host: arista1, Gateway: 10.220.88.1" in std_out
    assert "Host: arista2, Gateway: 10.220.88.1" in std_out
    assert "Host: arista3, Gateway: 10.220.88.1" in std_out
    assert "Host: arista4, Gateway: 10.220.88.1" in std_out
    assert std_err == ""


def test_class2_ex4():
    base_path = "../class2/exercises/exercise4/"
    cmd_list = ["python", "exercise4.py"]

    os.environ["PYTHONWARNINGS"] = "ignore::Warning"
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert (
        "cisco3, Gateway: {'interface': 'GigabitEthernet0/0/0', 'mac': '00:62:EC:29:70"
        in std_out
    )
    assert (
        "cisco4, Gateway: {'interface': 'GigabitEthernet0/0/0', 'mac': '00:62:EC:29:70:"
        in std_out
    )
    assert (
        "arista1, Gateway: {'interface': 'Vlan1, Ethernet1', 'mac': '00:62:EC:29:70:FE"
        in std_out
    )
    assert (
        "arista2, Gateway: {'interface': 'Vlan1, Ethernet1', 'mac': '00:62:EC:29:70:FE"
        in std_out
    )
    assert (
        "arista3, Gateway: {'interface': 'Vlan1, Ethernet1', 'mac': '00:62:EC:29:70:FE"
        in std_out
    )
    assert (
        "arista4, Gateway: {'interface': 'Vlan1, Ethernet1', 'mac': '00:62:EC:29:70:FE"
        in std_out
    )
    assert std_err == ""


def test_class2_ex5a():
    base_path = "../class2/exercises/exercise5/"
    cmd_list = ["python", "exercise5a.py"]

    os.environ["PYTHONWARNINGS"] = "ignore::Warning"
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "GigabitEthernet0/0/0   10.220.88.22" in std_out
    assert "GigabitEthernet0/0/0   10.220.88.23" in std_out
    assert std_err == ""


def test_class2_ex5b():
    base_path = "../class2/exercises/exercise5/"
    cmd_list = ["python", "exercise5b.py"]

    os.environ["PYTHONWARNINGS"] = "ignore::Warning"
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "Authentication failure" in std_out
    assert "GigabitEthernet0/0/0   10.220.88.23" in std_out
    assert "Task failed hosts: {'cisco3'" in std_out
    assert "Global failed hosts: {'cisco3'}" in std_out
    assert std_err == ""


def test_class2_ex5c():
    base_path = "../class2/exercises/exercise5/"
    cmd_list = ["python", "exercise5c.py"]

    os.environ["PYTHONWARNINGS"] = "ignore::Warning"
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "Authentication failure" in std_out
    assert "GigabitEthernet0/0/0   10.220.88.23" in std_out
    assert "Task failed hosts: {'cisco3'" in std_out
    assert std_out.count("Global failed hosts: {'cisco3'}", 2)
    assert "Task failed hosts: {}" in std_out
    assert std_err == ""


def test_class2_ex5d():
    base_path = "../class2/exercises/exercise5/"
    cmd_list = ["python", "exercise5d.py"]

    os.environ["PYTHONWARNINGS"] = "ignore::Warning"
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "Authentication failure" in std_out
    assert "GigabitEthernet0/0/0   10.220.88.23" in std_out
    assert "Task failed hosts: {'cisco3'" in std_out
    assert std_out.count("Global failed hosts: {'cisco3'}", 2)
    assert "Task failed hosts: {}" in std_out
    assert "Global failed hosts: set()" in std_out
    assert std_err == ""
