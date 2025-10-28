# 🐍 Configuración de Entorno Virtual con pyenv y uv

## ¿Qué son los entornos virtuales y por qué los necesitas?

Imagina que cada proyecto de Python es como una casa. Cada casa necesita sus propios muebles (librerías) y puede tener diferentes versiones de Python. Los entornos virtuales te permiten mantener cada proyecto aislado, evitando conflictos entre dependencias.

**Beneficios:**
- ✅ Cada proyecto tiene sus propias librerías sin afectar otros proyectos
- ✅ Puedes usar diferentes versiones de Python en diferentes proyectos
- ✅ Facilita compartir tu proyecto con otros desarrolladores
- ✅ Evita el famoso "en mi máquina funciona" 😅

---

## 🛠️ Herramientas que vamos a usar

### pyenv
Administrador de versiones de Python. Te permite instalar y cambiar entre diferentes versiones de Python fácilmente.

### uv
Herramienta moderna y ultra-rápida para gestionar entornos virtuales y dependencias de Python. Es mucho más rápida que pip tradicional.

---

## 🍎 Configuración en macOS

### Paso 1: Instalar Homebrew (si no lo tienes)

Homebrew es un gestor de paquetes para macOS. Abre la Terminal y ejecuta:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Sigue las instrucciones que aparecen en pantalla.

### Paso 2: Instalar pyenv

En la Terminal, ejecuta:

```bash
brew update
brew install pyenv
```

Ahora necesitas configurar tu shell. Ejecuta estos comandos:

```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
```

**💡 Nota:** Si usas bash en lugar de zsh, reemplaza `~/.zshrc` con `~/.bash_profile`

Reinicia tu Terminal o ejecuta:

```bash
source ~/.zshrc
```

Verifica que pyenv se instaló correctamente:

```bash
pyenv --version
```

Deberías ver algo como: `pyenv 2.x.x`

### Paso 3: Instalar Python con pyenv

Primero, instala las dependencias necesarias:

```bash
brew install openssl readline sqlite3 xz zlib tcl-tk
```

Ahora, lista las versiones de Python disponibles:

```bash
pyenv install --list
```

Instala la versión más reciente de Python 3.12 (o la que prefieras):

```bash
pyenv install 3.12.0
```

**💡 Nota:** Este proceso puede tardar varios minutos.

Establece la versión global de Python:

```bash
pyenv global 3.12.0
```

Verifica la instalación:

```bash
python --version
```

### Paso 4: Instalar uv

Ejecuta este comando:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Después de la instalación, agrega `uv` a tu PATH:

```bash
source $HOME/.local/bin/env
```

Para que funcione permanentemente, agrega la ruta al PATH:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

Verifica la instalación:

```bash
uv --version
```

### Paso 5: Crear tu primer entorno virtual

Navega a la carpeta de tu proyecto:

```bash
cd /ruta/a/tu/proyecto
```

Crea un entorno virtual con uv:

```bash
uv venv
```

Esto creará una carpeta `.venv` en tu proyecto.

Activa el entorno virtual:

```bash
source .venv/bin/activate
```

Cuando el entorno esté activo, verás `(.venv)` al inicio de tu línea de comandos.

### Paso 6: Instalar paquetes con uv

Con el entorno activado, instala paquetes usando uv:

```bash
uv add numpy pandas matplotlib
```

**💡 Ventaja:** uv es mucho más rápido que pip tradicional.

Para instalar desde un archivo `requirements.txt`:

```bash
uv pip install -r requirements.txt
```

### Paso 7: Desactivar el entorno virtual

Cuando termines de trabajar:

```bash
deactivate
```

---

## 🪟 Configuración en Windows

### Paso 1: Instalar pyenv-win

**Opción A: Usando PowerShell (Recomendado)**

Abre PowerShell como **Administrador** y ejecuta:

```powershell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```

**Opción B: Usando Git Bash**

```bash
git clone https://github.com/pyenv-win/pyenv-win.git "$HOME/.pyenv"
```

Luego agrega pyenv al PATH manualmente:

