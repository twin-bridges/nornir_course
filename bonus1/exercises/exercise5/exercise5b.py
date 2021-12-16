from pathlib import Path

from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result


def get_checkpoint_file(task):
    napalm_conn = task.host.get_connection("napalm", task.nornir.config)
    checkpoint = napalm_conn._get_checkpoint_file()
    task.host["backup"] = checkpoint
    Path("backups").mkdir(exist_ok=True)
    with open(f"backups/{task.host.name}_checkpoint", "w") as f:
        f.write(checkpoint)
    return checkpoint


def main():
    with InitNornir(config_file="config.yaml") as nr:
        nr = nr.filter(F(groups__contains="nxos"))
        agg_result = nr.run(task=get_checkpoint_file)
        print_result(agg_result)


if __name__ == "__main__":
    main()
