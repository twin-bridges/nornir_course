import os
from pathlib import Path
import pytest

from utilities import subprocess_runner
from utilities import gen_inventory_dict

import nornir
from nornir import InitNornir

NORNIR_LOGGING = {"enabled": False}

TEST_CASES = [
    ("../class3/collateral/netmiko_textfsm/test_tfsm.py", None),
    ("../class3/collateral/inventory_preference/inv_pref.py", "all"),
    ("../class3/collateral/inventory_filtering/filtering.py", "all"),
    ("../class3/collateral/resolution_and_preference_extras/filtering.py", None),
    ("../class3/collateral/napalm_getters/getters.py", None),
    ("../class3/collateral/nornir_pdb/nr_test.py", None),
]


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


def test_class3_ex1a():
    base_path = "../class3/exercises/exercise1/exercise1a/"
    cmd_list = ["python", "exercise1a.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "{'role': 'AGG'}" in std_out
    assert "{'role': 'AGG', 'timezone': 'CET', 'state': 'WA'}" in std_out
    assert std_err == ""


def test_class3_ex1b():
    base_path = "../class3/exercises/exercise1/exercise1b/"
    cmd_list = ["python", "exercise1b.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("CET") == 2
    assert std_out.count("PST") == 1
    assert std_err == ""


def test_class3_ex2():
    base_path = "../class3/exercises/exercise2/"
    cmd_list = ["python", "exercise2.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("{'arista1': Host: arista1}") == 2
    assert "{'arista1': Host: arista1, 'arista2': Host: arista2}" in std_out
    assert "{'arista2': Host: arista2}" in std_out
    assert std_err == ""


def test_class3_ex3():
    base_path = "../class3/exercises/exercise3/"
    cmd_list = ["python", "exercise3.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "{'arista3': Host: arista3}" in std_out
    assert (
        "{'arista1': Host: arista1, 'arista2': Host: arista2, 'arista3': Host: arista3}"
        in std_out
    )
    assert "{'arista2': Host: arista2}" in std_out
    assert "{'arista1': Host: arista1}" in std_out
    assert std_err == ""


def test_class3_ex4():
    base_path = "../class3/exercises/exercise4/"
    cmd_list = ["python", "exercise4.py"]

    os.environ["PYTHONWARNINGS"] = "ignore::Warning"
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "{'arista1': {'Et1': {'status': 'connected', 'vlan': '1'}," in std_out
    assert "'arista2': {'Et1': {'status': 'connected', 'vlan': '1'}," in std_out
    assert "'arista3': {'Et1': {'status': 'connected', 'vlan': '1'}," in std_out
    assert "'arista4': {'Et1': {'status': 'connected', 'vlan': '1'}," in std_out
    assert std_err == ""


def test_class3_ex5():
    base_path = "../class3/exercises/exercise5/"
    cmd_list = ["python", "exercise5.py"]

    os.environ["PYTHONWARNINGS"] = "ignore::Warning"
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "{'arista1': {'Et1': {'status': 'connected', 'vlan': '1'}," in std_out
    assert "'arista2': {'Et1': {'status': 'connected', 'vlan': '1'}," in std_out
    assert "'arista3': {'Et1': {'status': 'connected', 'vlan': '1'}," in std_out
    assert "'arista4': {'Et1': {'status': 'connected', 'vlan': '1'}," in std_out
    assert std_err == ""


def test_class3_ex6a():
    base_path = "../class3/exercises/exercise6/"
    cmd_list = ["python", "exercise6a.py"]

    os.environ["PYTHONWARNINGS"] = "ignore::Warning"
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("nxos1") == 5
    assert std_out.count("nxos2") == 5
    assert std_out.count("napalm_get") == 5
    assert std_out.count("candidate") == 2
    assert std_out.count("running") == 2
    assert std_out.count("startup") == 2
    assert std_err == ""


def test_class3_ex6b():
    base_path = "../class3/exercises/exercise6/"
    cmd_list = ["python", "exercise6b.py"]

    os.environ["PYTHONWARNINGS"] = "ignore::Warning"
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("nxos1") == 3
    assert std_out.count("nxos2") == 3
    assert std_out.count("napalm_get") == 5
    assert std_out.count("candidate") == 2
    assert std_out.count("running") == 2
    assert std_out.count("startup") == 2
    assert std_err == ""


def test_class3_ex6c():
    base_path = "../class3/exercises/exercise6/"
    cmd_list = ["python", "exercise6c.py"]

    os.environ["PYTHONWARNINGS"] = "ignore::Warning"
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("nxos1") == 5
    assert std_out.count("nxos2") == 5
    assert std_out.count("facts") == 2
    assert std_out.count("napalm_get") == 5
    assert std_out.count("candidate") == 2
    assert std_out.count("running") == 2
    assert std_out.count("startup") == 2
    assert std_err == ""


def test_class3_ex6d():
    base_path = "../class3/exercises/exercise6/"
    cmd_list = ["python", "exercise6d.py"]

    os.environ["PYTHONWARNINGS"] = "ignore::Warning"
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "{'nxos1': {'model': 'Nexus9000 9000v Chassis'" in std_out
    assert "'nxos2': {'model': 'Nexus9000 9000v Chassis'," in std_out
    assert std_err == ""
