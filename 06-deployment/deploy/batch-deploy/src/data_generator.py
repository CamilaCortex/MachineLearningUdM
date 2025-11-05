"""Generador simple de datos de taxi para batch prediction"""

import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.settings as settings

def generate_taxi_data(num_trips=None):
    """
    Genera datos simples de taxi para batch processing
    
    Args:
        num_trips: Número de viajes a generar
        
    Returns:
        DataFrame con datos de viajes
    """
    if num_trips is None:
        num_trips = settings.NUM_TRIPS
        
    print(f"🚕 Generando {num_trips} viajes de taxi...")
    
    # Usar seed para resultados reproducibles
    np.random.seed(42)
    
    # Generar datos básicos
    data = {
        'PULocationID': np.random.choice(settings.COMMON_LOCATIONS, num_trips),
        'DOLocationID': np.random.choice(settings.COMMON_LOCATIONS, num_trips),
        'trip_distance': np.random.uniform(0.5, 10.0, num_trips)  # 0.5 a 10 km
    }
    
    df = pd.DataFrame(data)
    
    # Asegurar que pickup != dropoff
    same_location = df['PULocationID'] == df['DOLocationID']
    if same_location.any():
        # Cambiar dropoff a una location diferente
        df.loc[same_location, 'DOLocationID'] = np.random.choice(
            [loc for loc in settings.COMMON_LOCATIONS], 
            same_location.sum()
        )
    
    print(f"✅ Generados {len(df)} viajes")
    print(f"📊 Distancia promedio: {df['trip_distance'].mean():.2f} km")
    
    return df

def save_batch_data(df, timestamp=None):
    """Guarda los datos en formato parquet"""
    if timestamp is None:
        timestamp = datetime.now()
    
    filename = f"taxi_batch_{timestamp.strftime('%Y%m%d_%H%M%S')}.parquet"
    filepath = settings.DATA_INPUT_DIR / filename
    
    df.to_parquet(filepath)
    print(f"📁 Datos guardados en: {filepath}")
    return filepath

# Función principal para ejecutar directamente
if __name__ == "__main__":
    # Generar datos
    df = generate_taxi_data()
    
    # Guardar datos
    filepath = save_batch_data(df)
    
    print(f"🎉 Proceso completado. Archivo: {filepath}")
