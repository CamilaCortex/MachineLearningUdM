"""Predictor simple para batch processing"""

import pickle
import pandas as pd
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.settings as settings

def load_model():
    """Carga el modelo ML"""
    print("🤖 Cargando modelo...")
    try:
        with open(settings.MODEL_PATH, 'rb') as f:
            dv, model = pickle.load(f)
        print("✅ Modelo cargado correctamente")
        return dv, model
    except FileNotFoundError:
        print(f"❌ No se encontró el modelo en: {settings.MODEL_PATH}")
        raise

def prepare_features(df):
    """Prepara las features para predicción"""
    print(f"🔧 Preparando features para {len(df)} viajes...")
    
    # Crear feature PU_DO (igual que en web service)
    features = []
    for _, row in df.iterrows():
        feature = {
            'PU_DO': f"{row['PULocationID']}_{row['DOLocationID']}",
            'trip_distance': row['trip_distance']
        }
        features.append(feature)
    
    print("✅ Features preparadas")
    return features

def make_predictions(features, dv, model):
    """Hace predicciones en lote"""
    print(f"🎯 Haciendo {len(features)} predicciones...")
    
    start_time = datetime.now()
    
    # Transformar features y predecir
    X = dv.transform(features)
    predictions = model.predict(X)
    
    end_time = datetime.now()
    processing_time = (end_time - start_time).total_seconds()
    
    print(f"✅ Predicciones completadas en {processing_time:.2f} segundos")
    print(f"⚡ Velocidad: {len(predictions)/processing_time:.0f} predicciones/segundo")
    
    return predictions

def save_predictions(df, predictions, timestamp=None):
    """Guarda las predicciones"""
    if timestamp is None:
        timestamp = datetime.now()
    
    # Crear DataFrame con resultados
    results = df.copy()
    results['predicted_duration_minutes'] = predictions
    results['prediction_timestamp'] = timestamp
    
    # Guardar archivo
    filename = f"predictions_{timestamp.strftime('%Y%m%d_%H%M%S')}.parquet"
    filepath = settings.DATA_OUTPUT_DIR / filename
    
    results.to_parquet(filepath)
    print(f"💾 Predicciones guardadas en: {filepath}")
    
    # Mostrar estadísticas
    print("📈 Estadísticas de duración:")
    print(f"   Promedio: {predictions.mean():.1f} minutos")
    print(f"   Mínimo: {predictions.min():.1f} minutos")
    print(f"   Máximo: {predictions.max():.1f} minutos")
    
    return filepath

def process_batch_file(input_file):
    """Procesa un archivo de batch completo"""
    print(f"📂 Procesando archivo: {input_file}")
    
    # 1. Cargar modelo
    dv, model = load_model()
    
    # 2. Leer datos
    df = pd.read_parquet(input_file)
    print(f"📊 Cargados {len(df)} viajes")
    
    # 3. Preparar features
    features = prepare_features(df)
    
    # 4. Hacer predicciones
    predictions = make_predictions(features, dv, model)
    
    # 5. Guardar resultados
    output_file = save_predictions(df, predictions)
    
    return output_file

# Función principal para ejecutar directamente
if __name__ == "__main__":
    # Buscar archivos de input
    input_files = list(settings.DATA_INPUT_DIR.glob("*.parquet"))
    
    if not input_files:
        print("❌ No se encontraron archivos de input")
        print("💡 Ejecuta primero: python src/data_generator.py")
    else:
        # Procesar el archivo más reciente
        latest_file = max(input_files, key=lambda x: x.stat().st_mtime)
        output_file = process_batch_file(latest_file)
        print(f"🎉 Proceso completado. Resultado: {output_file}")
