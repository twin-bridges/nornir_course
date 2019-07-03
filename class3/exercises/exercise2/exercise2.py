from nornir import InitNornir
from nornir.core.filter import F


def main():
    nr = InitNornir()

    arista1 = nr.filter(name="arista1")
    print(arista1.inventory.hosts)

    wan_devs = nr.filter(role="WAN")
    print(wan_devs.inventory.hosts)
    wan_devs = wan_devs.filter(port=22)
    print(wan_devs.inventory.hosts)
    # Alternatively:
    # wan_devs = nr.filter(role="WAN").filter(port=22)

    sfo_f_obj = nr.filter(F(groups__contains="sfo"))
    print(sfo_f_obj.inventory.hosts)
    sfo_filt = nr.filter(groups=["eos", "sfo"])
    print(sfo_filt.inventory.hosts)


if __name__ == "__main__":
    main()
