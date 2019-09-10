import lxml

from nornir import InitNornir
from nornir.core.filter import F


def direct(task):

    # Manually create NAPALM connection
    napalm = task.host.get_connection("napalm", task.nornir.config)
    jnpr_conn = napalm.device
    xml_output = jnpr_conn.rpc.get_software_information()
    print(xml_output)
    print(lxml.etree.tostring(xml_output, pretty_print=True).decode())


if __name__ == "__main__":
    nr = InitNornir(config_file="config.yaml")
    filt = F(groups__contains="junos")
    nr = nr.filter(filt)
    nr.run(task=direct, num_workers=1)
