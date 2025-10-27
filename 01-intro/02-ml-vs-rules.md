# 1.2 Machine Learning vs Sistemas Basados en Reglas

> **Objetivo**: Entender cuándo usar ML y cuándo un sistema basado en reglas es más apropiado.

## 📖 Introducción

Como desarrolladores, nuestra primera inclinación es resolver problemas con código: escribir funciones, condicionales y reglas lógicas. Pero ¿cuándo deberíamos considerar Machine Learning en lugar de código tradicional? Esta lección te ayudará a tomar esa decisión.

## 🎯 Caso de Estudio: Filtro de Spam

Analicemos un problema real que ilustra perfectamente esta diferencia: **detectar correos spam**.

### Enfoque 1: Sistema Basado en Reglas

#### Implementación Inicial

```python
def es_spam_v1(email):
    """Primera versión: reglas simples"""
    spam_keywords = ['gratis', 'ganador', 'premio', 'urgente', 'click aquí']
    
    # Regla 1: Verificar palabras clave
    texto_lower = email['texto'].lower()
    for keyword in spam_keywords:
        if keyword in texto_lower:
            return True
    
    # Regla 2: Verificar remitente sospechoso
    if '@suspicious-domain.com' in email['remitente']:
        return True
    
    # Regla 3: Demasiados signos de exclamación
    if email['texto'].count('!') > 3:
        return True
    
    return False
```

**Parece simple, ¿verdad?** Pero veamos qué pasa en la realidad...

#### El Problema: Evolución del Spam

```python
def es_spam_v2(email):
    """Segunda versión: más reglas para evadir spammers"""
    spam_keywords = [
        'gratis', 'gr4tis', 'g-r-a-t-i-s', 'grat1s',  # Variaciones
        'ganador', 'g@nador', 'gan4dor',
        'premio', 'pr3mio', 'p.r.e.m.i.o',
        # ... 100+ variaciones más
    ]
    
    # Regla 1: Palabras clave (ahora con 100+ variaciones)
    texto_normalizado = normalizar_texto(email['texto'])
    for keyword in spam_keywords:
        if keyword in texto_normalizado:
            return True
    
    # Regla 2: Remitentes sospechosos (lista creciente)
    dominios_spam = cargar_lista_dominios_spam()  # 10,000+ dominios
    if email['remitente'].split('@')[1] in dominios_spam:
        return True
    
    # Regla 3: Signos de exclamación
    if email['texto'].count('!') > 3:
        return True
    
    # Regla 4: Mayúsculas excesivas
    if sum(1 for c in email['texto'] if c.isupper()) / len(email['texto']) > 0.5:
        return True
    
    # Regla 5: Enlaces sospechosos
    if contar_enlaces(email['texto']) > 5:
        return True
    
    # Regla 6-20: ... más reglas
    # El código crece exponencialmente
    
    return False
```

#### Problemas del Enfoque Basado en Reglas

1. **Mantenimiento Insostenible**
   - Cada nueva táctica de spam requiere código nuevo
   - Las reglas se vuelven cada vez más complejas
   - Difícil de testear todas las combinaciones

2. **Falsos Positivos**
   ```python
   # Email legítimo bloqueado por error
   email_legítimo = {
       'texto': '¡Felicidades! Ganaste el concurso de fotografía',
       'remitente': 'concursos@empresa-legitima.com'
   }
   # es_spam_v2(email_legítimo) → True (¡ERROR!)
   ```

3. **Requiere Experiencia del Dominio**
   - Necesitas ser experto en spam para escribir buenas reglas
   - El conocimiento está codificado en el programa

4. **No Se Adapta Automáticamente**
   - Cada cambio requiere actualización manual del código
   - Deploy constante de nuevas versiones

### Enfoque 2: Machine Learning

#### Implementación con ML

```python
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# 1. Preparar datos de entrenamiento
emails_entrenamiento = pd.DataFrame({
    'texto': [
        'Gana dinero fácil haciendo click aquí',
        'Reunión de equipo mañana a las 10am',
        '¡URGENTE! Has ganado un premio',
        'Informe trimestral adjunto',
        'Oferta exclusiva solo por hoy',
        'Confirmación de tu pedido #12345'
    ],
    'es_spam': [1, 0, 1, 0, 1, 0]  # 1=spam, 0=legítimo
})

# 2. Crear y entrenar el modelo
modelo_spam = Pipeline([
    ('vectorizer', TfidfVectorizer(max_features=1000)),
    ('classifier', MultinomialNB())
])

modelo_spam.fit(
    emails_entrenamiento['texto'], 
    emails_entrenamiento['es_spam']
)

# 3. Usar el modelo
def es_spam_ml(email_texto):
    probabilidad = modelo_spam.predict_proba([email_texto])[0][1]
    return probabilidad > 0.5, probabilidad

# Probar
texto_nuevo = "Oferta especial para ti"
es_spam, confianza = es_spam_ml(texto_nuevo)
print(f"¿Es spam? {es_spam} (confianza: {confianza:.2%})")
```

#### Ventajas del Enfoque ML

1. **Aprende Automáticamente**
   ```python
   # Solo necesitas más ejemplos, no más código
   nuevos_ejemplos = cargar_nuevos_emails_etiquetados()
   modelo_spam.fit(nuevos_ejemplos['texto'], nuevos_ejemplos['es_spam'])
   ```

