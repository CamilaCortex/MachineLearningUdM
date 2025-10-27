# 1.3 Machine Learning Supervisado

> **Objetivo**: Dominar los conceptos fundamentales del aprendizaje supervisado y sus tipos principales.

## 📖 Introducción

**Machine Learning Supervisado** es el tipo más común de ML en la industria. Se llama "supervisado" porque aprendemos de datos que ya tienen las respuestas correctas (etiquetas). Es como aprender con un profesor que te muestra ejemplos y te dice cuál es la respuesta correcta.

## 🎯 Concepto Central

En ML Supervisado tenemos:

```python
# Datos de entrenamiento con respuestas conocidas
X = [[2019, 50000, 1],    # Features: año, km, es_toyota
     [2015, 120000, 0],
     [2020, 30000, 1]]

y = [18000, 12000, 22000]  # Target: precios conocidos

# El modelo aprende la relación
modelo.fit(X, y)

# Luego predice para nuevos datos
X_nuevo = [[2018, 60000, 1]]
precio = modelo.predict(X_nuevo)  # Predice el precio
```

### Componentes Fundamentales

#### 1. Matriz de Características (X)

Es una tabla donde:
- **Filas** = Observaciones/ejemplos
- **Columnas** = Características/features

```python
import pandas as pd

# Ejemplo: Dataset de casas
X = pd.DataFrame({
    'metros_cuadrados': [120, 85, 200, 150],
    'habitaciones': [3, 2, 4, 3],
    'antiguedad': [5, 15, 2, 10],
    'distancia_centro': [2.5, 8.0, 1.2, 5.0]
})

print(X.shape)  # (4, 4) - 4 casas, 4 características
```

#### 2. Vector Objetivo (y)

Es lo que queremos predecir:

```python
# Precios de las casas (en miles)
y = pd.Series([250, 180, 450, 300])

# Cada valor en y corresponde a una fila en X
assert len(X) == len(y)  # Siempre deben coincidir
```

#### 3. El Modelo como Función

El modelo es una función matemática **g** que mapea X → y:

```python
# Conceptualmente
y_predicho = g(X)

# En la práctica
y_predicho = modelo.predict(X)
```

## 📊 Tipos de Problemas Supervisados

### 1. Regresión 📈

**Predecir valores numéricos continuos**

#### Ejemplos Prácticos

```python
from sklearn.linear_model import LinearRegression
import numpy as np

# Problema: Predecir salario basado en años de experiencia
X = np.array([[1], [2], [3], [4], [5]])  # años experiencia
y = np.array([30000, 35000, 42000, 50000, 58000])  # salario

modelo = LinearRegression()
modelo.fit(X, y)

# Predecir salario para 6 años de experiencia
salario_6_años = modelo.predict([[6]])
print(f"Salario estimado: ${salario_6_años[0]:,.0f}")
```

**Casos de uso**:
- Predicción de precios (casas, acciones, productos)
- Estimación de demanda
- Pronóstico de ventas
- Predicción de temperatura
- Estimación de tiempo de entrega

### 2. Clasificación 🏷️

**Predecir categorías o clases**

#### A. Clasificación Binaria (2 clases)

```python
from sklearn.linear_model import LogisticRegression

# Problema: Detectar transacciones fraudulentas
X = [[100, 1, 0],      # [monto, es_internacional, hora_noche]
     [5000, 1, 1],
     [50, 0, 0],
     [10000, 1, 1]]

y = [0, 1, 0, 1]       # 0=legítima, 1=fraude

modelo = LogisticRegression()
modelo.fit(X, y)

# Predecir nueva transacción
nueva_transaccion = [[3000, 1, 1]]
es_fraude = modelo.predict(nueva_transaccion)
probabilidad = modelo.predict_proba(nueva_transaccion)

print(f"¿Es fraude? {bool(es_fraude[0])}")
print(f"Probabilidad de fraude: {probabilidad[0][1]:.2%}")
```

**Casos de uso**:
- Detección de spam (spam/no spam)
- Diagnóstico médico (enfermo/sano)
- Aprobación de crédito (aprobar/rechazar)
- Churn prediction (se va/se queda)
- Detección de fraude

#### B. Clasificación Multiclase (3+ clases)

```python
from sklearn.ensemble import RandomForestClassifier

# Problema: Clasificar tipo de flor
X = [[5.1, 3.5, 1.4, 0.2],  # medidas de pétalos y sépalos
     [6.2, 2.9, 4.3, 1.3],
     [7.3, 2.9, 6.3, 1.8]]

y = ['setosa', 'versicolor', 'virginica']  # 3 especies

modelo = RandomForestClassifier()
modelo.fit(X, y)

# Clasificar nueva flor
nueva_flor = [[5.8, 3.0, 4.5, 1.5]]
especie = modelo.predict(nueva_flor)
print(f"Especie: {especie[0]}")
```

