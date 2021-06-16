import questionary
import typer
from jinja2 import Environment, FileSystemLoader

app = typer.Typer()


@app.command()
def create_dag() -> None:
    tags = ["example"]

    kwargs = questionary.form(
        file_path=questionary.path("Path to DAG including file name"),
        dag_id=questionary.text(
            "DAG name",
            default="dag_boilerplate__v1",
            validate=lambda dag_id: True
            if dag_id.split("_")[-1].startswith("v")
            and dag_id.split("_")[-2] == ""
            and " " not in dag_id
            else "Check Naming Convention.",
        ),
        schedule_interval=questionary.text(
            "schedule_interval using crontab expression", default="0 0 * * *"
        ),
        tags=questionary.checkbox("Select tags", choices=tags, default=None),
        retries=questionary.text("retries", default="5"),
        retry_delay=questionary.text("retry delay minutes", default="10"),
        catchup=questionary.confirm("catchup", default=False),
        max_active_runs=questionary.text("max_active_runs", default="1"),
        has_dependency=questionary.confirm("DAG has cross dependency ?", default=False),
    ).ask()
    external_dag_id = (
        questionary.text("external_dag_id").skip_if(not kwargs["has_dependency"]).ask()
    )
    kwargs["external_dag_id"] = external_dag_id

    file_loader = FileSystemLoader("templates")
    env = Environment(loader=file_loader)
    if kwargs["has_dependency"]:
        template = env.get_template("dag_with_dependency.tpl")
    else:
        template = env.get_template("dag.tpl")
    output = template.render(**kwargs)
    with open(kwargs["file_path"], "w") as f:
        f.write(output)


if __name__ == "__main__":
    app()
