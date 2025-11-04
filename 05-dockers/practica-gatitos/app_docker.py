"""
🐱 Gatitos App - Versión Docker
Una aplicación simple de Flask que muestra fotos aleatorias de gatitos
Optimizada para correr en contenedores Docker
"""

from flask import Flask, render_template
import random

app = Flask(__name__)

# Lista de URLs de gatitos de la API pública Cat as a Service
GATITOS = [
    "https://cataas.com/cat",
    "https://cataas.com/cat/cute",
    "https://cataas.com/cat/says/Hello",
    "https://cataas.com/cat/says/Docker",
    "https://cataas.com/cat/says/Meow",
]

@app.route('/')
def home():
    """Página principal con un gatito aleatorio"""
    gatito_url = random.choice(GATITOS)
    # Usar el template específico para Docker
    return render_template('index_docker.html', gatito_url=gatito_url)

@app.route('/health')
def health():
    """Endpoint de salud para verificar que la app está corriendo"""
    return {'status': 'healthy', 'message': '🐱 Gatitos app is running in Docker!'}

if __name__ == '__main__':
    # Importante: host='0.0.0.0' para que Docker pueda acceder desde fuera del contenedor
    print("🐳 Iniciando Gatitos App en Docker...")
    print("📍 La app estará disponible en el puerto mapeado")
    app.run(host='0.0.0.0', port=5000, debug=False)
