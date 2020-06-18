import os
from pathlib import Path
import pytest

from utilities import subprocess_runner
from utilities import gen_inventory_dict

import nornir
from nornir import InitNornir


NORNIR_LOGGING = {"enabled": False}

TEST_CASES = [
    ("../bonus2/collateral/netbox/nbox.py", None),
    ("../bonus2/collateral/processors/processor_timestamper.py", None),
    ("../bonus2/collateral/processors/processor_basic.py", None),
    ("../bonus2/collateral/genie/show_genie.py", None),
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


def test_class_bonus2_ex1():
    base_path = "../bonus2/exercises/"
    cmd_list = ["python", "bgp_config_tool_final.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("completed successfully!") == 6
    assert std_out.count("ERROR") == 0
    assert std_err == ""
