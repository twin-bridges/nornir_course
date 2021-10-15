from nornir import InitNornir
from nornir.core.filter import F  # noqa


def main():
    nr = InitNornir(config_file="config.yaml")
    print(nr)
    # import pdbr
    # pdbr.set_trace()


if __name__ == "__main__":
    main()
