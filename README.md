# airflow-k8s-executor-example

## Prerequisite

- Linux/Unix OS
- Docker Desktop
- Helm
- Kubectl
- Python >= 3.8,<3.10

## Start Guide

1. git hook Setting

   > 💡 스크립트 실행에 문제가 있다면, `chmod 700 ./pre-commit.sh` 명령어를 통해 실행권한을 줍니다.

   ```
   ./pre-commit.sh
   ```

2. Create kubernetes namespace

   ```
   kubectl create namespace airflow
   ```

3. Create kubernetes secret

   ```
   # airflow-secrets
   kubectl apply -f secrets/secrets.yaml -n airflow

   # crawler-env
   kubectl apply -f secrets/crawler.yaml -n airflow
   ```

4. Add helm repo

   ```
   helm repo add airflow-stable https://airflow-helm.github.io/charts
   helm repo update
   ```

5. Install helm chart & Update helm chart

   ```
   # helm install
   helm install -f values.yaml airflow airflow-stable/airflow --namespace airflow

   # helm upgrade
   helm upgrade -f values.yaml airflow airflow-stable/airflow -n airflow
   ```

6. airflow web port-forwarding

   ```
   kubectl port-forward service/airflow-web 8080:8080 -n airflow
   kubectl port-forward service/airflow-web 8080:8080 -n airflow --address 0.0.0.0 # WSL2
   ```

## CheatSheet

### Create DAG

```
# create dag using boilerplate
python create_dag.py
```

### Create User

```
kubectl exec deployment/airflow-web -n airflow \
-- airflow users create \
   --role Admin \
   --username $AIRFLOW_ADMIN_USERNAME \
   --firstname admin \
   --lastname admin \
   --email EMAIL@example.org \
   --password $AIRFLOW_ADMIN_PASSWORD

```

### Create Connections

```
# msteams_webhook_url
kubectl exec deployment/airflow-web -n airflow \
-- airflow connections add 'msteams_webhook_url' \
   --conn-type $AIRFLOW_CONN_MSTEAMS_WEBHOOK_URL_TYPE \
   --conn-host $AIRFLOW_CONN_MSTEAMS_WEBHOOK_URL_HOST \
   --conn-schema $AIRFLOW_CONN_MSTEAMS_WEBHOOK_URL_SCHEMA
```
