import subprocess


def subprocess_runner(cmd_list, exercise_dir):
    with subprocess.Popen(
        cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=exercise_dir
    ) as proc:
        std_out, std_err = proc.communicate()
    return (std_out.decode(), std_err.decode(), proc.returncode)


def test_class_bonus2_ex1():
    base_path = "../bonus2/exercises/"
    cmd_list = ["python", "bgp_config_tool_final.py"]

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert std_out.count("completed successfully!") == 6
    assert std_out.count("ERROR") == 0
    assert std_err == ""
