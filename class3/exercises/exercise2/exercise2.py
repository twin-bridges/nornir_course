from nornir import InitNornir
from nornir.core.filter import F


def main():
    nr = InitNornir()

    # Exercise 2a
    print("\nExercise 2a")
    print("-" * 20)
    arista1 = nr.filter(name="arista1")
    print(arista1.inventory.hosts)
    print("-" * 20)

    print("\nExercise 2b")
    print("-" * 20)
    wan_devs = nr.filter(role="WAN")
    print(wan_devs.inventory.hosts)
    wan_devs = wan_devs.filter(port=22)
    print(wan_devs.inventory.hosts)
    print("-" * 20)
    # Alternatively:
    # wan_devs = nr.filter(role="WAN").filter(port=22)

    print("\nExercise 2c")
    print("-" * 20)
    sfo_f_obj = nr.filter(F(groups__contains="sfo"))
    print(sfo_f_obj.inventory.hosts)
    print("-" * 20)
    print()


if __name__ == "__main__":
    main()
