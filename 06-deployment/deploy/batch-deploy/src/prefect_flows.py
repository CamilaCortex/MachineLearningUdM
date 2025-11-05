"""Flows simples de Prefect para batch prediction"""

from datetime import datetime
from prefect import flow, task, get_run_logger

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_generator import generate_taxi_data, save_batch_data
from src.batch_predictor import process_batch_file


@task(name="generar-datos")
def generar_datos_task():
    """Genera datos de taxi para el batch"""
    logger = get_run_logger()
    logger.info("🚕 Generando datos de taxi...")
    
    # Generar datos
    df = generate_taxi_data()
    
    # Guardar datos
    filepath = save_batch_data(df)
    
    logger.info(f"✅ Datos generados y guardados en: {filepath}")
    return filepath


@task(name="procesar-predicciones")
def procesar_predicciones_task(input_file):
    """Procesa las predicciones en lote"""
    logger = get_run_logger()
    logger.info(f"🎯 Procesando predicciones para: {input_file}")
    
    # Procesar archivo
    output_file = process_batch_file(input_file)
    
    logger.info(f"✅ Predicciones completadas: {output_file}")
    return output_file


@flow(name="batch-completo")
def batch_completo_flow():
    """Flow completo: genera datos y procesa predicciones"""
    logger = get_run_logger()
    logger.info("🚀 Iniciando flow completo de batch prediction")
    
    try:
        # Paso 1: Generar datos
        input_file = generar_datos_task()
        
        # Paso 2: Procesar predicciones
        output_file = procesar_predicciones_task(input_file)
        
        logger.info("🎉 Flow completado exitosamente!")
        logger.info(f"📂 Archivo de salida: {output_file}")
        
        return {
            'status': 'success',
            'input_file': str(input_file),
            'output_file': str(output_file),
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Error en el flow: {e}")
        raise


if __name__ == "__main__":
    # Ejecutar el flow localmente
    print("🧪 Ejecutando flow de prueba...")
    result = batch_completo_flow()
    print(f"✅ Resultado: {result}")
