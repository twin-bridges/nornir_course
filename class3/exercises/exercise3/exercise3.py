from nornir import InitNornir
from nornir.core.filter import F


def main():
    nr = InitNornir()

    agg_devs = nr.filter(F(role__contains="AGG"))
    print(agg_devs.inventory.hosts)

    racecar = nr.filter(F(site_details__wifi_password__contains="racecar"))
    print(racecar.inventory.hosts)

    union = nr.filter(F(groups__contains="sea") | F(groups__contains="sfo"))
    print(union.inventory.hosts)

    intersection = nr.filter(
        F(role__contains="WAN") & F(site_details__wifi_password__contains="racecar")
    )
    print(intersection.inventory.hosts)

    inverse = nr.filter(
        F(role__contains="WAN") & ~F(site_details__wifi_password__contains="racecar")
    )
    print(inverse.inventory.hosts)


if __name__ == "__main__":
    main()
