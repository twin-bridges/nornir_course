from nornir import InitNornir
from nornir.core.filter import F  # noqa


def main():
    nr = InitNornir(config_file="config.yaml")
    print(nr)
    import ipdb

    ipdb.set_trace()


if __name__ == "__main__":
    main()
