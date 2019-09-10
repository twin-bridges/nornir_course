from nornir import InitNornir
from nornir.core.filter import F
from pprint import pprint


def direct(task):

    # Manually create NAPALM connection
    import ipdb

    ipdb.set_trace()
    napalm = task.host.get_connection("napalm", task.nornir.config)
    eapi_conn = napalm.device

    show_version = eapi_conn.enable("show version")
    pprint(show_version)


if __name__ == "__main__":
    nr = InitNornir(config_file="config.yaml")
    filt = F(groups__contains="eos")
    nr = nr.filter(filt)
    nr.run(task=direct, num_workers=1)
