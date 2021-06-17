from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)
from kubernetes.client import models as k8s

from dags.hooks.ms_teams_hook import on_failure

with DAG(
    tags=["depends_on_past"],
    dag_id="depends_on_past_on__v1",
    start_date=datetime(2021, 6, 1, 0, 0, 0, 0),
    schedule_interval="* * * * *",
    catchup=False,
    max_active_runs=1,
    default_args={
        "retries": 1,
        "retry_delay": timedelta(minutes=1),
        "on_failure_callback": on_failure,
        "depends_on_past": True,
    },
) as dag:
    globals()["depends_on_past_on__v1"] = dag
    success = KubernetesPodOperator(
        namespace="airflow",
        image="ubuntu:18.04",
        name="success",
        cmds=["bash", "-c"],
        arguments=["echo 'Hello Airflow'"],
        secrets=[],
        get_logs=True,
        image_pull_secrets=[k8s.V1LocalObjectReference("regcred")],
        is_delete_operator_pod=True,
        dag=dag,
        task_id="success",
    )
    fail = KubernetesPodOperator(
        namespace="airflow",
        image="ubuntu:18.04",
        name="fail",
        cmds=["bash", "-c"],
        arguments=["Error"],
        secrets=[],
        get_logs=True,
        image_pull_secrets=[k8s.V1LocalObjectReference("regcred")],
        is_delete_operator_pod=True,
        dag=dag,
        task_id="fail",
    )
    success >> fail

with DAG(
    tags=["depends_on_past"],
    dag_id="depends_on_past_off__v1",
    start_date=datetime(2021, 6, 1, 0, 0, 0, 0),
    schedule_interval="* * * * *",
    catchup=False,
    max_active_runs=1,
    default_args={
        "retries": 1,
        "retry_delay": timedelta(minutes=1),
        "on_failure_callback": on_failure,
    },
) as dag:
    globals()["depends_on_past_off__v1"] = dag
    success = KubernetesPodOperator(
        namespace="airflow",
        image="ubuntu:18.04",
        name="success",
        cmds=["bash", "-c"],
        arguments=["echo 'Hello Airflow'"],
        secrets=[],
        get_logs=True,
        image_pull_secrets=[k8s.V1LocalObjectReference("regcred")],
        is_delete_operator_pod=True,
        dag=dag,
        task_id="success",
    )
    fail = KubernetesPodOperator(
        namespace="airflow",
        image="ubuntu:18.04",
        name="fail",
        cmds=["bash", "-c"],
        arguments=["Error"],
        secrets=[],
        get_logs=True,
        image_pull_secrets=[k8s.V1LocalObjectReference("regcred")],
        is_delete_operator_pod=True,
        dag=dag,
        task_id="fail",
    )
    success >> fail
