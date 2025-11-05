"""Configuración simple para NYC Taxi Batch Prediction"""

from pathlib import Path

# 📁 Rutas básicas
PROJECT_ROOT = Path(__file__).parent.parent
DATA_INPUT_DIR = PROJECT_ROOT / "data" / "input"
DATA_OUTPUT_DIR = PROJECT_ROOT / "data" / "output"
MODEL_PATH = PROJECT_ROOT / "lin_reg.bin"

# ⚙️ Configuración básica
NUM_TRIPS = 1000  # Número de viajes a generar
MAX_WORKERS = 2   # Número de workers para procesamiento paralelo

# 🕐 Scheduling (para Prefect)
BATCH_SCHEDULE = "0 */2 * * *"  # Cada 2 horas

# 📊 Locations comunes en NYC
COMMON_LOCATIONS = [161, 162, 163, 164, 236, 237, 238, 239, 140, 141, 142, 143]

# Crear directorios si no existen
DATA_INPUT_DIR.mkdir(parents=True, exist_ok=True)
DATA_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
