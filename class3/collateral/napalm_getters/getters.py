from nornir import InitNornir


def main():
    nr = InitNornir(config_file="config.yaml")
    print(nr)
    import ipdb

    ipdb.set_trace()


if __name__ == "__main__":
    main()
