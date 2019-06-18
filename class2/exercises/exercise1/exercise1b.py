from nornir import InitNornir


def main():
    nr = InitNornir(config_file="config.yaml")
    print(nr.config.core.num_workers)  # print 5 from setting in config file


if __name__ == "__main__":
    main()
