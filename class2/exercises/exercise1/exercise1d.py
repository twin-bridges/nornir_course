from nornir import InitNornir


def main():
    nr = InitNornir(config_file="config.yaml", core={"num_workers": 15})
    # Use inline configuration: set the number of workers to 15
    print(f"\nNumber of workers: {nr.config.core.num_workers}\n")


if __name__ == "__main__":
    main()