1. Presiona `Win + R`, escribe `sysdm.cpl` y presiona Enter
2. Ve a la pestaña **Avanzado** → **Variables de entorno**
3. En **Variables del sistema**, busca `Path` y haz clic en **Editar**
4. Agrega estas tres rutas (reemplaza `TU-USUARIO` con tu nombre de usuario):
   ```
   C:\Users\TU-USUARIO\.pyenv\pyenv-win\bin
   C:\Users\TU-USUARIO\.pyenv\pyenv-win\shims
   ```
5. Haz clic en **Aceptar** en todas las ventanas

Reinicia PowerShell o Git Bash.

Verifica la instalación:

```bash
pyenv --version
```

### Paso 2: Instalar Python con pyenv

Lista las versiones disponibles:

```bash
pyenv install --list
```

Instala la versión más reciente de Python 3.12:

```bash
pyenv install 3.12.0
```

**💡 Nota:** En Windows, este proceso puede tardar varios minutos y descargará Python automáticamente.

Establece la versión global:

```bash
pyenv global 3.12.0
```

Reinicia tu terminal y verifica:

```bash
python --version
```

### Paso 3: Instalar uv

**Opción A: Usando PowerShell**

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Opción B: Usando pip**

```bash
pip install uv
```

Verifica la instalación:

```bash
uv --version
```

### Paso 4: Crear tu primer entorno virtual

Navega a la carpeta de tu proyecto:

```bash
cd C:\ruta\a\tu\proyecto
```

Crea un entorno virtual:

```bash
uv venv
```

Activa el entorno virtual:

**En PowerShell:**
```powershell
.venv\Scripts\Activate.ps1
```

**En Git Bash:**
```bash
source .venv/Scripts/activate
```

**En CMD:**
```cmd
.venv\Scripts\activate.bat
```

Cuando esté activo, verás `(.venv)` al inicio de tu línea de comandos.

### Paso 5: Instalar paquetes con uv

Con el entorno activado:

```bash
uv pip install numpy pandas matplotlib
```

Para instalar desde `requirements.txt`:

```bash
uv pip install -r requirements.txt
```

### Paso 6: Desactivar el entorno virtual

```bash
deactivate
```

---

## 📋 Flujo de trabajo típico

### Crear un nuevo proyecto con pyproject.toml (Recomendado)

```bash
# 1. Crear carpeta del proyecto
mkdir mi-proyecto
cd mi-proyecto

# 2. Inicializar proyecto con uv (crea pyproject.toml automáticamente)
uv init

# 3. Esto crea automáticamente:
# - pyproject.toml (configuración del proyecto)
# - .venv/ (entorno virtual)
# - .python-version (versión de Python)

# 4. Agregar dependencias
uv add numpy pandas scikit-learn matplotlib

# 5. Agregar dependencias de desarrollo (opcional)
uv add --dev pytest black ruff jupyter
```

### Crear proyecto manualmente con pyproject.toml

```bash
# 1. Crear carpeta y archivo de configuración
mkdir mi-proyecto
cd mi-proyecto

# 2. Crear pyproject.toml manualmente
cat > pyproject.toml << 'EOF'
[project]
name = "mi-proyecto"
version = "0.1.0"
description = "Descripción de mi proyecto"
requires-python = ">=3.12"
dependencies = [
    "numpy>=1.24.0",
    "pandas>=2.0.0",
    "scikit-learn>=1.3.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
]
EOF

# 3. Crear entorno virtual
uv venv

# 4. Activar entorno
source .venv/bin/activate  # macOS/Linux
# o
.venv\Scripts\Activate.ps1  # Windows

# 5. Instalar dependencias desde pyproject.toml
uv pip install -e .

# 6. Instalar dependencias de desarrollo
uv pip install -e ".[dev]"
```

### Trabajar en un proyecto existente con pyproject.toml

