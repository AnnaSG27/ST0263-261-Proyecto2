#!/bin/bash

set -e

BUCKET_NAME="proyecto2-jose-anna-datalake"
EMR_CLUSTER_ID="${EMR_CLUSTER_ID:-}"

if [ -z "$EMR_CLUSTER_ID" ]; then
    echo "ERROR: Debes definir la variable EMR_CLUSTER_ID antes de ejecutar el pipeline."
    echo "Ejemplo: export EMR_CLUSTER_ID=j-XXXXXXXXXXXXX"
    exit 1
fi

wait_for_step() {
    local STEP_ID=$1
    local STEP_NAME=$2

    echo "Esperando finalización del step: $STEP_NAME ($STEP_ID)"

    while true; do
        STEP_STATE=$(aws emr describe-step \
            --cluster-id "$EMR_CLUSTER_ID" \
            --step-id "$STEP_ID" \
            --query 'Step.Status.State' \
            --output text)

        echo "Estado actual de $STEP_NAME: $STEP_STATE"

        if [ "$STEP_STATE" = "COMPLETED" ]; then
            echo "Step completado correctamente: $STEP_NAME"
            break
        fi

        if [ "$STEP_STATE" = "FAILED" ] || [ "$STEP_STATE" = "CANCELLED" ] || [ "$STEP_STATE" = "INTERRUPTED" ]; then
            echo "ERROR: El step $STEP_NAME terminó con estado $STEP_STATE"
            exit 1
        fi

        sleep 20
    done
}

add_spark_step() {
    local STEP_NAME=$1
    local SCRIPT_PATH=$2

    STEP_ID=$(aws emr add-steps \
        --cluster-id "$EMR_CLUSTER_ID" \
        --steps Type=Spark,Name="$STEP_NAME",ActionOnFailure=CONTINUE,Args=["$SCRIPT_PATH"] \
        --query 'StepIds[0]' \
        --output text)

    echo "Step enviado: $STEP_NAME ($STEP_ID)"
    wait_for_step "$STEP_ID" "$STEP_NAME"
}

echo "========================================="
echo "INICIANDO PIPELINE DE DATOS"
echo "========================================="

echo ""
echo "1. Ingestando parque automotor desde MariaDB hacia S3 raw..."
python /home/ubuntu/ST0263-261-Proyecto2/scripts/ingestion/mariadb_to_s3.py

echo ""
echo "2. Ingestando datos climáticos desde API Open-Meteo hacia S3 raw..."
python /home/ubuntu/ST0263-261-Proyecto2/scripts/ingestion/api_clima_to_s3.py

echo ""
echo "3. Ejecutando ETL de accidentes en EMR con Spark..."
add_spark_step \
    "ETL Accidentes Spark" \
    "s3://${BUCKET_NAME}/scripts/clean_accidents_spark.py"

echo ""
echo "4. Ejecutando ETL de clima en EMR con Spark..."
add_spark_step \
    "ETL Clima Spark" \
    "s3://${BUCKET_NAME}/scripts/clean_clima_spark.py"

echo ""
echo "5. Ejecutando ETL de parque automotor en EMR con Spark..."
add_spark_step \
    "ETL Parque Automotor Spark" \
    "s3://${BUCKET_NAME}/scripts/clean_parque_automotor_spark.py"

echo ""
echo "6. Ejecutando consultas analíticas SparkSQL en EMR..."
add_spark_step \
    "SparkSQL Analytics" \
    "s3://${BUCKET_NAME}/scripts/sparksql_queries.py"

echo ""
echo "========================================="
echo "PIPELINE FINALIZADO CORRECTAMENTE"
echo "Datos procesados disponibles en S3 trusted_spark"
echo "Resultados analíticos disponibles en S3 refined/sparksql"
echo "El dashboard Streamlit consume los resultados generados por SparkSQL"
echo "========================================="
