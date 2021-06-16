from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)
from kubernetes.client import models as k8s

from dags.hooks.ms_teams_hook import on_failure

with DAG(
    tags=["example"],
    dag_id="dag_example__v1",
    start_date=datetime(2021, 6, 1, 0, 0, 0, 0),
    schedule_interval="0 0 * * *",
    catchup=False,
    max_active_runs=1,
    default_args={
        "retries": 1,
        "retry_delay": timedelta(minutes=1),
        "on_failure_callback": on_failure,
    },
) as dag:
    globals()["dag_example__v1"] = dag
    task = KubernetesPodOperator(
        namespace="airflow",
        image="ubuntu:18.04",
        name="task_id",
        cmds=["bash", "-c"],
        arguments=["echo 'Hello Airflow'"],
        secrets=[],
        get_logs=True,
        image_pull_secrets=[k8s.V1LocalObjectReference("regcred")],
        is_delete_operator_pod=True,
        dag=dag,
        task_id="task_id",
    )