```bash
# 1. Clonar o navegar al proyecto
cd mi-proyecto

# 2. Sincronizar proyecto (crea .venv e instala todo automáticamente)
uv sync

# O manualmente:
# 2a. Crear entorno virtual
uv venv

# 2b. Activar entorno
source .venv/bin/activate  # macOS/Linux
# o
.venv\Scripts\Activate.ps1  # Windows

# 2c. Instalar dependencias
uv pip install -e .
```

### Flujo tradicional con requirements.txt (Alternativa)

```bash
# 1. Crear carpeta del proyecto
mkdir mi-proyecto
cd mi-proyecto

# 2. Crear entorno virtual
uv venv

# 3. Activar entorno
source .venv/bin/activate  # macOS/Linux
# o
.venv\Scripts\Activate.ps1  # Windows

# 4. Instalar dependencias
uv pip install numpy pandas scikit-learn

# 5. Guardar dependencias
uv pip freeze > requirements.txt

# 6. Instalar desde requirements.txt (en otro momento)
uv pip install -r requirements.txt
```

---

## 🎯 Comandos útiles de pyenv

### Ver versiones instaladas
```bash
pyenv versions
```

### Ver versión actual
```bash
pyenv version
```

### Instalar una versión específica
```bash
pyenv install 3.11.5
```

### Cambiar versión global
```bash
pyenv global 3.12.0
```

### Cambiar versión solo para un proyecto
```bash
cd mi-proyecto
pyenv local 3.11.5
```

Esto crea un archivo `.python-version` en tu proyecto.

### Desinstalar una versión
```bash
pyenv uninstall 3.10.0
```

---

## 🚀 Comandos útiles de uv

### 📝 Nota importante: `uv init` vs `uv venv`

**`uv init` - Inicializa proyecto completo (Recomendado para proyectos nuevos)**

```bash
uv init
```

**Lo que hace:**
- ✅ Crea `pyproject.toml` automáticamente
- ✅ Crea `.venv/` (entorno virtual)
- ✅ Crea `.python-version` (versión de Python)
- ✅ Configura el proyecto listo para usar
- ✅ Permite usar `uv add` directamente

**Cuándo usarlo:** Cuando empiezas un proyecto desde cero.

---

**`uv venv` - Solo crea entorno virtual**

```bash
uv venv
```

**Lo que hace:**
- ✅ Crea **solo** la carpeta `.venv/` (entorno virtual)
- ❌ NO crea `pyproject.toml`
- ❌ NO crea estructura de proyecto

**Cuándo usarlo:** Cuando ya tienes un `pyproject.toml` existente o prefieres crear la configuración manualmente.

---

### Gestión de proyectos (con pyproject.toml)

#### Inicializar un nuevo proyecto
```bash
uv init
```

#### Agregar una dependencia
```bash
uv add nombre-paquete
```

#### Agregar dependencia de desarrollo
```bash
uv add --dev nombre-paquete
```

#### Remover una dependencia
```bash
uv remove nombre-paquete
```

#### Sincronizar proyecto (instalar todas las dependencias)
```bash
uv sync
```

#### Actualizar dependencias
```bash
uv lock --upgrade
```

### Gestión de entornos virtuales

#### Crear entorno virtual
```bash
uv venv
```

#### Crear entorno con versión específica de Python
```bash
uv venv --python 3.11
```

### Gestión de paquetes (estilo pip)

#### Instalar un paquete
```bash
uv pip install nombre-paquete
```

#### Instalar versión específica
```bash
uv pip install numpy==1.24.0
```

#### Instalar desde requirements.txt
```bash
uv pip install -r requirements.txt
```

#### Instalar desde pyproject.toml
```bash
uv pip install -e .
```

#### Instalar con dependencias opcionales
```bash
uv pip install -e ".[dev]"
```

#### Listar paquetes instalados
```bash
uv pip list
```

#### Guardar dependencias
```bash
uv pip freeze > requirements.txt
```

#### Desinstalar un paquete
```bash
uv pip uninstall nombre-paquete
```

#### Actualizar un paquete
```bash
uv pip install --upgrade nombre-paquete
```

### Ejecutar comandos sin activar el entorno

#### Ejecutar script con uv
```bash
uv run python mi_script.py
```