2. **Se Adapta al Cambio**
   - El modelo aprende nuevos patrones de spam
   - No necesitas codificar cada variación manualmente

3. **Maneja Complejidad**
   - Descubre patrones que los humanos no ven
   - Combina múltiples señales automáticamente

4. **Probabilidades en Lugar de Binario**
   ```python
   # Puedes ajustar el umbral según tus necesidades
   _, confianza = es_spam_ml(email)
   if confianza > 0.9:
       print("Definitivamente spam")
   elif confianza > 0.5:
       print("Probablemente spam - revisar")
   else:
       print("Legítimo")
   ```

## 📊 Comparación Directa

| Aspecto | Sistemas Basados en Reglas | Machine Learning |
|---------|---------------------------|------------------|
| **Complejidad Inicial** | Baja - fácil empezar | Media - requiere datos |
| **Mantenimiento** | Alto - código crece constantemente | Bajo - reentrenar con nuevos datos |
| **Adaptabilidad** | Manual - requiere código nuevo | Automática - aprende de datos |
| **Explicabilidad** | Alta - reglas claras | Variable - depende del modelo |
| **Datos Requeridos** | No requiere | Sí - necesita ejemplos etiquetados |
| **Precisión** | Limitada por reglas | Mejora con más datos |

## 🎯 ¿Cuándo Usar Cada Enfoque?

### Usa Sistemas Basados en Reglas Cuando:

✅ **Las reglas son claras y estables**
```python
def puede_votar(edad, es_ciudadano):
    return edad >= 18 and es_ciudadano
```

✅ **Necesitas explicabilidad total**
```python
# Sistemas médicos críticos, legales, financieros
def aprobar_credito(ingreso, deuda, historial):
    if ingreso < 30000:
        return False, "Ingreso insuficiente"
    if deuda / ingreso > 0.4:
        return False, "Ratio deuda/ingreso muy alto"
    # Reglas claras y auditables
```

✅ **Tienes pocos datos o ninguno**

✅ **El problema es simple**

### Usa Machine Learning Cuando:

✅ **Los patrones son complejos**
```python
# Reconocimiento de imágenes, procesamiento de lenguaje natural
modelo.predict(imagen)  # Imposible con reglas simples
```

✅ **Los patrones cambian con el tiempo**
```python
# Detección de fraude, spam, tendencias
# Los atacantes adaptan sus estrategias constantemente
```

✅ **Tienes muchos datos etiquetados**

✅ **Necesitas adaptación automática**

✅ **Las reglas serían demasiado complejas de codificar**

## 🔄 Enfoque Híbrido: Lo Mejor de Ambos Mundos

En la práctica, muchos sistemas combinan ambos enfoques:

```python
def clasificar_email_hibrido(email):
    # 1. Reglas de negocio claras primero
    if email['remitente'] in lista_blanca:
        return 'legitimo', 1.0
    
    if email['remitente'] in lista_negra:
        return 'spam', 1.0
    
    # 2. ML para casos ambiguos
    es_spam, confianza = modelo_ml.predict(email['texto'])
    
    # 3. Reglas de validación final
    if es_spam and confianza < 0.6:
        # Baja confianza - enviar a revisión humana
        return 'revisar', confianza
    
    return 'spam' if es_spam else 'legitimo', confianza
```

## 💡 Ejemplo Práctico: Sistema de Recomendación

```python
def recomendar_productos(usuario_id):
    # Regla de negocio: No recomendar productos agotados
    productos_disponibles = obtener_productos_en_stock()
    
    # ML: Predecir qué le gustará al usuario
    recomendaciones_ml = modelo_recomendacion.predict(
        usuario_id, 
        productos_disponibles
    )
    
    # Regla de negocio: Filtrar por política de la empresa
    recomendaciones_finales = [
        p for p in recomendaciones_ml 
        if p.precio <= usuario.limite_credito
        and p.categoria not in usuario.categorias_bloqueadas
    ]
    
    return recomendaciones_finales[:10]
```

## 🎯 Puntos Clave

✅ **Sistemas basados en reglas**: Simples al inicio, pero difíciles de mantener

✅ **Machine Learning**: Requiere datos, pero se adapta automáticamente

✅ **Híbrido**: Combina reglas de negocio claras con ML para casos complejos

✅ **La elección depende**: Complejidad, datos disponibles, y necesidad de adaptación

✅ **No siempre necesitas ML**: Empieza simple, evoluciona cuando sea necesario

## 🔄 Próximos Pasos

Ahora que entiendes cuándo usar ML, en la siguiente lección profundizaremos en **Machine Learning Supervisado**, el tipo más común de ML en aplicaciones empresariales.

## 💬 Notas de la Comunidad

* [Notas de Peter Ernicke](https://knowmledge.com/2023/09/10/ml-zoomcamp-2023-introduction-to-machine-learning-part-2/)
* **Comparte tu experiencia** - ¿Has migrado de reglas a ML? Cuéntanos tu caso

---

**📖 Material base**: Adaptado del [ML Zoomcamp](https://github.com/DataTalksClub/machine-learning-zoomcamp) por Alexey Grigorev y DataTalks.Club

---

[⬅️ Anterior: ¿Qué es ML?](01-what-is-ml.md) | [Volver al índice](README.md) | [Siguiente: ML Supervisado ➡️](03-supervised-ml.md)
