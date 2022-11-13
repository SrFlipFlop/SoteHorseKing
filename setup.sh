#Generate airflow folders
mkdir -p logs dags plugins config results

#Generate .env file
echo "AIRFLOW_UID=$(id -u)" > .env

#Generate new RSA keys
KEY=config/id_rsa
if [ ! -f "$KEY" ]; then
    ssh-keygen -b 4096 -t rsa -f "$KEY" -q -N ""
fi