#### Ejecutar comando con uv
```bash
uv run pytest
```

---

## 🔍 Verificar que todo funciona

Crea un archivo de prueba `test.py`:

```python
import sys
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

try:
    import numpy as np
    print(f"NumPy version: {np.__version__}")
    print("✅ NumPy funciona correctamente")
except ImportError:
    print("❌ NumPy no está instalado")
```

Ejecuta:

```bash
python test.py
```

Deberías ver la versión de Python y NumPy (si lo instalaste).

---

## ❓ Problemas comunes

### "pyenv: command not found" (macOS)

**Solución:** Asegúrate de haber agregado pyenv a tu archivo de configuración del shell y reiniciado la terminal.

```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc
```

### "pyenv: command not found" (Windows)

**Solución:** Verifica que las rutas de pyenv estén en las variables de entorno PATH.

### "cannot be loaded because running scripts is disabled" (Windows PowerShell)

**Solución:** Ejecuta PowerShell como Administrador y ejecuta:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### El entorno virtual no se activa

**macOS/Linux:**
```bash
source .venv/bin/activate
```

**Windows PowerShell:**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
.venv\Scripts\activate.bat
```

### "uv: command not found"

**Solución:** Reinicia tu terminal después de instalar uv, o ejecuta:

**macOS/Linux:**
```bash
source $HOME/.local/bin/env
```

Para hacerlo permanente en macOS:
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Windows:** Reinicia PowerShell o agrega `%USERPROFILE%\.cargo\bin` al PATH.

### Error al instalar Python con pyenv en macOS

**Solución:** Instala las dependencias necesarias:

```bash
brew install openssl readline sqlite3 xz zlib tcl-tk
```

---

## 📁 Estructura recomendada de proyecto

### Con pyproject.toml (Recomendado)

```
mi-proyecto/
├── .venv/                 # Entorno virtual (no subir a Git)
├── .python-version        # Versión de Python del proyecto
├── pyproject.toml        # Configuración del proyecto y dependencias
├── uv.lock               # Lock file de dependencias (generado por uv)
├── .gitignore            # Ignorar .venv y otros archivos
├── README.md             # Documentación
├── src/                  # Código fuente
│   ├── __init__.py
│   └── main.py
├── tests/                # Pruebas
│   ├── __init__.py
│   └── test_main.py
├── notebooks/            # Jupyter notebooks (opcional)
│   └── exploracion.ipynb
└── data/                 # Datos (si aplica)
    ├── raw/
    └── processed/
```

### Ejemplo de pyproject.toml

```toml
[project]
name = "mi-proyecto"
version = "0.1.0"
description = "Proyecto de Machine Learning"
readme = "README.md"
requires-python = ">=3.12"
authors = [
    { name = "Tu Nombre", email = "tu@email.com" }
]