**Casos de uso**:
- Reconocimiento de dígitos (0-9)
- Clasificación de documentos (deportes/política/economía)
- Reconocimiento de emociones (feliz/triste/enojado/neutral)
- Categorización de productos
- Diagnóstico de múltiples enfermedades

### 3. Ranking 🏆

**Ordenar elementos por relevancia**

```python
# Problema: Sistema de recomendación
# Predecir puntuación de relevancia para ordenar

usuario_features = [25, 'M', 'tech']  # edad, género, intereses
productos = [
    {'id': 1, 'categoria': 'tech', 'precio': 500},
    {'id': 2, 'categoria': 'deportes', 'precio': 100},
    {'id': 3, 'categoria': 'tech', 'precio': 1000}
]

# El modelo predice scores de relevancia
scores = modelo.predict_scores(usuario_features, productos)
# scores = [0.9, 0.3, 0.8]

# Ordenar por score descendente
productos_ordenados = sorted(
    zip(productos, scores), 
    key=lambda x: x[1], 
    reverse=True
)
```

**Casos de uso**:
- Motores de búsqueda (ranking de resultados)
- Sistemas de recomendación (Netflix, Spotify)
- Ranking de candidatos en reclutamiento
- Priorización de tareas

## 🔄 El Proceso de Aprendizaje Supervisado

```python
# 1. PREPARAR DATOS
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 2. ELEGIR Y ENTRENAR MODELO
from sklearn.ensemble import RandomForestRegressor

modelo = RandomForestRegressor(n_estimators=100)
modelo.fit(X_train, y_train)  # Aprende de los datos

# 3. EVALUAR
from sklearn.metrics import mean_absolute_error

y_pred = modelo.predict(X_test)
error = mean_absolute_error(y_test, y_pred)
print(f"Error promedio: {error}")

# 4. USAR EN PRODUCCIÓN
nuevos_datos = [[...]]
prediccion = modelo.predict(nuevos_datos)
```

## 🎯 Regresión vs Clasificación: Guía Rápida

| Pregunta | Tipo |
|----------|------|
| ¿Cuánto costará? | Regresión |
| ¿Cuántos clientes tendremos? | Regresión |
| ¿Es spam o no? | Clasificación Binaria |
| ¿Qué categoría es? | Clasificación Multiclase |
| ¿Cuál es la probabilidad de...? | Clasificación |
| ¿En qué orden mostrar resultados? | Ranking |

## 💡 Ejemplo Completo: Predicción de Churn

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report

# 1. Cargar datos
datos = pd.DataFrame({
    'meses_cliente': [12, 3, 24, 6, 36],
    'llamadas_soporte': [0, 5, 1, 3, 0],
    'gasto_mensual': [50, 30, 80, 45, 100],
    'se_fue': [0, 1, 0, 1, 0]  # Target: churn
})

# 2. Separar features y target
X = datos[['meses_cliente', 'llamadas_soporte', 'gasto_mensual']]
y = datos['se_fue']

# 3. Dividir datos
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. Entrenar modelo
modelo = GradientBoostingClassifier()
modelo.fit(X_train, y_train)

# 5. Evaluar
y_pred = modelo.predict(X_test)
print(classification_report(y_test, y_pred))

# 6. Predecir para nuevo cliente
nuevo_cliente = [[18, 2, 65]]  # 18 meses, 2 llamadas, $65/mes
probabilidad_churn = modelo.predict_proba(nuevo_cliente)[0][1]

print(f"Probabilidad de churn: {probabilidad_churn:.2%}")

if probabilidad_churn > 0.7:
    print("⚠️ Cliente en riesgo - activar retención")
```

## 🎯 Puntos Clave

✅ **Supervisado = Aprender de ejemplos etiquetados**

✅ **Regresión** → Predecir números (precio, cantidad, temperatura)

✅ **Clasificación** → Predecir categorías (spam/no spam, tipo de producto)

✅ **Ranking** → Ordenar por relevancia (recomendaciones, búsqueda)

✅ **X (features)** = Lo que conocemos | **y (target)** = Lo que queremos predecir

✅ **El modelo aprende la función** X → y durante el entrenamiento

## 🔄 Próximos Pasos

En la siguiente lección aprenderemos **CRISP-DM**, la metodología estándar para organizar proyectos de Machine Learning de principio a fin.

## 💬 Notas de la Comunidad

* [Notas de Peter Ernicke](https://knowmledge.com/2023/09/11/ml-zoomcamp-2023-introduction-to-machine-learning-part-3/)
* **Comparte tus ejemplos** - ¿Qué problema supervisado estás resolviendo?

---

**📖 Material base**: Adaptado del [ML Zoomcamp](https://github.com/DataTalksClub/machine-learning-zoomcamp) por Alexey Grigorev y DataTalks.Club

---

[⬅️ Anterior: ML vs Reglas](02-ml-vs-rules.md) | [Volver al índice](README.md) | [Siguiente: CRISP-DM ➡️](04-crisp-dm.md)

