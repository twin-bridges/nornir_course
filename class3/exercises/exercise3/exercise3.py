from nornir import InitNornir
from nornir.core.filter import F


def main():
    nr = InitNornir()

    print("\nExercise 3a (role AGG)")
    print("-" * 20)
    agg_devs = nr.filter(F(role__contains="AGG"))
    print(agg_devs.inventory.hosts)
    print("-" * 20)

    print("\nExercise 3b (sea or sfo group)")
    print("-" * 20)
    union = nr.filter(F(groups__contains="sea") | F(groups__contains="sfo"))
    print(union.inventory.hosts)
    print("-" * 20)

    print("\nExercise 3c (WAN-role and WIFI password 'racecar')")
    print("-" * 20)
    racecar = nr.filter(
        F(site_details__wifi_password__contains="racecar") & F(role="WAN")
    )
    print(racecar.inventory.hosts)
    print("-" * 20)

    print("\nExercise 3d (WAN-role and not WIFI password 'racecar')")
    print("-" * 20)
    not_racecar = nr.filter(
        ~F(site_details__wifi_password__contains="racecar") & F(role="WAN")
    )
    print(not_racecar.inventory.hosts)
    print("-" * 20)
    print()


if __name__ == "__main__":
    main()
