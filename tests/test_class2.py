import os
import pytest
from pathlib import Path

import nornir
from nornir import InitNornir

from utilities import gen_inventory_dict
from utilities import subprocess_runner


NORNIR_LOGGING = {"enabled": False}

TEST_CASES = [
    ("../class2/collateral/configuration_options/base_example_cfg_file.py", None),
    ("../class2/collateral/configuration_options/base_example_cfg_in_code.py", None),
    ("../class2/collateral/results/results_example.py", None),
    ("../class2/collateral/nornir_netmiko_plugins/netmiko_show_ip.py", "hosts-groups"),
    (
        "../class2/collateral/nornir_netmiko_plugins/netmiko_show_ip_2.py",
        "hosts-groups",
    ),
    ("../class2/collateral/netmiko_enable/netmiko_enable.py", "hosts-groups"),
    ("../class2/collateral/netmiko_save_config/netmiko_wrmem.py", "hosts-groups"),
    (
        "../class2/collateral/nornir_napalm_plugins/napalm_example/napalm_arp.py",
        "hosts-groups",
    ),
    (
        "../class2/collateral/nornir_napalm_plugins/napalm_example/napalm_facts.py",
        "hosts-groups",
    ),
    (
        "../class2/collateral/nornir_napalm_plugins/napalm_example/napalm_lldp.py",
        "hosts-groups",
    ),
    (
        "../class2/collateral/nornir_napalm_plugins/enable/napalm_config.py",
        "hosts-groups",
    ),
    (
        "../class2/collateral/nornir_napalm_plugins/napalm_bgp/napalm_bgp.py",
        "hosts-groups",
    ),
]

TEST_CASES_EXPECTED_FAIL = [
    ("../class2/collateral/configuration_options/base_example.py", None),
    ("../class2/collateral/failed_tasks/raise_on_error.py", None),
]


@pytest.mark.parametrize("test_case_dir, inventory_check", TEST_CASES_EXPECTED_FAIL)
def test_runner_collateral_fail(test_case_dir, inventory_check):
    path_obj = Path(test_case_dir)
    script = path_obj.name
    script_dir = path_obj.parents[0]

    # Inventory Checks
    if inventory_check is None:
        pass

    # Script Check
    cmd_list = ["python", script]
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=script_dir)
    assert return_code != 0
    assert std_err != ""


@pytest.mark.parametrize("test_case_dir, inventory_check", TEST_CASES)
def test_runner_collateral(test_case_dir, inventory_check):
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
    assert "Traceback" not in std_out


def test_class2_ex1a():
    base_path = "../class2/exercises/exercise1/"
    cmd_list = ["python", "exercise1a.py"]

    nornir_inventory = gen_inventory_dict(base_path)
    nr = InitNornir(inventory=nornir_inventory, logging=NORNIR_LOGGING)  # noqa
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

    options = nr.config.runner.options
    assert options["num_workers"] == 5
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
        config_file=f"{base_path}/config1c.yaml",
    )
    assert nr.config.runner.options == {}
    os.environ["NORNIR_RUNNER_OPTIONS"] = '{"num_workers": 100}'
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "100" in std_out
    assert std_err == ""
    del os.environ["NORNIR_RUNNER_OPTIONS"]


def test_class2_ex1d():
    base_path = "../class2/exercises/exercise1/"
    cmd_list = ["python", "exercise1d.py"]

    nornir_inventory = gen_inventory_dict(base_path)
    nr = InitNornir(
        inventory=nornir_inventory,
        logging=NORNIR_LOGGING,
        config_file=f"{base_path}/config.yaml",
    )
    options = nr.config.runner.options
    assert options["num_workers"] == 5
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "15" in std_out
    assert std_err == ""


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
    assert "cisco3, Gateway: {'interface': 'GigabitEthernet0/0/0'" in std_out
    assert "cisco4, Gateway: {'interface': 'GigabitEthernet0/0/0'" in std_out
    assert "arista1, Gateway: {'interface': 'Vlan1, Ethernet1'" in std_out
    assert "arista2, Gateway: {'interface': 'Vlan1, Ethernet1'" in std_out
    assert "arista3, Gateway: {'interface': 'Vlan1, Ethernet1'" in std_out
    assert "arista4, Gateway: {'interface': 'Vlan1, Ethernet1'" in std_out
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
    assert "Authentication failed" in std_out
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
    assert "Authentication failed" in std_out
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
    assert "Authentication failed" in std_out
    assert "GigabitEthernet0/0/0   10.220.88.23" in std_out
    assert "Task failed hosts: {'cisco3'" in std_out
    assert std_out.count("Global failed hosts: {'cisco3'}", 2)
    assert "Task failed hosts: {}" in std_out
    assert "Global failed hosts: set()" in std_out
    assert std_err == ""
