#!/bin/bash

set -e

CRAWLER_NAME="crawler-movilidad-spark"

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
echo "3. Procesando accidentes con Apache Spark raw -> trusted_spark..."
python /home/ubuntu/ST0263-261-Proyecto2/scripts/processing_spark/clean_accidents_spark.py

echo ""
echo "4. Procesando clima con Apache Spark raw -> trusted_spark..."
python /home/ubuntu/ST0263-261-Proyecto2/scripts/processing_spark/clean_clima_spark.py

echo ""
echo "5. Procesando parque automotor con Apache Spark raw -> trusted_spark..."
python /home/ubuntu/ST0263-261-Proyecto2/scripts/processing_spark/clean_parque_automotor_spark.py

echo ""
echo "6. Ejecutando AWS Glue Crawler para actualizar el Data Catalog..."
aws glue start-crawler --name "$CRAWLER_NAME" || echo "El crawler ya podría estar en ejecución. Continuando con validación..."

echo ""
echo "Esperando a que el Glue Crawler finalice..."
while true; do
    CRAWLER_STATE=$(aws glue get-crawler --name "$CRAWLER_NAME" --query 'Crawler.State' --output text)

    echo "Estado actual del crawler: $CRAWLER_STATE"

    if [ "$CRAWLER_STATE" = "READY" ]; then
        break
    fi

    sleep 15
done

echo ""
echo "========================================="
echo "PIPELINE FINALIZADO CORRECTAMENTE"
echo "Datos disponibles en S3 trusted_spark y catalogados en AWS Glue"
echo "========================================="
