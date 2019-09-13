from nornir import InitNornir
from nornir.core.filter import F


def direct(task):

    # Manually create NAPALM connection
    import ipdb

    ipdb.set_trace()
    napalm = task.host.get_connection("napalm", task.nornir.config)
    conn = napalm.device  # noqa


if __name__ == "__main__":
    nr = InitNornir(config_file="config.yaml")
    filt = F(groups__contains="nxos")
    nr = nr.filter(filt)
    nr.run(task=direct, num_workers=1)
