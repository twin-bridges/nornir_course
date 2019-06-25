from nornir import InitNornir


def main():
    nr = InitNornir(config_file="config.yaml")
    # Using 'export NORNIR_CORE_NUM_WORKERS=10' (number of workers should now be 10)
    print(f"\nNumber of workers: {nr.config.core.num_workers}\n")


if __name__ == "__main__":
    main()
