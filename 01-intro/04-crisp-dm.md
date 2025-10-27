# 1.4 CRISP-DM: Metodología para Proyectos de ML

> **Objetivo**: Aprender a estructurar proyectos de ML usando la metodología estándar de la industria.

## 📖 Introducción

**CRISP-DM** (Cross-Industry Standard Process for Data Mining) es la metodología más utilizada en la industria para proyectos de Machine Learning y Data Science. Fue creada en 1996 y sigue siendo el estándar de facto porque proporciona un marco estructurado y probado.

## 🔄 Las 6 Fases de CRISP-DM

```
    ┌─────────────────────┐
    │ 1. Comprensión del  │
    │    Negocio          │
    └──────────┬──────────┘
               │
    ┌──────────▼──────────┐
    │ 2. Comprensión de   │
    │    los Datos        │
    └──────────┬──────────┘
               │
    ┌──────────▼──────────┐
    │ 3. Preparación de   │
    │    Datos            │
    └──────────┬──────────┘
               │
    ┌──────────▼──────────┐
    │ 4. Modelado         │◄──┐
    └──────────┬──────────┘   │
               │               │
    ┌──────────▼──────────┐   │
    │ 5. Evaluación       │───┘
    └──────────┬──────────┘
               │
    ┌──────────▼──────────┐
    │ 6. Despliegue       │
    └─────────────────────┘
```

### 1️⃣ Comprensión del Negocio

**Objetivo**: Definir claramente el problema y los objetivos del proyecto.

#### Preguntas Clave

- ¿Qué problema de negocio estamos resolviendo?
- ¿Realmente necesitamos ML para esto?
- ¿Cómo mediremos el éxito?
- ¿Cuál es el impacto esperado?

#### Ejemplo Práctico

```python
# Documento de proyecto: Sistema de predicción de churn

PROBLEMA_NEGOCIO = {
    'descripcion': 'Clientes abandonan el servicio sin previo aviso',
    'impacto_actual': 'Pérdida de $500K mensuales',
    'objetivo': 'Predecir qué clientes están en riesgo de irse',
    'metrica_exito': 'Reducir churn en 20% en 6 meses',
    'necesita_ml': True,  # Patrones complejos, muchos datos
    'alternativas_evaluadas': ['Reglas simples', 'Análisis manual']
}

# Criterios de éxito medibles
METRICAS_NEGOCIO = {
    'precision_minima': 0.75,  # 75% de predicciones correctas
    'recall_minimo': 0.60,     # Detectar 60% de churners
    'tiempo_respuesta': '< 100ms',
    'costo_falso_positivo': '$10',  # Costo de retener cliente que no se iría
    'costo_falso_negativo': '$500'  # Costo de perder cliente
}
```

### 2️⃣ Comprensión de los Datos

**Objetivo**: Explorar y entender los datos disponibles.

#### Actividades

```python
import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos
df = pd.read_csv('clientes.csv')

# 1. Exploración inicial
print(f"Filas: {len(df)}, Columnas: {len(df.columns)}")
print(df.info())
print(df.describe())

# 2. Verificar calidad
print(f"\nValores nulos:\n{df.isnull().sum()}")
print(f"\nDuplicados: {df.duplicated().sum()}")

# 3. Análisis de distribución del target
print(f"\nDistribución de churn:")
print(df['churn'].value_counts(normalize=True))

# 4. Visualizar relaciones
df.groupby('churn')['meses_cliente'].mean().plot(kind='bar')
plt.title('Meses promedio por grupo')
plt.show()

# 5. Identificar problemas
PROBLEMAS_DATOS = {
    'valores_nulos': df.isnull().sum().sum(),
    'desbalanceo_clases': df['churn'].value_counts()[1] / len(df),
    'outliers_detectados': True,
    'necesita_mas_datos': len(df) < 10000
}
```

#### Checklist de Calidad de Datos

- ✅ ¿Tenemos suficientes datos? (mínimo 1000 ejemplos)
- ✅ ¿Los datos son representativos?
- ✅ ¿Hay valores nulos o inconsistentes?
- ✅ ¿Las clases están balanceadas?
- ✅ ¿Necesitamos datos adicionales?

