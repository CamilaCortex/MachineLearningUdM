"""Test simple del flow sin servidor Prefect"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data_generator import generate_taxi_data, save_batch_data
from src.batch_predictor import process_batch_file

def test_simple_batch_flow():
    """Test completo del flow sin Prefect"""
    print("🚀 Iniciando test del batch flow simplificado")
    
    try:
        # Paso 1: Generar datos
        print("\n📊 Paso 1: Generando datos...")
        df = generate_taxi_data()
        input_file = save_batch_data(df)
        print(f"✅ Datos generados: {input_file}")
        
        # Paso 2: Procesar predicciones
        print("\n🎯 Paso 2: Procesando predicciones...")
        output_file = process_batch_file(input_file)
        print(f"✅ Predicciones completadas: {output_file}")
        
        print("\n🎉 Flow completado exitosamente!")
        return {
            'status': 'success',
            'input_file': str(input_file),
            'output_file': str(output_file)
        }
        
    except Exception as e:
        print(f"❌ Error en el flow: {e}")
        raise

if __name__ == "__main__":
    result = test_simple_batch_flow()
    print(f"\n📋 Resultado final: {result}")
