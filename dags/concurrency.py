from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)
from kubernetes.client import models as k8s

from dags.hooks.ms_teams_hook import on_failure

with DAG(
    tags=["concurrency"],
    dag_id="concurrency_on__v1",
    start_date=datetime(2021, 6, 1, 0, 0, 0, 0),
    schedule_interval=None,
    catchup=False,
    max_active_runs=1,
    concurrency=3,
    default_args={
        "retries": 5,
        "retry_delay": timedelta(minutes=10),
        "on_failure_callback": on_failure,
    },
) as dag:
    globals()["concurrency_on__v1"] = dag
    tasks = []
    for i in range(10):
        tasks.append(
            KubernetesPodOperator(
                namespace="airflow",
                image="ubuntu:18.04",
                name=f"task_{i}",
                cmds=["bash", "-c"],
                arguments=["echo 'Hello Airflow'"],
                secrets=[],
                get_logs=True,
                image_pull_secrets=[k8s.V1LocalObjectReference("regcred")],
                is_delete_operator_pod=True,
                dag=dag,
                task_id=f"task_{i}",
            )
        )


with DAG(
    tags=["concurrency"],
    dag_id="concurrency_off__v1",
    start_date=datetime(2021, 6, 1, 0, 0, 0, 0),
    schedule_interval=None,
    catchup=False,
    max_active_runs=1,
    default_args={
        "retries": 5,
        "retry_delay": timedelta(minutes=10),
        "on_failure_callback": on_failure,
    },
) as dag:
    globals()["concurrency_off__v1"] = dag
    tasks = []
    for i in range(10):
        tasks.append(
            KubernetesPodOperator(
                namespace="airflow",
                image="ubuntu:18.04",
                name=f"task_{i}",
                cmds=["bash", "-c"],
                arguments=["echo 'Hello Airflow'"],
                secrets=[],
                get_logs=True,
                image_pull_secrets=[k8s.V1LocalObjectReference("regcred")],
                is_delete_operator_pod=True,
                dag=dag,
                task_id=f"task_{i}",
            )
        )
