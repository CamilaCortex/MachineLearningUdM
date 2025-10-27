# 1.1 ¿Qué es Machine Learning?

> **Objetivo**: Comprender los fundamentos de Machine Learning y cómo se diferencia de la programación tradicional.

## 📖 Introducción

Como desarrollador de software, estás acostumbrado a escribir código que sigue reglas explícitas: "si esto, entonces aquello". Machine Learning (ML) representa un cambio de paradigma fundamental: en lugar de programar reglas, **enseñamos a las computadoras a aprender patrones de los datos**.

## 🎯 ¿Qué es Machine Learning?

**Machine Learning** es una rama de la Inteligencia Artificial que permite a los sistemas aprender y mejorar automáticamente a partir de la experiencia sin ser explícitamente programados.

### Definición Práctica

En términos de desarrollo de software:

```
Programación Tradicional: Datos + Reglas → Resultados
Machine Learning: Datos + Resultados → Reglas (Modelo)
```

## 💡 Ejemplo Práctico: Predicción de Precios de Automóviles

Imaginemos que necesitas construir un sistema para estimar el precio de automóviles usados.

### Enfoque Tradicional (Sin ML)

```python
def calcular_precio_auto(año, kilometraje, marca):
    precio_base = 20000
    
    # Reglas codificadas manualmente
    if año < 2015:
        precio_base -= 5000
    if kilometraje > 100000:
        precio_base -= 3000
    if marca == "Toyota":
        precio_base += 2000
    
    return precio_base
```

**Problemas**:
- Reglas simplistas y poco precisas
- Difícil mantener y actualizar
- No captura relaciones complejas
- Requiere conocimiento experto del dominio

### Enfoque con Machine Learning

```python
import pandas as pd
from sklearn.linear_model import LinearRegression

# 1. Datos históricos
datos = pd.DataFrame({
    'año': [2018, 2015, 2020, 2017, 2019],
    'kilometraje': [50000, 120000, 30000, 80000, 45000],
    'marca_toyota': [1, 0, 1, 0, 1],
    'precio': [18000, 12000, 22000, 15000, 19000]
})

# 2. Entrenar el modelo
X = datos[['año', 'kilometraje', 'marca_toyota']]
y = datos['precio']

modelo = LinearRegression()
modelo.fit(X, y)  # El modelo aprende los patrones

# 3. Predecir nuevos precios
nuevo_auto = [[2019, 60000, 1]]
precio_estimado = modelo.predict(nuevo_auto)
print(f"Precio estimado: ${precio_estimado[0]:,.2f}")
```

**Ventajas**:
- Aprende patrones complejos automáticamente
- Se adapta a nuevos datos
- Mejora con más información
- No requiere reglas explícitas

## 🔑 Conceptos Fundamentales

### 1. Features (Características)

Son las **variables de entrada** que describen el objeto que queremos analizar.

**Ejemplo**: Para predecir precios de autos
- Año de fabricación
- Kilometraje
- Marca
- Modelo
- Color
- Número de puertas

```python
features = {
    'año': 2019,
    'kilometraje': 45000,
    'marca': 'Toyota',
    'modelo': 'Corolla',
    'puertas': 4
}
```

### 2. Target (Objetivo)

Es la **variable que queremos predecir**.

**Ejemplo**: 
- Precio del automóvil
- Probabilidad de falla
- Categoría del producto

```python
target = 19500  # Precio en dólares
```

### 3. Modelo

Es la **representación matemática** de los patrones aprendidos de los datos.

```python
# El modelo es una función que mapea features → target
precio = modelo.predict(features)
```

### 4. Entrenamiento

Es el **proceso de aprendizaje** donde el modelo encuentra patrones en los datos históricos.

```python
# Durante el entrenamiento
modelo.fit(X_train, y_train)  # Aprende de ejemplos pasados
```

### 5. Predicción

Es la **aplicación del modelo** a nuevos datos para obtener resultados.

```python
# Durante la predicción
precio_nuevo = modelo.predict(X_nuevo)  # Aplica lo aprendido
```

## 🎓 Proceso de Machine Learning

```
1. Recolectar Datos
   ↓
2. Preparar Datos (limpieza, transformación)
   ↓
3. Seleccionar Features
   ↓
4. Entrenar Modelo
   ↓
5. Evaluar Modelo
   ↓
6. Hacer Predicciones
```

## 🚀 Casos de Uso Reales

### 1. E-commerce
- **Recomendación de productos**: "Clientes que compraron X también compraron Y"
- **Detección de fraude**: Identificar transacciones sospechosas
- **Optimización de precios**: Ajustar precios dinámicamente

### 2. Finanzas
- **Aprobación de créditos**: Evaluar riesgo crediticio
- **Trading algorítmico**: Predicción de movimientos del mercado
- **Detección de lavado de dinero**: Identificar patrones sospechosos

### 3. Salud
- **Diagnóstico médico**: Detectar enfermedades en imágenes
- **Predicción de readmisiones**: Identificar pacientes en riesgo
- **Descubrimiento de medicamentos**: Analizar compuestos químicos

### 4. Tecnología
- **Filtros de spam**: Clasificar correos electrónicos
- **Reconocimiento de voz**: Asistentes virtuales
- **Traducción automática**: Google Translate

## ⚠️ Cuándo NO usar Machine Learning

ML no es siempre la solución. **No uses ML cuando**:

1. **Las reglas son simples y claras**
   ```python
   # No necesitas ML para esto
   def es_mayor_edad(edad):
       return edad >= 18
   ```

2. **Tienes pocos datos** (< 100 ejemplos típicamente)

3. **Necesitas explicabilidad total** (sistemas críticos de seguridad)

4. **Los datos no son representativos** del problema real

5. **El costo de errores es muy alto** sin supervisión humana

## 🎯 Puntos Clave

✅ **ML aprende patrones de datos** en lugar de seguir reglas programadas

✅ **Features** son las entradas, **Target** es lo que predecimos

✅ **El modelo** es la representación de patrones aprendidos

✅ **Entrenamiento** es el proceso de aprendizaje

✅ **ML es poderoso** pero no siempre es la mejor solución

## 🔄 Próximos Pasos

En la siguiente lección exploraremos las diferencias detalladas entre sistemas basados en reglas y Machine Learning, con ejemplos prácticos de cuándo usar cada enfoque.

## 📚 Recursos Adicionales

- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Machine Learning Crash Course - Google](https://developers.google.com/machine-learning/crash-course)
- [Fast.ai Practical Deep Learning](https://course.fast.ai/)

## 💬 Notas de la Comunidad

¿Tienes preguntas o comentarios sobre este tema? Comparte tus notas:

* [Notas de Peter Ernicke](https://knowmledge.com/2023/09/09/ml-zoomcamp-2023-introduction-to-machine-learning-part-1/)
* **Agrega tus notas aquí** - Envía un PR

---

**📖 Material base**: Adaptado del [ML Zoomcamp](https://github.com/DataTalksClub/machine-learning-zoomcamp) por Alexey Grigorev y DataTalks.Club

---

[⬅️ Volver al índice](README.md) | [Siguiente: ML vs Sistemas Basados en Reglas ➡️](02-ml-vs-rules.md)
