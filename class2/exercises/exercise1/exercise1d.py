from nornir import InitNornir


def main():
    nr = InitNornir(config_file="config.yaml", core={"num_workers": 15})
    print(nr.config.core.num_workers)  # print 15 from setting in python


if __name__ == "__main__":
    main()
