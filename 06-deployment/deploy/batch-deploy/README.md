# 🚀 NYC Taxi Batch Prediction - Versión Simplificada

Sistema de predicciones por lotes para duración de viajes de taxis NYC, diseñado para **aprender MLOps** paso a paso.

## 🎯 ¿Qué es Batch Processing?

Procesa grandes volúmenes de datos de manera programada:

- **Procesamiento masivo**: Miles de predicciones simultáneas
- **Ejecución programada**: Automático cada X horas/días
- **Análisis histórico**: Procesar datos acumulados

## 🚀 Cómo Usar el Sistema

### **Paso 0: Setup Inicial (Opcional)**

```bash
# Si es la primera vez, ejecutar setup automático
./scripts/setup_batch_system.sh
```

- Verifica Python y dependencias
- Crea modelo de prueba
- Configura directorios

### **Paso 1: Activar Entorno**

```bash
source .venv/bin/activate
```

### **Paso 2: Ejecutar Componentes**

#### **A. Generar Datos**

```bash
uv run python src/data_generator.py
```

- Crea 1000 viajes de taxi simulados
- Guarda en `data/input/`

#### **B. Hacer Predicciones**

```bash
uv run python src/batch_predictor.py
```

- Carga modelo ML
- Procesa datos y hace predicciones
- Guarda resultados en `data/output/`

#### **C. Pipeline Completo**

```bash
uv run python test_simple_flow.py
```

- Ejecuta generación + predicción juntos

### **Paso 3: Orquestación con Prefect**

#### **Terminal 1: Servidor**

```bash
source .venv/bin/activate
prefect server start --host 0.0.0.0 --port **4200**
```

#### **Terminal 2: Ejecutar Flow**

```bash
source .venv/bin/activate
export PREFECT_API_URL=http://0.0.0.0:4200/api
python src/prefect_flows.py
```

#### **Dashboard**

- Abrir: <http://localhost:4200>
- Ver ejecuciones y logs

## 📁 Archivos Principales

```text
src/
├── data_generator.py      # Genera datos de taxi
├── batch_predictor.py     # Hace predicciones ML
└── prefect_flows.py       # Flow con Prefect

data/
├── input/                 # Datos de entrada
└── output/                # Resultados

test_simple_flow.py        # Pipeline sin Prefect
```

## 🎓 ¿Qué Aprenderás?

- **Batch Processing**: Procesamiento por lotes vs tiempo real
- **Pipeline ML**: Datos → Modelo → Predicciones → Resultados
- **Orquestación**: Automatizar flujos con Prefect
- **Monitoreo**: Dashboard y logs de ejecución

## 🔧 Troubleshooting

### **Error: "Model file not found"**

```bash
cp ../web-service/lin_reg.bin model/model.pkl
```

### **Error: "Prefect server not running"**

```bash
prefect server start --host 0.0.0.0 --port 4200
```

### **Error: "Module not found"**

```bash
source .venv/bin/activate
```

---

**🎉 ¡Listo para aprender MLOps con batch processing!**