dependencies = [
    "numpy>=1.24.0",
    "pandas>=2.0.0",
    "scikit-learn>=1.3.0",
    "matplotlib>=3.7.0",
    "seaborn>=0.12.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "ipython>=8.0.0",
]
jupyter = [
    "jupyter>=1.0.0",
    "ipykernel>=6.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.black]
line-length = 88
target-version = ['py312']

[tool.ruff]
line-length = 88
target-version = "py312"
```

### Estructura tradicional con requirements.txt

```
mi-proyecto/
├── .venv/                 # Entorno virtual (no subir a Git)
├── .python-version        # Versión de Python del proyecto
├── .gitignore            # Ignorar .venv y otros archivos
├── requirements.txt      # Dependencias del proyecto
├── requirements-dev.txt  # Dependencias de desarrollo
├── README.md            # Documentación
├── src/                 # Código fuente
│   └── main.py
├── tests/               # Pruebas
│   └── test_main.py
└── data/                # Datos (si aplica)
```

### Ejemplo de .gitignore

```gitignore
# Entornos virtuales
.venv/
venv/
env/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
*.egg-info/
dist/
build/

# Jupyter Notebook
.ipynb_checkpoints
*.ipynb_checkpoints/

# uv
uv.lock

# Datos
data/
*.csv
*.xlsx
*.db
*.sqlite

# IDE
.vscode/
.idea/
*.swp
*.swo

# Sistema
.DS_Store
Thumbs.db
```

---

## 🎓 Mejores prácticas

1. **Siempre usa entornos virtuales** - Nunca instales paquetes globalmente
2. **Un entorno por proyecto** - Cada proyecto debe tener su propio entorno
3. **Usa pyproject.toml** - Es el estándar moderno de Python (compatible con Poetry, uv, pip, etc.)
4. **Documenta tus dependencias** - Usa `pyproject.toml` o `requirements.txt`
5. **No subas .venv a Git** - Agrégalo a `.gitignore`
6. **Usa versiones específicas** - Especifica rangos de versiones compatibles (ej: `numpy>=1.24.0,<2.0.0`)
7. **Separa dependencias** - Usa `[project.optional-dependencies]` para dev, test, etc.
8. **Actualiza regularmente** - Mantén tus dependencias actualizadas con `uv lock --upgrade`
9. **Usa .python-version** - Define la versión de Python con pyenv para consistencia
10. **Aprovecha uv** - Es mucho más rápido que pip tradicional

---

## 📚 Recursos adicionales

- [Documentación oficial de pyenv](https://github.com/pyenv/pyenv)
- [Documentación oficial de uv](https://github.com/astral-sh/uv)
- [pyproject.toml specification (PEP 621)](https://peps.python.org/pep-0621/)
- [Python Packaging User Guide](https://packaging.python.org/)
- [Python Virtual Environments: A Primer](https://realpython.com/python-virtual-environments-a-primer/)
- [pyenv-win GitHub](https://github.com/pyenv-win/pyenv-win)

---

## ✅ Checklist

### Configuración inicial
- [ ] Instalé pyenv
- [ ] Instalé una versión de Python con pyenv
- [ ] Configuré la versión global de Python
- [ ] Instalé uv y lo agregué al PATH

### Primer proyecto
- [ ] Creé mi primer proyecto con `uv init` o manualmente
- [ ] Creé el archivo `pyproject.toml`
- [ ] Agregué dependencias con `uv add` o manualmente
- [ ] Instalé las dependencias con `uv sync` o `uv pip install -e .`
- [ ] Creé el archivo `.gitignore` con `.venv/` incluido

### Verificación
- [ ] Puedo activar y desactivar el entorno virtual
- [ ] Puedo instalar paquetes con uv
- [ ] Mi proyecto tiene estructura organizada (src/, tests/, etc.)
- [ ] Entiendo la diferencia entre dependencias normales y de desarrollo

---

## 🎉 ¡Felicidades!

Ya tienes todo configurado para trabajar con Python de forma profesional y moderna. Ahora puedes:

- ✅ Gestionar múltiples versiones de Python con pyenv
- ✅ Crear entornos virtuales aislados para cada proyecto
- ✅ Usar pyproject.toml como estándar moderno de configuración
- ✅ Instalar dependencias ultra-rápido con uv
- ✅ Compartir tu proyecto fácilmente con otros desarrolladores
- ✅ Mantener tus proyectos organizados y reproducibles

**Próximos pasos:**
1. Crea tu primer proyecto con `uv init`
2. Agrega las librerías que necesites con `uv add`
3. Organiza tu código en `src/`
4. Escribe tests en `tests/`
5. Empieza a programar 🚀

**Flujo recomendado para nuevos proyectos:**
```bash
# Crear proyecto
mkdir mi-proyecto-ml
cd mi-proyecto-ml

# Inicializar con uv (crea pyproject.toml y .venv automáticamente)
uv init

# Agregar dependencias de ML
uv add numpy pandas scikit-learn matplotlib seaborn

# Agregar herramientas de desarrollo
uv add --dev pytest black ruff jupyter

# ¡Listo para programar!
```

---

**¿Dudas?** Revisa la sección de problemas comunes o consulta la documentación oficial de las herramientas.
