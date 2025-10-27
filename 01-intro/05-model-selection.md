## 1.5 Proceso de Selección de Modelos


## Notas

### ¿Qué modelo elegir?

- Regresión logística
- Árbol de decisión
- Red neuronal
- O muchos otros

El conjunto de validación no se usa en el entrenamiento. Hay matrices de características y vectores y
tanto para los conjuntos de entrenamiento como de validación. 
El modelo se ajusta con los datos de entrenamiento, y se usa para predecir los valores y de la matriz
de características de validación. Luego, los valores y predichos (probabilidades)
se comparan con los valores y reales. 

**Problema de comparaciones múltiples (MCP):** simplemente por azar un modelo puede tener suerte y obtener
buenas predicciones porque todos son probabilísticos. 

El conjunto de prueba puede ayudar a evitar el MCP. La obtención del mejor modelo se realiza con los conjuntos de entrenamiento y validación, mientras que el conjunto de prueba se usa para asegurar que el mejor modelo propuesto es el mejor. 

1. Dividir los conjuntos de datos en entrenamiento, validación y prueba. Por ejemplo, 60%, 20% y 20% respectivamente 
2. Entrenar los modelos
3. Evaluar los modelos
4. Seleccionar el mejor modelo 
5. Aplicar el mejor modelo al conjunto de prueba 
6. Comparar las métricas de rendimiento de validación y prueba

<u>Nota:</u> Es posible reutilizar los datos de validación. Después de seleccionar el mejor modelo (paso 4), los conjuntos de validación y entrenamiento pueden combinarse para formar un único conjunto de entrenamiento para el modelo elegido antes de probarlo en el conjunto de prueba.


## Navegación

* [Curso Machine Learning Zoomcamp](../)
* [Lección 1: Introducción al Machine Learning](./)
* Anterior: [CRISP-DM](04-crisp-dm.md)
* Siguiente: [Configuración del Entorno](06-environment.md)
