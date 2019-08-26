from nornir import InitNornir
from nornir.plugins.tasks import text


def render_configurations(task):
    """
    The following line would fail due to "domain_name" being udnefined
    task.run(task=text.template_file, template="eos.j2", path="templates", **task.host)
    """
    task.run(
        task=text.template_file,
        template="eos.j2",
        path="templates",
        **task.host,
        domain_name="TEST"
    )


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="arista1")
    agg_result = nr.run(task=render_configurations)
    print(agg_result["arista1"].result)
    print("Complete!")


if __name__ == "__main__":
    main()
