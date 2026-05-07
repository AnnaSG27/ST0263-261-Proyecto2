#!/bin/bash

set -e

echo "========================================="
echo "INICIANDO PIPELINE DE DATOS"
echo "========================================="

echo ""
echo "1. Ingestando parque automotor desde MariaDB hacia S3 raw..."
python /home/ubuntu/scripts/ingestion/mariadb_to_s3.py

echo ""
echo "2. Ingestando datos climáticos desde API hacia S3 raw..."
python /home/ubuntu/scripts/ingestion/api_clima_to_s3.py

echo ""
echo "3. Procesando accidentes raw -> trusted..."
python /home/ubuntu/scripts/processing/clean_accidents.py

echo ""
echo "4. Procesando clima raw -> trusted..."
python /home/ubuntu/scripts/processing/clean_clima.py

echo ""
echo "5. Procesando parque automotor raw -> trusted..."
python /home/ubuntu/scripts/processing/clean_parque_automotor.py

echo ""
echo "========================================="
echo "PIPELINE FINALIZADO CORRECTAMENTE"
echo "========================================="
