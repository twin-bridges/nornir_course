from pathlib import Path
import pytest

from utilities import subprocess_runner
from utilities import gen_inventory_dict

import nornir
from nornir import InitNornir

NORNIR_LOGGING = {"enabled": False}

TEST_CASES = [
    ("../class5/collateral/generic_inventory_data/generic_data.py", "all"),
    ("../class5/collateral/connection_options/conn_options.py", "all"),
    ("../class5/collateral/additional_data/ingest_data.py", None),
    ("../class5/collateral/jinja2_render/nornir_jinja2_test.py", None),
    ("../class5/collateral/jinja2_config/nornir_jinja2_test.py", None),
    ("../class5/collateral/closing_conns/conn_close1.py", None),
    ("../class5/collateral/closing_conns/conn_close2.py", None),
    ("../class5/collateral/closing_conns/conn_close3.py", None),
    ("../class5/collateral/closing_conns/conn_close4.py", None),
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


def test_class5_ex1():
    base_path = "../class5/exercises/exercise1/"
    cmd_list = ["python", "exercise1.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("---- netmiko_send_config ** changed : True") == 6
    assert std_out.count("snmp-server chassis-id") == 2
    assert std_out.count("snmp chassis-id") == 4
    assert std_out.count("sea_datacenter-arista4") == 1
    assert "% Invalid input" not in std_out
    assert std_err == ""


def test_class5_ex2():
    base_path = "../class5/exercises/exercise2/"
    cmd_list = ["python", "exercise2.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("! Command: show running-config") == 4
    assert "Traceback" not in std_out
    assert std_err == ""


def test_class5_ex3():
    base_path = "../class5/exercises/exercise3/"
    cmd_list = ["python", "exercise3.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("rule1") == 4
    assert std_out.count("rule2") == 4
    assert std_out.count("rule3") == 4
    assert std_err == ""


def test_class5_ex4a():
    base_path = "../class5/exercises/exercise4/"
    cmd_list = ["python", "exercise4a.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("rule1") == 4
    assert std_out.count("rule2") == 4
    assert std_out.count("rule3") == 4
    assert std_err == ""


def test_class5_ex4b():
    base_path = "../class5/exercises/exercise4/"
    cmd_list = ["python", "exercise4b.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("rule1") == 4
    assert std_out.count("rule2") == 4
    assert std_out.count("rule3") == 4
    assert std_err == ""


def test_class5_ex4c():
    base_path = "../class5/exercises/exercise4/"
    cmd_list = ["python", "exercise4c.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("rule1") == 4
    assert std_out.count("rule2") == 4
    assert std_out.count("rule3") == 4
    assert std_err == ""


def test_class5_ex5b():
    base_path = "../class5/exercises/exercise5/"
    cmd_list = ["python", "exercise5b.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "router bgp 22\n  router-id 172.20.0.1\n  neighbor 172.20.0.2" in std_out
    assert (
        "Ethernet1/4\n no switchport\n ip address 172.20.0.1 255.255.255.252" in std_out
    )
    assert "router bgp 22\n  router-id 172.20.0.2\n  neighbor 172.20.0.1" in std_out
    assert (
        "Ethernet1/4\n no switchport\n ip address 172.20.0.1 255.255.255.252" in std_out
    )
    assert std_err == ""


def test_class5_ex5c():
    base_path = "../class5/exercises/exercise5/"
    cmd_list = ["python", "exercise5c.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "router bgp 22\n  router-id 172.20.0.1\n  neighbor 172.20.0.2" in std_out
    assert (
        "Ethernet1/4\n no switchport\n ip address 172.20.0.1 255.255.255.252" in std_out
    )
    assert "router bgp 22\n  router-id 172.20.0.2\n  neighbor 172.20.0.1" in std_out
    assert (
        "Ethernet1/4\n no switchport\n ip address 172.20.0.1 255.255.255.252" in std_out
    )
    assert std_out.count("success BGP is up!") == 2
    assert std_err == ""
