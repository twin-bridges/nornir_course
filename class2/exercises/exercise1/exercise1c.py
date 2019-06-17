from nornir import InitNornir


def main():
    nr = InitNornir(config_file="config.yaml")
    print(nr.config.core.num_workers)  # print 10 from setting in env var


if __name__ == "__main__":
    main()
