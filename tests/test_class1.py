from pathlib import Path
import pytest

from nornir import InitNornir
import nornir
from utilities import gen_inventory_dict
from utilities import subprocess_runner

NORNIR_LOGGING = {"enabled": False}

TEST_CASES_INVENTORY = [
    ("../class1/collateral/first_task/test_nr.py", "hosts"),
    ("../class1/collateral/core_inventory_objects/invalid.py", "all"),
    ("../class1/collateral/first_task/invalid.py", "hosts"),
    ("../class1/collateral/inventory_overview/invalid.py", "hosts"),
    ("../class1/collateral/inventory_resolution/invalid.py", "all"),
    ("../class1/collateral/run_method/invalid.py", "hosts"),
]

TEST_CASES = [
    "../class1/collateral/run_method/example.py",
    "../class1/collateral/run_method/example_w_runner.py",
]


@pytest.mark.parametrize("test_case_dir, inventory_check", TEST_CASES_INVENTORY)
def test_runner_collateral_inv(test_case_dir, inventory_check):
    path_obj = Path(test_case_dir)
    script_dir = path_obj.parents[0]
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


@pytest.mark.parametrize("test_case", TEST_CASES)
def test_runner_collateral(test_case):
    path_obj = Path(test_case)
    script = path_obj.name
    script_dir = path_obj.parents[0]

    cmd_list = ["python", script]
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=script_dir)
    assert return_code == 0
    assert std_err == ""
    assert "Traceback" not in std_out


def test_class1_ex1():
    base_path = "../class1/exercises/exercise1/"
    nornir_inventory = gen_inventory_dict(base_path)
    nr = InitNornir(inventory=nornir_inventory, logging=NORNIR_LOGGING)
    assert isinstance(nr, nornir.core.Nornir)
    assert isinstance(nr.inventory.hosts, nornir.core.inventory.Hosts)
    assert isinstance(nr.inventory.hosts["my_host"], nornir.core.inventory.Host)
    assert nr.inventory.hosts["my_host"].hostname == "localhost"


def test_class1_ex2():
    base_path = "../class1/exercises/exercise2/"
    cmd_list = ["python", "exercise2.py"]

    nornir_inventory = gen_inventory_dict(base_path)
    nr = InitNornir(inventory=nornir_inventory, logging=NORNIR_LOGGING)
    assert len(nr.inventory.hosts) == 2
    for host_name, host_obj in nr.inventory.hosts.items():
        assert host_obj.hostname is not None
        assert len(host_obj.groups) == 1
        assert host_obj.groups[0].name == "ios"
        assert host_obj.platform == "cisco_ios"
        assert host_obj.username == "pyclass"
        assert host_obj.password == "cisco123"
        assert host_obj.port == 22

    my_group = nr.inventory.groups["ios"]
    assert my_group.hostname is None
    assert my_group.platform == "cisco_ios"
    assert my_group.username == "pyclass"
    assert my_group.password == "cisco123"
    assert my_group.port == 22

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "cisco3" in std_out
    assert "cisco_ios" in std_out
    assert std_err == ""


def test_class1_ex3():
    base_path = "../class1/exercises/exercise3/"
    cmd_list = ["python", "exercise3.py"]

    nornir_inventory = gen_inventory_dict(base_path)
    nr = InitNornir(inventory=nornir_inventory, logging=NORNIR_LOGGING)
    assert len(nr.inventory.hosts) == 2
    for host_name, host_obj in nr.inventory.hosts.items():
        assert host_obj.hostname is not None
        assert len(host_obj.groups) == 1
        assert host_obj.groups[0].name == "ios"
        assert host_obj.platform == "cisco_ios"
        assert host_obj.username == "pyclass"
        assert host_obj.password == "cisco123"
        assert host_obj.port == 22

    my_group = nr.inventory.groups["ios"]
    assert my_group.hostname is None
    assert my_group.platform == "cisco_ios"
    assert my_group.port == 22

    defaults = nr.inventory.defaults
    assert defaults.username == "pyclass"
    assert defaults.password == "cisco123"

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "cisco3" in std_out
    assert "cisco_ios" in std_out
    assert std_err == ""


def test_class1_ex4():
    base_path = "../class1/exercises/exercise4/"
    cmd_list = ["python", "exercise4.py"]

    nornir_inventory = gen_inventory_dict(base_path)
    nr = InitNornir(inventory=nornir_inventory, logging=NORNIR_LOGGING)
    assert len(nr.inventory.hosts) == 2
    for host_name, host_obj in nr.inventory.hosts.items():
        assert host_obj.hostname is not None
        assert len(host_obj.groups) == 1
        assert host_obj.groups[0].name == "ios"
        assert host_obj.platform == "cisco_ios"
        assert host_obj.username == "pyclass"
        assert host_obj.password == "cisco123"
        assert host_obj.port == 22

    my_group = nr.inventory.groups["ios"]
    assert my_group.hostname is None
    assert my_group.platform == "cisco_ios"
    assert my_group.port == 22

    defaults = nr.inventory.defaults
    assert defaults.username == "pyclass"
    assert defaults.password == "cisco123"

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "cisco3.lasthop.io" in std_out
    assert "cisco4.lasthop.io" in std_out
    assert "These aren't the droids you're looking for" in std_out
    assert std_err == ""


def test_class1_ex5():
    base_path = "../class1/exercises/exercise5/"
    cmd_list = ["python", "exercise5.py"]

    nornir_inventory = gen_inventory_dict(base_path)
    nr = InitNornir(inventory=nornir_inventory, logging=NORNIR_LOGGING)

    assert len(nr.inventory.hosts) == 2
    for host_name, host_obj in nr.inventory.hosts.items():
        assert host_obj.hostname is not None
        assert len(host_obj.groups) == 1
        assert host_obj.groups[0].name == "ios"
        assert host_obj.platform == "cisco_ios"
        assert host_obj.username == "pyclass"
        assert host_obj.password == "cisco123"
        assert host_obj.port == 22
        if host_name == "cisco3":
            assert host_obj["dns1"] == "8.8.8.8"

    my_group = nr.inventory.groups["ios"]
    assert my_group.hostname is None
    assert my_group.platform == "cisco_ios"
    assert my_group.port == 22

    defaults = nr.inventory.defaults
    assert defaults.username == "pyclass"
    assert defaults.password == "cisco123"
    assert defaults.data["dns1"] == "1.1.1.1"
    assert defaults.data["dns2"] == "1.0.0.1"

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "cisco3.lasthop.io" in std_out
    assert "cisco4.lasthop.io" in std_out
    assert "8.8.8.8" in std_out
    assert "1.1.1.1" in std_out
    assert "1.0.0.1" in std_out
    assert std_err == ""
