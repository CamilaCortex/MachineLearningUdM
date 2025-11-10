"""
🐱 Gatitos App - Versión Local (sin Docker)
Una aplicación simple de Flask que muestra fotos aleatorias de gatitos
"""

from flask import Flask, render_template
import random

app = Flask(__name__)

# Lista de URLs de gatitos de la API pública Cat as a Service
GATITOS = [
    "https://cataas.com/cat",
    "https://cataas.com/cat/cute",
    "https://cataas.com/cat/says/Hello",
    "https://cataas.com/cat/says/Python",
    "https://cataas.com/cat/says/Meow",
]

@app.route('/')
def home():
    """Página principal con un gatito aleatorio"""
    gatito_url = random.choice(GATITOS)
    return render_template('index.html', gatito_url=gatito_url)

@app.route('/health')  # ping 
def health():
    """Endpoint de salud para verificar que la app está corriendo"""
    return {'status': 'healthy', 'message': '🐱 Gatitos app is running!'}

if __name__ == '__main__':
    print("🐱 Iniciando Gatitos App...")
    print("📍 Abre tu navegador en: http://127.0.0.1:5000")
    print("⏹️  Para detener: Ctrl+C")
    app.run(host='127.0.0.1', port=5000, debug=True)


# uv run python app.py