### 3️⃣ Preparación de Datos

**Objetivo**: Transformar datos crudos en formato listo para ML.

#### Pipeline de Preparación

```python
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

# 1. Limpieza
def limpiar_datos(df):
    # Eliminar duplicados
    df = df.drop_duplicates()
    
    # Corregir tipos de datos
    df['fecha_registro'] = pd.to_datetime(df['fecha_registro'])
    
    # Eliminar outliers extremos
    Q1 = df['gasto_mensual'].quantile(0.25)
    Q3 = df['gasto_mensual'].quantile(0.75)
    IQR = Q3 - Q1
    df = df[~((df['gasto_mensual'] < (Q1 - 3 * IQR)) | 
              (df['gasto_mensual'] > (Q3 + 3 * IQR)))]
    
    return df

# 2. Feature Engineering
def crear_features(df):
    # Features temporales
    df['dias_desde_registro'] = (pd.Timestamp.now() - df['fecha_registro']).dt.days
    df['mes_registro'] = df['fecha_registro'].dt.month
    
    # Features de comportamiento
    df['gasto_por_mes'] = df['gasto_total'] / df['meses_cliente']
    df['llamadas_por_mes'] = df['llamadas_soporte'] / df['meses_cliente']
    
    # Features categóricas
    df = pd.get_dummies(df, columns=['plan_tipo', 'region'])
    
    return df

# 3. Pipeline completo
preprocessing_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Aplicar
df_limpio = limpiar_datos(df)
df_features = crear_features(df_limpio)
X = df_features.drop('churn', axis=1)
y = df_features['churn']
X_procesado = preprocessing_pipeline.fit_transform(X)
```

### 4️⃣ Modelado

**Objetivo**: Entrenar y comparar diferentes modelos.

```python
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

# Probar múltiples modelos
modelos = {
    'Logistic Regression': LogisticRegression(),
    'Random Forest': RandomForestClassifier(n_estimators=100),
    'Gradient Boosting': GradientBoostingClassifier()
}

resultados = {}
for nombre, modelo in modelos.items():
    scores = cross_val_score(modelo, X_procesado, y, cv=5, scoring='f1')
    resultados[nombre] = {
        'f1_mean': scores.mean(),
        'f1_std': scores.std()
    }
    print(f"{nombre}: F1={scores.mean():.3f} (+/- {scores.std():.3f})")

# Seleccionar mejor modelo
mejor_modelo = max(resultados, key=lambda x: resultados[x]['f1_mean'])
print(f"\n🏆 Mejor modelo: {mejor_modelo}")
```

### 5️⃣ Evaluación

**Objetivo**: Validar que el modelo resuelve el problema de negocio.

```python
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

# Entrenar modelo final
modelo_final = GradientBoostingClassifier()
modelo_final.fit(X_train, y_train)

# Predecir en test set
y_pred = modelo_final.predict(X_test)
y_proba = modelo_final.predict_proba(X_test)[:, 1]

# Métricas técnicas
print("Reporte de Clasificación:")
print(classification_report(y_test, y_pred))

# Matriz de confusión
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d')
plt.title('Matriz de Confusión')
plt.show()

# Evaluación de negocio
def evaluar_impacto_negocio(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    
    # Costos
    costo_fp = fp * 10   # $10 por falso positivo
    costo_fn = fn * 500  # $500 por falso negativo
    ahorro_tp = tp * 500 # $500 ahorrado por cada churn detectado
    
    roi = ahorro_tp - (costo_fp + costo_fn)
    
    return {
        'clientes_salvados': tp,
        'costo_total': costo_fp + costo_fn,
        'ahorro_total': ahorro_tp,
        'roi': roi,
        'roi_mensual': roi
    }

impacto = evaluar_impacto_negocio(y_test, y_pred)
print(f"\n💰 ROI Estimado: ${impacto['roi']:,.0f}/mes")
```

#### Preguntas de Evaluación

- ✅ ¿El modelo cumple las métricas técnicas?
- ✅ ¿Resuelve el problema de negocio?
- ✅ ¿El ROI justifica la inversión?
- ✅ ¿Es mejor que la solución actual?
- ✅ ¿Es interpretable para stakeholders?

### 6️⃣ Despliegue

