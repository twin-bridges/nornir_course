from glob import glob
import os
from pathlib import Path
import pytest

from utilities import subprocess_runner, subprocess_runner_stdin
from utilities import gen_inventory_dict
import nornir
from nornir import InitNornir

NORNIR_LOGGING = {"enabled": False}

TEST_CASES = [
    ("../class6/collateral/failed_tasks/failed_creds.py", None),
    ("../class6/collateral/getpass_password/getpass_password.py", None),
    ("../class6/collateral/ansible_vault/ans_vault.py", None),
    ("../class6/collateral/enable_secret/enable_secret.py", None),
    ("../class6/collateral/getpass_secret/getpass_secrets.py", None),
    ("../class6/collateral/environment_variables/env_var.py", None),
    ("../class6/collateral/logging/test_errors.py", None),
    ("../class6/collateral/logging/test_logging.py", None),
    ("../class6/collateral/logging/test_logging2.py", None),
    ("../class6/collateral/troubleshooting/test_netmiko_pdb.py", None),
    ("../class6/collateral/troubleshooting/test_napalm_slog.py", None),
    ("../class6/collateral/troubleshooting/test_netmiko_slog1.py", None),
    ("../class6/collateral/troubleshooting/test_netmiko_slog2.py", None),
]

TEST_CASES_STDIN = []

TEST_CASES_EXPECTED_FAIL = [
    ("../class6/collateral/failed_tasks/failed_netmiko.py", None),
    ("../class6/collateral/failed_tasks/failed_j2.py", None),
]


@pytest.mark.parametrize("test_case_dir, inventory_check", TEST_CASES_STDIN)
def test_runner_collateral_stdin(test_case_dir, inventory_check):

    path_obj = Path(test_case_dir)
    script = path_obj.name
    script_dir = path_obj.parents[0]

    # Inventory Checks
    if inventory_check is None:
        pass

    # Script Check
    passwd = os.environ["NORNIR_PASSWORD"]
    stdin_responses = [passwd]
    cmd_list = ["python", script]
    std_out, std_err, return_code = subprocess_runner_stdin(
        cmd_list, stdin_responses, exercise_dir=script_dir
    )
    assert return_code == 0
    assert std_err == ""


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
    assert return_code == 0
    assert std_err != ""


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


def remove_log_files(exercise_dir):
    log_files = glob(f"{exercise_dir}/*.log")
    for file in log_files:
        os.remove(file)


def test_class6_ex1a():
    base_path = "../class6/exercises/exercise1/"
    cmd_list = ["python", "exercise1a.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("syntax error, expecting <command>.") == 1
    assert std_out.count("ValueError") == 0
    assert std_err == ""


def test_class6_ex1b():
    base_path = "../class6/exercises/exercise1/"
    cmd_list = ["python", "exercise1b.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("syntax error, expecting <command>.") == 1
    assert std_out.count("ValueError") == 2
    assert std_err == ""


def test_class6_ex2a():
    base_path = "../class6/exercises/exercise2/exercise2a/"
    cmd_list = ["python", "exercise2a.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "  ip address 1.2.3.1 255.255.255.255" in std_out
    assert "  ip address 1.3.2.1 255.255.255.255" in std_out
    assert std_err == ""


def test_class6_ex2b():
    base_path = "../class6/exercises/exercise2/exercise2b_2c/"
    cmd_list = ["python", "exercise2b.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "  ip address 1.2.3.1 255.255.255.255" in std_out
    assert "Templating error occurred, but its okay" in std_out
    assert std_err == ""


def test_class6_ex2c():
    base_path = "../class6/exercises/exercise2/exercise2b_2c/"
    cmd_list = ["python", "exercise2c.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "  ip address 1.2.3.1 255.255.255.255" in std_out
    assert "Encountered Jinja2 error" in std_out
    assert std_err == ""


def test_class6_ex3a():
    base_path = "../class6/exercises/exercise3/"
    cmd_list = ["python", "exercise3a.py"]

    remove_log_files(base_path)
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert os.path.exists(f"{base_path}my_log.log")
    assert return_code == 0
    assert std_err == ""
    remove_log_files(base_path)


def test_class6_ex3b():
    base_path = "../class6/exercises/exercise3/"
    cmd_list = ["python", "exercise3b.py"]

    remove_log_files(base_path)
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert os.path.exists(f"{base_path}my_log.log")
    assert return_code == 0
    assert std_err == ""
    remove_log_files(base_path)


def test_class6_ex4a():
    base_path = "../class6/exercises/exercise4/"
    cmd_list = ["python", "exercise4a.py"]

    remove_log_files(base_path)
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert os.stat(f"{base_path}my_session.log")
    assert return_code == 0
    assert std_err == ""
    remove_log_files(base_path)


def test_class6_ex4b():
    base_path = "../class6/exercises/exercise4/"
    cmd_list = ["python", "exercise4b.py"]

    remove_log_files(base_path)
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert os.stat(f"{base_path}nxos1_session.log")
    assert os.stat(f"{base_path}nxos2_session.log")
    assert return_code == 0
    assert std_err == ""
    remove_log_files(base_path)


def test_class6_ex5a():
    base_path = "../class6/exercises/exercise5/"
    cmd_list = ["python", "exercise5a.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert std_out.count("Clock source: NTP server") >= 2
    assert std_out.count("Time source is NTP") == 2
    assert "Current time:" in std_out
    assert return_code == 0
    assert std_err == ""


def test_class6_ex5b():
    base_path = "../class6/exercises/exercise5/"
    cmd_list = ["python", "exercise5b.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert std_out.count("Clock source: NTP server") >= 2
    assert std_out.count("Time source is NTP") == 2
    assert "Current time:" in std_out
    assert return_code == 0
    assert std_err == ""


def test_class6_ex5c():
    base_path = "../class6/exercises/exercise5/"
    cmd_list = ["python", "exercise5c.py"]

    os.environ["NORNIR_VAULT_PASSWORD"] = "password"
    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert std_out.count("Clock source: NTP server") >= 2
    assert std_out.count("Time source is NTP") == 2
    assert "Current time:" in std_out
    assert return_code == 0
    assert std_err == ""
