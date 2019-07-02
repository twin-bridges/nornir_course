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


def test_class3_ex1a():
    base_path = "../class3/exercises/exercise1/1a/"
    cmd_list = ["python", "exercise1a.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "{'role': 'AGG'}" in std_out
    assert (
        "dict_items([('role', 'AGG'), ('timezone', 'CET'), ('state', 'WA')])" in std_out
    )
    assert std_err == ""


def test_class3_ex1b():
    base_path = "../class3/exercises/exercise1/1b/"
    cmd_list = ["python", "exercise1b.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "{'role': 'AGG'}" in std_out
    assert (
        "dict_items([('role', 'AGG'), ('state', 'WA'), ('timezone', 'PST')])" in std_out
    )
    assert std_err == ""


def test_class3_ex2a():
    base_path = "../class3/exercises/exercise2/"
    cmd_list = ["python", "exercise2a.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("{'arista1': Host: arista1}") == 3
    assert "{'arista1': Host: arista1, 'arista2': Host: arista2}" in std_out
    assert "{'arista2': Host: arista2}" in std_out
    assert std_err == ""


def test_class3_ex3a():
    base_path = "../class3/exercises/exercise3/"
    cmd_list = ["python", "exercise3a.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "{'arista3': Host: arista3}" in std_out
    assert std_out.count("{'arista2': Host: arista2}") == 2
    assert (
        "{'arista1': Host: arista1, 'arista2': Host: arista2, 'arista3': Host: arista3}"
        in std_out
    )
    assert "{'arista1': Host: arista1}" in std_out
    assert std_err == ""


def test_class3_ex5a():
    base_path = "../class3/exercises/exercise5/"
    cmd_list = ["python", "exercise5a.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "{'arista1': {'Et1': {'status': 'connected', 'vlan': '1'}," in std_out
    assert "{'arista2': {'Et1': {'status': 'connected', 'vlan': '1'}," in std_out
    assert "{'arista3': {'Et1': {'status': 'connected', 'vlan': '1'}," in std_out
    assert "{'arista4': {'Et1': {'status': 'connected', 'vlan': '1'}," in std_out
    assert std_err == ""


def test_class3_ex6a():
    base_path = "../class3/exercises/exercise6/"
    cmd_list = ["python", "exercise6a.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "{'nxos1': {'model': 'Nexus9000 9000v Chassis'" in std_out
    assert "'nxos2': {'model': 'Nexus9000 9000v Chassis'," in std_out
    assert std_err == ""
