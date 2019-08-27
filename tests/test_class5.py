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
    assert "router bgp 22\n  router-id 1.1.1.1\n  neighbor 172.20.0.2" in std_out
    assert (
        "Ethernet1/4\n no switchport\n ip address 172.20.0.1 255.255.255.252" in std_out
    )
    assert "router bgp 22\n  router-id 2.2.2.2\n  neighbor 172.20.0.1" in std_out
    assert (
        "Ethernet1/4\n no switchport\n ip address 172.20.0.1 255.255.255.252" in std_out
    )
    assert std_err == ""


def test_class5_ex5c():
    base_path = "../class5/exercises/exercise5/"
    cmd_list = ["python", "exercise5c.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "router bgp 22\n  router-id 1.1.1.1\n  neighbor 172.20.0.2" in std_out
    assert (
        "Ethernet1/4\n no switchport\n ip address 172.20.0.1 255.255.255.252" in std_out
    )
    assert "router bgp 22\n  router-id 2.2.2.2\n  neighbor 172.20.0.1" in std_out
    assert (
        "Ethernet1/4\n no switchport\n ip address 172.20.0.1 255.255.255.252" in std_out
    )
    assert std_out.count("Success BGP is up...") == 2
    assert std_err == ""