**Objetivo**: Poner el modelo en producción.

```python
import joblib
from flask import Flask, request, jsonify

# 1. Guardar modelo
joblib.dump(modelo_final, 'modelo_churn_v1.pkl')
joblib.dump(preprocessing_pipeline, 'pipeline_v1.pkl')

# 2. API de predicción
app = Flask(__name__)

modelo = joblib.load('modelo_churn_v1.pkl')
pipeline = joblib.load('pipeline_v1.pkl')

@app.route('/predict', methods=['POST'])
def predecir_churn():
    # Recibir datos
    datos_cliente = request.json
    
    # Preparar features
    X_nuevo = pd.DataFrame([datos_cliente])
    X_procesado = pipeline.transform(X_nuevo)
    
    # Predecir
    probabilidad = modelo.predict_proba(X_procesado)[0][1]
    prediccion = 'alto_riesgo' if probabilidad > 0.7 else 'bajo_riesgo'
    
    return jsonify({
        'cliente_id': datos_cliente['id'],
        'riesgo_churn': prediccion,
        'probabilidad': float(probabilidad),
        'accion_recomendada': 'contactar_retencion' if probabilidad > 0.7 else 'monitorear'
    })

# 3. Monitoreo
def monitorear_modelo():
    """Verificar performance en producción"""
    predicciones_mes = cargar_predicciones_mes_actual()
    resultados_reales = cargar_resultados_reales()
    
    precision_actual = calcular_precision(predicciones_mes, resultados_reales)
    
    if precision_actual < 0.70:  # Umbral de alerta
        enviar_alerta("⚠️ Modelo degradado - reentrenar")
```

## 🔄 Naturaleza Iterativa

CRISP-DM no es lineal. Constantemente vuelves a fases anteriores:

```python
# Ciclo típico de iteración
iteracion = 1
while not modelo_satisfactorio:
    print(f"\n=== Iteración {iteracion} ===")
    
    # Modelado
    modelo = entrenar_modelo(X_train, y_train)
    
    # Evaluación
    metricas = evaluar_modelo(modelo, X_test, y_test)
    
    if metricas['f1'] < 0.75:
        # Volver a preparación de datos
        print("❌ Métricas bajas - mejorar features")
        X_train, X_test = agregar_nuevas_features(X_train, X_test)
    elif metricas['roi'] < 50000:
        # Volver a comprensión de negocio
        print("❌ ROI bajo - revisar objetivos")
        ajustar_umbrales_decision()
    else:
        print("✅ Modelo satisfactorio")
        modelo_satisfactorio = True
    
    iteracion += 1
```

## 🎯 Puntos Clave

✅ **CRISP-DM estructura proyectos de ML** de principio a fin

✅ **6 fases**: Negocio → Datos → Preparación → Modelado → Evaluación → Despliegue

✅ **Es iterativo**: Vuelves a fases anteriores según resultados

✅ **Enfoque en negocio**: No solo métricas técnicas, también ROI

✅ **Documentación**: Cada fase debe estar documentada

## 💡 Consejos Prácticos

1. **Empieza simple**: Modelo baseline primero
2. **Itera rápido**: Ciclos cortos de 1-2 semanas
3. **Mide siempre**: Métricas técnicas Y de negocio
4. **Comunica**: Actualiza stakeholders regularmente
5. **Documenta**: Decisiones y experimentos

## 🔄 Próximos Pasos

En la siguiente lección profundizaremos en el **Proceso de Selección de Modelos**, una parte crítica de la fase de Modelado.

## 💬 Notas de la Comunidad

* [Notas de Peter Ernicke](https://knowmledge.com/2023/09/12/ml-zoomcamp-2023-introduction-to-machine-learning-part-4/)
* **Comparte tu experiencia** - ¿Qué fase te resulta más desafiante?

---

**📖 Material base**: Adaptado del [ML Zoomcamp](https://github.com/DataTalksClub/machine-learning-zoomcamp) por Alexey Grigorev y DataTalks.Club

---

[⬅️ Anterior: ML Supervisado](03-supervised-ml.md) | [Volver al índice](README.md) | [Siguiente: Selección de Modelos ➡️](05-model-selection.md)

