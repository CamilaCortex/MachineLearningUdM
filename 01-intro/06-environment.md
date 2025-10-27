# 1.6 Configuración del Entorno de Desarrollo

> **Objetivo**: Configurar tu máquina local con todas las herramientas necesarias para el curso de Machine Learning.

## 📋 Tabla de Contenidos

1. [Instalación de Git](#1-instalación-de-git)
2. [Configuración de SSH para GitHub](#2-configuración-de-ssh-para-github)
3. [Instalación de Python con uv](#3-instalación-de-python-con-uv)
4. [Gestión de Entornos Virtuales con uv](#4-gestión-de-entornos-virtuales-con-uv)
5. [Instalación de Dependencias del Curso](#5-instalación-de-dependencias-del-curso)
6. [Verificación de la Instalación](#6-verificación-de-la-instalación)

---

## 1. Instalación de Git

Git es el sistema de control de versiones que usaremos para gestionar el código del curso.

### 🍎 macOS

#### Opción 1: Usando Homebrew (Recomendado)

```bash
# 1. Instalar Homebrew si no lo tienes
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Instalar Git
brew install git

# 3. Verificar instalación
git --version
# Debería mostrar: git version 2.x.x
```

#### Opción 2: Usando el instalador oficial

1. Descarga el instalador desde: https://git-scm.com/download/mac
2. Ejecuta el archivo `.dmg` descargado
3. Sigue las instrucciones del instalador

### 🪟 Windows

#### Opción 1: Git for Windows (Recomendado)

1. Descarga Git desde: https://git-scm.com/download/win
2. Ejecuta el instalador descargado
3. **Configuración recomendada durante la instalación:**
   - Editor: Selecciona "Use Visual Studio Code" (o tu editor preferido)
   - PATH: "Git from the command line and also from 3rd-party software"
   - SSH: "Use bundled OpenSSH"
   - HTTPS: "Use the OpenSSL library"
   - Line endings: "Checkout Windows-style, commit Unix-style"
   - Terminal: "Use MinTTY"
   - Git Credential Manager: Marcar esta opción

4. Verifica la instalación abriendo **Git Bash** o **PowerShell**:

```bash
git --version
# Debería mostrar: git version 2.x.x
```

### Configuración Inicial de Git (Ambos Sistemas)

```bash
# Configurar tu nombre (reemplaza con tu nombre real)
git config --global user.name "Tu Nombre"

# Configurar tu email (usa el mismo email de GitHub)
git config --global user.email "tu.email@ejemplo.com"

# Configurar editor predeterminado (opcional)
git config --global core.editor "code --wait"  # Para VS Code

# Verificar configuración
git config --list
```

---

## 2. Configuración de SSH para GitHub

SSH te permite conectarte a GitHub sin ingresar tu contraseña cada vez.

### 🍎 macOS

#### Paso 1: Verificar si ya tienes llaves SSH

```bash
# Abrir Terminal y ejecutar:
ls -la ~/.ssh

# Si ves archivos como id_ed25519 o id_rsa, ya tienes llaves
# Si no, continúa con el paso 2
```

#### Paso 2: Generar nueva llave SSH

```bash
# Genera una nueva llave SSH (reemplaza con tu email de GitHub)
ssh-keygen -t ed25519 -C "tu.email@ejemplo.com"

# Cuando pregunte "Enter file in which to save the key", presiona Enter
# Cuando pregunte por passphrase, puedes:
#   - Dejar en blanco (menos seguro pero más conveniente)
#   - O crear una contraseña (más seguro)
```

#### Paso 3: Agregar la llave al ssh-agent

```bash
# Iniciar el ssh-agent
eval "$(ssh-agent -s)"

# Crear/editar el archivo de configuración SSH
touch ~/.ssh/config
open -e ~/.ssh/config

# Agregar estas líneas al archivo:
```

Copia y pega esto en el archivo `~/.ssh/config`:

```
Host github.com
  AddKeysToAgent yes
  UseKeychain yes
  IdentityFile ~/.ssh/id_ed25519
```

Guarda y cierra el archivo, luego ejecuta:

```bash
# Agregar la llave al ssh-agent
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

#### Paso 4: Copiar la llave pública

```bash
# Copiar la llave pública al portapapeles
pbcopy < ~/.ssh/id_ed25519.pub

# O mostrarla en pantalla para copiarla manualmente
cat ~/.ssh/id_ed25519.pub
```

### 🪟 Windows

#### Paso 1: Abrir PowerShell o Git Bash

Abre **PowerShell** como administrador o **Git Bash**.

#### Paso 2: Verificar llaves existentes

```bash
# En PowerShell:
ls ~\.ssh

# En Git Bash:
ls -la ~/.ssh

# Si ves archivos como id_ed25519 o id_rsa, ya tienes llaves
```

#### Paso 3: Generar nueva llave SSH

```bash
# Genera una nueva llave SSH
ssh-keygen -t ed25519 -C "tu.email@ejemplo.com"

# Presiona Enter para aceptar la ubicación predeterminada
# Opcionalmente, ingresa una passphrase
```

#### Paso 4: Iniciar el ssh-agent

**En PowerShell (como administrador):**

```powershell
# Configurar el servicio ssh-agent para inicio automático
Get-Service ssh-agent | Set-Service -StartupType Automatic

# Iniciar el servicio
Start-Service ssh-agent

# Agregar la llave
ssh-add ~\.ssh\id_ed25519
```

**En Git Bash:**

```bash
# Iniciar ssh-agent
eval "$(ssh-agent -s)"

# Agregar la llave
ssh-add ~/.ssh/id_ed25519
```

#### Paso 5: Copiar la llave pública

**En PowerShell:**

```powershell
# Copiar al portapapeles
Get-Content ~\.ssh\id_ed25519.pub | Set-Clipboard

# O mostrar en pantalla
cat ~\.ssh\id_ed25519.pub
```

**En Git Bash:**

```bash
# Copiar al portapapeles (si tienes clip)
cat ~/.ssh/id_ed25519.pub | clip

# O mostrar en pantalla
cat ~/.ssh/id_ed25519.pub
```

### Agregar la Llave SSH a GitHub (Ambos Sistemas)

1. Ve a GitHub: https://github.com/settings/keys
2. Haz clic en **"New SSH key"**
3. Dale un título descriptivo (ej: "Mi MacBook Pro" o "PC Windows Casa")
4. Pega la llave pública que copiaste
5. Haz clic en **"Add SSH key"**

### Probar la Conexión SSH

```bash
# Probar conexión a GitHub
ssh -T git@github.com

# Deberías ver un mensaje como:
# Hi tu-usuario! You've successfully authenticated...
```

---

## 3. Instalación de Python con uv

**uv** es un gestor de paquetes y entornos de Python extremadamente rápido, escrito en Rust.

### 🍎 macOS

```bash
# Instalar uv usando curl
curl -LsSf https://astral.sh/uv/install.sh | sh

# O usando Homebrew
brew install uv

# Verificar instalación
uv --version

# Agregar uv al PATH (si es necesario)
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### 🪟 Windows

**Opción 1: PowerShell (Recomendado)**

```powershell
# Ejecutar en PowerShell
irm https://astral.sh/uv/install.ps1 | iex

# Verificar instalación
uv --version
```

**Opción 2: Usando pip**

```bash
# Si ya tienes Python instalado
pip install uv

# Verificar
uv --version
```

### Instalar Python con uv

```bash
# Instalar Python 3.11 (versión recomendada para el curso)
uv python install 3.11

# Verificar versiones disponibles
uv python list

# Ver la versión instalada
uv python pin 3.11
```

---

## 4. Gestión de Entornos Virtuales con uv

Los entornos virtuales mantienen las dependencias del proyecto aisladas.

### Crear un Entorno Virtual

```bash
# Navegar a la carpeta de tu proyecto
cd ~/proyectos/machine-learning-zoomcamp

# Crear entorno virtual con Python 3.11
uv venv --python 3.11

# Esto crea una carpeta .venv en tu proyecto
```

### Activar el Entorno Virtual

#### 🍎 macOS / Linux

```bash
# Activar el entorno
source .venv/bin/activate

# Verás (venv) o (.venv) al inicio de tu prompt
# Ejemplo: (.venv) usuario@mac:~/proyecto$
```

#### 🪟 Windows

**PowerShell:**

```powershell
# Activar el entorno
.\.venv\Scripts\Activate.ps1

# Si obtienes error de permisos, ejecuta primero:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Command Prompt (CMD):**

```cmd
.\.venv\Scripts\activate.bat
```

**Git Bash:**

```bash
source .venv/Scripts/activate
```

### Desactivar el Entorno Virtual

```bash
# En cualquier sistema operativo
deactivate
```

### Comandos Útiles de uv

```bash
# Ver información del entorno actual
uv venv --help

# Eliminar entorno virtual
rm -rf .venv  # macOS/Linux
rmdir /s .venv  # Windows CMD

# Crear entorno con nombre específico
uv venv mi-entorno --python 3.11

# Listar paquetes instalados
uv pip list

# Actualizar uv
uv self update
```

---

## 5. Instalación de Dependencias del Curso

### Método 1: Instalación Directa con uv (Recomendado)

```bash
# Asegúrate de tener el entorno activado
# Deberías ver (.venv) en tu prompt

# Instalar paquetes básicos de ML
uv pip install numpy pandas scikit-learn matplotlib seaborn jupyter

# Instalar paquetes adicionales
uv pip install ipykernel notebook jupyterlab

# Para análisis de datos
uv pip install plotly scipy statsmodels

# Verificar instalación
uv pip list
```

### Método 2: Usando archivo requirements.txt

Crea un archivo `requirements.txt` en tu proyecto:

```txt
# requirements.txt
numpy>=1.24.0
pandas>=2.0.0
scikit-learn>=1.3.0
matplotlib>=3.7.0
seaborn>=0.12.0
jupyter>=1.0.0
jupyterlab>=4.0.0
ipykernel>=6.25.0
plotly>=5.17.0
scipy>=1.11.0
```

Luego instala:

```bash
# Instalar desde requirements.txt
uv pip install -r requirements.txt

# O instalar y sincronizar (más rápido)
uv pip sync requirements.txt
```

### Método 3: Usando pyproject.toml (Moderno)

Crea un archivo `pyproject.toml`:

```toml
[project]
name = "ml-zoomcamp"
version = "0.1.0"
description = "Proyecto del curso de Machine Learning"
requires-python = ">=3.11"

dependencies = [
    "numpy>=1.24.0",
    "pandas>=2.0.0",
    "scikit-learn>=1.3.0",
    "matplotlib>=3.7.0",
    "seaborn>=0.12.0",
    "jupyter>=1.0.0",
    "jupyterlab>=4.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
]
```

Instalar:

```bash
# Instalar dependencias del proyecto
uv pip install -e .

# Instalar con dependencias de desarrollo
uv pip install -e ".[dev]"
```

### Comandos Útiles para Gestión de Paquetes

```bash
# Instalar un paquete específico
uv pip install pandas

# Instalar versión específica
uv pip install pandas==2.0.0

# Actualizar un paquete
uv pip install --upgrade pandas

# Desinstalar un paquete
uv pip uninstall pandas

# Congelar dependencias actuales
uv pip freeze > requirements.txt

# Buscar información de un paquete
uv pip show pandas

# Verificar dependencias
uv pip check
```

---

## 6. Verificación de la Instalación

### Script de Verificación

Crea un archivo `verificar_instalacion.py`:

```python
#!/usr/bin/env python3
"""
Script para verificar que todas las dependencias estén instaladas correctamente
"""

def verificar_importaciones():
    """Verifica que todos los paquetes se puedan importar"""
    paquetes = {
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'sklearn': 'Scikit-learn',
        'matplotlib': 'Matplotlib',
        'seaborn': 'Seaborn',
        'jupyter': 'Jupyter',
    }
    
    print("🔍 Verificando instalación de paquetes...\n")
    
    errores = []
    for modulo, nombre in paquetes.items():
        try:
            __import__(modulo)
            # Obtener versión
            if modulo == 'sklearn':
                import sklearn
                version = sklearn.__version__
            else:
                mod = __import__(modulo)
                version = mod.__version__
            
            print(f"✅ {nombre:15} - v{version}")
        except ImportError as e:
            print(f"❌ {nombre:15} - NO INSTALADO")
            errores.append(nombre)
    
    print("\n" + "="*50)
    if errores:
        print(f"⚠️  Faltan {len(errores)} paquete(s): {', '.join(errores)}")
        print("Ejecuta: uv pip install " + " ".join(errores))
        return False
    else:
        print("🎉 ¡Todas las dependencias están instaladas correctamente!")
        return True

def verificar_python():
    """Verifica la versión de Python"""
    import sys
    print(f"\n🐍 Python {sys.version}")
    
    version_info = sys.version_info
    if version_info.major == 3 and version_info.minor >= 11:
        print("✅ Versión de Python correcta (3.11+)")
        return True
    else:
        print("⚠️  Se recomienda Python 3.11 o superior")
        return False

def test_basico():
    """Ejecuta un test básico de funcionalidad"""
    print("\n🧪 Ejecutando test básico...\n")
    
    try:
        import numpy as np
        import pandas as pd
        from sklearn.linear_model import LinearRegression
        
        # Crear datos de prueba
        X = np.array([[1], [2], [3], [4], [5]])
        y = np.array([2, 4, 6, 8, 10])
        
        # Entrenar modelo simple
        modelo = LinearRegression()
        modelo.fit(X, y)
        prediccion = modelo.predict([[6]])
        
        print(f"📊 Test de regresión lineal:")
        print(f"   Predicción para X=6: {prediccion[0]:.2f}")
        print(f"   Esperado: 12.00")
        
        if abs(prediccion[0] - 12.0) < 0.1:
            print("✅ Test básico exitoso")
            return True
        else:
            print("⚠️  Resultado inesperado")
            return False
            
    except Exception as e:
        print(f"❌ Error en test: {e}")
        return False

if __name__ == "__main__":
    print("="*50)
    print("  VERIFICACIÓN DE ENTORNO ML ZOOMCAMP")
    print("="*50)
    
    python_ok = verificar_python()
    paquetes_ok = verificar_importaciones()
    test_ok = test_basico()
    
    print("\n" + "="*50)
    if python_ok and paquetes_ok and test_ok:
        print("✨ ¡Tu entorno está listo para el curso!")
    else:
        print("⚠️  Revisa los errores anteriores")
    print("="*50)
```

Ejecutar el script:

```bash
# Asegúrate de tener el entorno activado
python verificar_instalacion.py
```

### Verificación Manual Rápida

```bash
# Verificar Python
python --version

# Verificar que estás en el entorno virtual
which python  # macOS/Linux
where python  # Windows

# Probar importaciones
python -c "import numpy, pandas, sklearn; print('✅ Todo OK')"

# Iniciar Jupyter Lab
jupyter lab
```

---

## 📝 Resumen de Comandos Rápidos

### Flujo de Trabajo Diario

```bash
# 1. Navegar al proyecto
cd ~/proyectos/machine-learning-zoomcamp

# 2. Activar entorno
source .venv/bin/activate  # macOS/Linux
.\.venv\Scripts\Activate.ps1  # Windows PowerShell

# 3. Trabajar en tu proyecto
jupyter lab
# o
python mi_script.py

# 4. Instalar nuevos paquetes si es necesario
uv pip install nombre-paquete

# 5. Desactivar cuando termines
deactivate
```

### Crear Nuevo Proyecto

```bash
# 1. Crear carpeta
mkdir mi-proyecto-ml
cd mi-proyecto-ml

# 2. Inicializar Git
git init

# 3. Crear entorno virtual
uv venv --python 3.11

# 4. Activar entorno
source .venv/bin/activate  # macOS/Linux
.\.venv\Scripts\Activate.ps1  # Windows

# 5. Instalar dependencias
uv pip install numpy pandas scikit-learn jupyter

# 6. Crear .gitignore
echo ".venv/" >> .gitignore
echo "*.pyc" >> .gitignore
echo "__pycache__/" >> .gitignore
echo ".ipynb_checkpoints/" >> .gitignore

# 7. Primer commit
git add .
git commit -m "Initial commit: Setup project"
```

---

## 🆘 Solución de Problemas Comunes

### Problema: "uv: command not found"

**Solución:**

```bash
# macOS/Linux
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Windows: Reinicia PowerShell o agrega manualmente al PATH
```

### Problema: Error de permisos en Windows PowerShell

**Solución:**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problema: SSH no funciona con GitHub

**Solución:**

```bash
# Verificar que el ssh-agent esté corriendo
eval "$(ssh-agent -s)"

# Agregar la llave nuevamente
ssh-add ~/.ssh/id_ed25519

# Probar conexión
ssh -T git@github.com
```

### Problema: Python no se encuentra después de instalar uv

**Solución:**

```bash
# Verificar instalación de Python
uv python list

# Instalar Python si no está
uv python install 3.11

# Especificar Python al crear entorno
uv venv --python 3.11
```

---

## 🎯 Próximos Pasos

Una vez que tengas todo configurado:

1. ✅ Clona el repositorio del curso
2. ✅ Crea tu entorno virtual
3. ✅ Instala las dependencias
4. ✅ Ejecuta el script de verificación
5. ✅ Abre Jupyter Lab y comienza con los notebooks

---

**📖 Material base**: Adaptado del [ML Zoomcamp](https://github.com/DataTalksClub/machine-learning-zoomcamp) por Alexey Grigorev y DataTalks.Club

---

[⬅️ Anterior: CRISP-DM](04-crisp-dm.md) | [Volver al índice](README.md)
