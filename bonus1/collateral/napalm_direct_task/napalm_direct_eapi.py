import pdbr  # noqa
from nornir import InitNornir
from nornir.core.filter import F
from pprint import pprint


def direct(task):

    # Manually create NAPALM connection
    # pdbr.set_trace()
    napalm = task.host.get_connection("napalm", task.nornir.config)
    eapi_conn = napalm.device

    show_version = eapi_conn.enable("show version")
    pprint(show_version)


if __name__ == "__main__":
    with InitNornir(config_file="config.yaml") as nr:
        filt = F(groups__contains="eos")
        nr = nr.filter(filt)
        nr.run(task=direct)
