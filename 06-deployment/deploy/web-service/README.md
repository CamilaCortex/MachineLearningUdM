# 🚕 NYC Taxi Duration Prediction - Guía de Despliegue para Estudiantes

Esta guía te ayudará a activar el entorno y desplegar el servicio de predicción de duración de viajes de taxi de NYC. **Las dependencias ya están gestionadas en el `pyproject.toml`**, solo necesitas activar el entorno con UV.

## 📋 Tabla de Contenidos

- [Inicio Rápido](#inicio-rápido)
- [Prerequisitos](#prerequisitos)
- [Activación del Entorno](#activación-del-entorno)
- [Despliegue del Servicio](#despliegue-del-servicio)
- [Pruebas del Servicio](#pruebas-del-servicio)
- [Troubleshooting](#troubleshooting)

## ⚡ Inicio Rápido

**¿Tienes prisa? Ejecuta estos 3 comandos:**

```bash
cd 04-Deployment/deploy/web-service/
uv sync
uv run python predict.py
```

¡Listo! Tu servicio estará corriendo en http://localhost:9696

## 🔧 Prerequisitos

**Solo necesitas tener instalado:**

- **Python 3.8+** (ya deberías tenerlo)
- **uv** (gestor de entornos virtuales moderno)

**Las dependencias del proyecto (Flask, scikit-learn, pandas, etc.) ya están definidas en `pyproject.toml` y se instalarán automáticamente.**

### Verificar que tienes UV instalado

```bash
# Verificar uv
uv --version
# Debe mostrar algo como: uv 0.x.x
```

### Si no tienes UV, instálalo:

```bash
# En macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Reinicia tu terminal después de la instalación
```

## 📁 Estructura del Proyecto

```
04-Deployment/deploy/web-service/
├── README.md              # Esta guía
├── pyproject.toml         # ✅ Dependencias ya configuradas
├── .python-version        # ✅ Versión de Python definida
├── predict.py             # 🎯 Servicio Flask principal
├── test.py               # 🧪 Cliente de pruebas
├── lin_reg.bin           # 🤖 Modelo entrenado
└── .venv/                # 📦 Entorno virtual (se crea automáticamente)
```

**Archivos importantes:**

- `pyproject.toml`: Contiene todas las dependencias ya configuradas
- `predict.py`: El servicio web que vas a ejecutar
- `lin_reg.bin`: Modelo de ML pre-entrenado

## 🚀 Activación del Entorno

### Paso 1: Navegar al Directorio del Proyecto

```bash
# Navegar al directorio web-service
cd 04-Deployment/deploy/web-service/
```

### Paso 2: Activar el Entorno con UV

**Las dependencias ya están configuradas. Solo necesitas activar el entorno:**

```bash
# Crear entorno virtual e instalar todas las dependencias automáticamente
uv sync

# ✅ Esto instalará: Flask, scikit-learn, pandas, numpy, gunicorn, etc.
# ✅ Todo basado en el pyproject.toml ya configurado
```

### Paso 3: Verificar la Instalación

```bash
# Verificar que el entorno se creó
ls -la .venv/  # Debe existir el directorio

# Ver las dependencias instaladas
uv tree
```

## 🎯 Formas de Usar el Entorno

### **Opción A: Con `uv run` (Más Fácil)**

```bash
# UV maneja todo automáticamente
uv run python predict.py
uv run python test.py
```

### **Opción B: Activar Manualmente**

```bash
# Activar el entorno virtual
source .venv/bin/activate

# Ahora puedes usar comandos normales
python predict.py
gunicorn --bind 0.0.0.0:9696 --workers 4 predict:app

# Para desactivar cuando termines
deactivate
```

### **¿Cuál usar?**

- **`uv run`**: Más fácil, no necesitas activar/desactivar
- **`source .venv/bin/activate`**: Más tradicional, útil si vas a ejecutar varios comandos

## 🌐 Despliegue del Servicio

### Método 1: Servidor de Desarrollo (Recomendado para Aprender)

```bash
# Ejecutar el servidor Flask
uv run python predict.py

# O si tienes el entorno activado:
python predict.py
```

**Verás algo como:**

```
INFO:__main__:🔄 Loading model and DictVectorizer...
INFO:__main__:✅ Model and DV loaded successfully
INFO:__main__:🚀 Starting Flask server on port 9696...
 * Running on http://127.0.0.1:9696
```

### Método 2: Servidor de Producción (Gunicorn)

```bash
# Con UV (recomendado)
uv run gunicorn --bind 0.0.0.0:9696 --workers 4 predict:app

# O con entorno activado
source .venv/bin/activate
gunicorn --bind 0.0.0.0:9696 --workers 4 predict:app
```

### ✅ Verificar que Todo Funciona

```bash
# 1. Verificar que el modelo existe
ls -la lin_reg.bin

# 2. Verificar que el entorno está activo
which python  # Debe apuntar a .venv/bin/python

# 3. Ver dependencias instaladas
uv tree | head -10
```

### Probar la Carga del Modelo

```bash
# Ejecutar prueba directa del modelo
uv run python predict_test.py
```

**Salida esperada:**

```
INFO:__main__:🔄 Loading model and DictVectorizer for testing...
INFO:__main__:✅ Model and DV loaded successfully
INFO:__main__:🧪 Running prediction test...
INFO:__main__:✅ Features prepared for testing: PU_DO=161_236, distance=2.5
INFO:__main__:🎯 Testing prediction made: 12.34 minutes
INFO:__main__:📊 Test result:
INFO:__main__:   Origin: 161
INFO:__main__:   Destination: 236
INFO:__main__:   Distance: 2.5 miles
INFO:__main__:   Predicted duration: 12.34 minutes
```

## 🌐 Despliegue Local

### Método 1: Ejecutar el Servidor Flask

```bash
# Ejecutar el servidor principal
uv run python predict.py
```

**Salida esperada:**

```
INFO:__main__:🔄 Loading model and DictVectorizer...
INFO:__main__:✅ Model and DV loaded successfully
INFO:__main__:🚀 Starting Flask server on port 9696...
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:9696
 * Running on http://[tu-ip]:9696
```

### Método 2: Usando Flask CLI

```bash
# Configurar variables de entorno
export FLASK_APP=predict.py
export FLASK_ENV=development

# Ejecutar servidor
flask run --host=0.0.0.0 --port=9696
```

### Método 3: Usando Gunicorn (Producción)

**Opción A: Con UV (Recomendado)**

```bash
# Gunicorn ya está incluido en las dependencias del pyproject.toml
# Ejecutar con UV
uv run gunicorn --bind 0.0.0.0:9696 --workers 4 predict:app
```

**Opción B: Con Entorno Activado**

```bash
# Activar entorno virtual
source .venv/bin/activate

# Ejecutar Gunicorn directamente
gunicorn --bind 0.0.0.0:9696 --workers 4 predict:app
```

**Probar el servicio:**

```bash
# En otra terminal, probar con curl
curl -X POST http://localhost:9696/predict \
  -H "Content-Type: application/json" \
  -d '{"PULocationID": 161, "DOLocationID": 236, "trip_distance": 2.5}'
```

## 🧪 Pruebas del Servicio

### Prueba 1: Health Check

```bash
# Verificar que el servicio está funcionando
curl http://localhost:9696/health
```

**Respuesta esperada:**

```json
{
  "dv_loaded": true,
  "model_loaded": true,
  "service": "NYC Taxi Duration Prediction",
  "status": "healthy"
}
```

### Prueba 2: Predicción Simple

```bash
# Hacer una predicción
curl -X POST http://localhost:9696/predict \
  -H "Content-Type: application/json" \
  -d '{
    "PULocationID": 161,
    "DOLocationID": 236,
    "trip_distance": 2.5
  }'
```

**Respuesta esperada:**

```json
{
  "duration": 12.34,
  "pickup_location": 161,
  "dropoff_location": 236,
  "trip_distance": 2.5
}
```

### Prueba 3: Suite Completa de Pruebas

```bash
# Ejecutar cliente de pruebas automatizado
uv run python test.py
```

## 📊 Entender el Entorno UV

### ¿Qué hace UV?

- **Gestiona dependencias** automáticamente
- **Crea entornos virtuales** sin configuración manual
- **Ejecuta comandos** en el entorno correcto

### Comandos UV útiles

```bash
uv info          # Ver información del proyecto
uv tree          # Ver dependencias instaladas
uv run <comando> # Ejecutar comando en el entorno
uv add <paquete> # Añadir nueva dependencia
uv sync          # Instalar/actualizar dependencias
```

### ¿Cuándo usar cada comando?


| Situación       | Comando                    |
| ---------------- | -------------------------- |
| Primera vez      | `uv sync`                  |
| Ejecutar app     | `uv run python predict.py` |
| Añadir paquete  | `uv add requests`          |
| Ver dependencias | `uv tree`                  |

## 🎯 Flujo Típico de Trabajo

1. **Clonar/descargar** el proyecto
2. **Navegar** al directorio: `cd 04-Deployment/deploy/web-service/`
3. **Instalar** dependencias: `uv sync`
4. **Levantar** servicio: `uv run python predict.py`
5. **Probar** en otra terminal: `curl http://localhost:9696/health`
6. **Hacer predicciones** con POST requests

## 💡 Tips para Estudiantes

### ✅ Buenas Prácticas

- Siempre usar `uv run` para ejecutar comandos
- Verificar que el modelo existe antes de levantar el servicio
- Probar con health check antes de hacer predicciones
- Leer los logs para entender qué está pasando

### ❌ Errores Comunes

- No estar en el directorio correcto
- Olvidar hacer `uv sync` primero
- Intentar usar pip en lugar de uv
- No verificar que el puerto esté libre

## 🏆 Objetivos de Aprendizaje

Al completar este ejercicio deberías entender:

1. **Gestión de entornos** con UV
2. **Despliegue de APIs** con Flask/Gunicorn
3. **Testing de servicios** con curl
4. **Troubleshooting** de problemas comunes
5. **Diferencias** entre desarrollo y producción

**Salida esperada:**

```
INFO:__main__:🚀 Starting test client for NYC Taxi API...
INFO:__main__:🧪 Starting comprehensive test suite...

INFO:__main__:1️⃣ Testing Health Check...
INFO:__main__:🏥 Checking health endpoint at http://localhost:9696/health
INFO:__main__:✅ Service healthy!

INFO:__main__:2️⃣ Testing basic prediction...
INFO:__main__:🚕 Sending test request to http://localhost:9696/predict
INFO:__main__:✅ Request successful!
INFO:__main__:📈 Predicted duration: 12.34 minutes

INFO:__main__:3️⃣ Testing edge cases...
INFO:__main__:   🔍 Case: Short trip
INFO:__main__:   ✅ Short trip: 8.45 minutes
INFO:__main__:   🔍 Case: Long trip
INFO:__main__:   ✅ Long trip: 45.67 minutes

INFO:__main__:🎉 Test suite completed!
```

## 📊 Monitoreo

### Logs del Servidor

Los logs aparecerán en la consola donde ejecutaste el servidor:

```
INFO:__main__:🚕 New prediction: 161 -> 236
INFO:__main__:✅ Features prepared: PU_DO=161_236, distance=2.5
INFO:__main__:🎯 Prediction made: 12.34 minutes
INFO:__main__:✅ Response sent: 12.34 minutes
```

### Endpoints Disponibles


| Endpoint   | Método | Descripción                  |
| ---------- | ------- | ----------------------------- |
| `/health`  | GET     | Verificar estado del servicio |
| `/predict` | POST    | Realizar predicción          |

### Formato de Request para `/predict`

```json
{
  "PULocationID": 161,      // ID de zona de recogida (1-263)
  "DOLocationID": 236,      // ID de zona de destino (1-263)
  "trip_distance": 2.5      // Distancia en millas
}
```

### Formato de Response

```json
{
  "duration": 12.34,        // Duración predicha en minutos
  "pickup_location": 161,   // Zona de recogida
  "dropoff_location": 236,  // Zona de destino
  "trip_distance": 2.5      // Distancia del viaje
}
```

## 🆘 Troubleshooting - Problemas Comunes

### Error: "No module named 'flask'"

**Síntomas:**

```
ModuleNotFoundError: No module named 'flask'
```

**Solución:**

```bash
# Instalar dependencias
uv sync

# Si persiste, recrear entorno
rm -rf .venv/
uv sync
```

### Error: "Port already in use"

**Síntomas:**

```
OSError: [Errno 48] Address already in use
```

**Solución:**

```bash
# Ver qué usa el puerto
lsof -i :9696

# Matar proceso
kill -9 <PID>
```

### Error: "lin_reg.bin not found"

**Síntomas:**

```
ERROR:__main__:❌ Error: lin_reg.bin file not found
```

**Solución:**

```bash
# Verificar que estás en el directorio correcto
pwd  # Debe terminar en /web-service/
ls lin_reg.bin  # Debe existir
```

### Error: Gunicorn no encuentra módulo

**Síntomas:**

```
ModuleNotFoundError: No module named 'predict'
```

**Solución:**

```bash
# Asegúrate de estar en el directorio correcto
cd 04-Deployment/deploy/web-service/

# Usar comando completo
uv run gunicorn --bind 0.0.0.0:9696 --workers 4 predict:app
```

### Error: Predicción fallida

**Síntomas:**

```json
{"error": "Missing required field: PULocationID"}
```

**Solución:**

- Verificar que el JSON incluye todos los campos requeridos
- Verificar el Content-Type header: `application/json`
- Verificar que los valores son del tipo correcto (int/float)

## 📞 Ayuda Adicional

Si tienes problemas:

1. **Lee los logs** completos del error
2. **Verifica prerequisitos** (Python, UV, directorio)
3. **Pregunta al profesor** con el error específico

## 🚀 Despliegue en Producción (Opcional)

### Opción 1: Docker con UV

```bash
# Crear Dockerfile optimizado para UV
cat > Dockerfile << EOF
FROM python:3.11-slim

# Instalar UV
RUN pip install uv

WORKDIR /app

# Copiar archivos de configuración
COPY pyproject.toml ./
COPY .python-version ./

# Crear entorno e instalar dependencias
RUN uv sync --no-dev

# Copiar código fuente
COPY . .

EXPOSE 9696

# Ejecutar con UV
CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:9696", "--workers", "4", "predict:app"]
EOF

# Construir imagen
docker build -t taxi-prediction .

# Ejecutar contenedor
docker run -p 9696:9696 taxi-prediction
```

### Opción 2: Heroku

```bash
# Crear Procfile
echo "web: gunicorn predict:app" > Procfile

# Crear runtime.txt
echo "python-3.9.16" > runtime.txt

# Deploy a Heroku
heroku create tu-app-name
git add .
git commit -m "Deploy taxi prediction service"
git push heroku main
```

### Opción 3: AWS EC2

```bash
# En tu instancia EC2
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt

# Usar systemd para mantener el servicio corriendo
sudo nano /etc/systemd/system/taxi-prediction.service
```

### Variables de Entorno para Producción

```bash
# Configurar variables de entorno
export FLASK_ENV=production
export MODEL_PATH=/path/to/lin_reg.bin
export PORT=9696
export WORKERS=4
```

## 📚 Recursos Adicionales

### Comandos Útiles

```bash
# Ver procesos de Python
ps aux | grep python

# Verificar entorno UV activo
uv info
echo $VIRTUAL_ENV

# Ver dependencias instaladas
uv tree

# Monitorear logs en tiempo real
tail -f /var/log/taxi-prediction.log

# Verificar uso de memoria
htop

# Hacer múltiples requests de prueba
for i in {1..10}; do curl -X POST http://localhost:9696/predict -H "Content-Type: application/json" -d '{"PULocationID": 161, "DOLocationID": 236, "trip_distance": 2.5}'; done

# Recrear entorno si hay problemas
rm -rf .venv/
uv sync
```

### Mejores Prácticas

1. **Siempre usar entornos virtuales**
2. **Validar datos de entrada**
3. **Implementar logging adecuado**
4. **Usar HTTPS en producción**
5. **Implementar rate limiting**
6. **Monitorear métricas de performance**

### Próximos Pasos

* Implementar autenticación (capas de seguridad)
* Generar board con métricas del sistema (cantidad de instancias, responses, memoria, tiempos de respuesta) - [DataDog](https://docs.datadoghq.com/es/getting_started/application/)
* Agregar tests unitarios
* Configurar CI/CD pipeline

## 🆘 Soporte

Si tienes problemas:

1. **Revisa los logs** del servidor
2. **Verifica las dependencias** están instaladas
3. **Confirma que el modelo** se carga correctamente
4. **Prueba con curl** antes de usar clientes complejos
5. **Consulta la documentación** de Flask si es necesario

**¡Felicidades! 🎉 Tu servicio de predicción de taxi está listo para usar.**

Para más información sobre MLOps y despliegue de modelos, consulta la documentación de teo y yo hemos preparado para ti.
