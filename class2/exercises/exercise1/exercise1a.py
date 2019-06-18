from nornir import InitNornir


def main():
    nr = InitNornir()
    print(nr.config.core.num_workers)  # print default of 20


if __name__ == "__main__":
    main()
