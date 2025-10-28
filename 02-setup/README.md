# 🛠️ Setup - Configuración del Entorno de Desarrollo

Esta carpeta contiene guías completas para configurar tu entorno de desarrollo para Machine Learning con Python.

## 📚 Guías disponibles

### 1. [Configuración de GitHub con SSH](./01-github-ssh-setup.md)

Aprende a instalar Git y configurar llaves SSH para trabajar con GitHub de forma segura y sin contraseñas.

**Incluye:**
- ✅ Instalación de Git en macOS y Windows
- ✅ Configuración inicial de Git
- ✅ Generación de llaves SSH
- ✅ Configuración del agente SSH
- ✅ Integración con GitHub
- ✅ Instrucciones para macOS y Windows
- ✅ Solución de problemas comunes

---

### 2. [Configuración de Entorno Virtual con pyenv y uv](./02-python-environment-setup.md)

Aprende a gestionar versiones de Python y crear entornos virtuales con las herramientas modernas más rápidas.

**Incluye:**
- ✅ Instalación de pyenv (gestor de versiones de Python)
- ✅ Instalación de uv (gestor ultra-rápido de paquetes)
- ✅ Uso de pyproject.toml (estándar moderno)
- ✅ Creación y gestión de entornos virtuales
- ✅ Instrucciones para macOS y Windows
- ✅ Mejores prácticas y estructura de proyectos

---

## 🎯 Orden recomendado

Si estás empezando desde cero, te recomendamos seguir este orden:

1. **Primero:** [Configuración de GitHub con SSH](./01-github-ssh-setup.md)
   - Esto te permitirá clonar y subir código a GitHub fácilmente

2. **Segundo:** [Configuración de Entorno Virtual](./02-python-environment-setup.md)
   - Esto te permitirá trabajar con Python de forma profesional

---

## ⚡ Quick Start

### Para instalar Git y configurar GitHub SSH (10-15 minutos)

**macOS:**
```bash
# 1. Instalar Git
brew install git

# 2. Configurar Git
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@ejemplo.com"

# 3. Generar llave SSH
ssh-keygen -t ed25519 -C "tu-email@ejemplo.com"

# 4. Copiar llave pública
pbcopy < ~/.ssh/id_ed25519.pub

# 5. Luego agrégala en GitHub → Settings → SSH and GPG keys
```

**Windows (PowerShell):**
```powershell
# 1. Instalar Git (o descarga desde git-scm.com/download/win)
winget install --id Git.Git -e --source winget

# 2. Reiniciar PowerShell, luego configurar Git
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@ejemplo.com"

# 3. Generar llave SSH
ssh-keygen -t ed25519 -C "tu-email@ejemplo.com"

# 4. Copiar llave pública
Get-Content $HOME\.ssh\id_ed25519.pub | Set-Clipboard

# 5. Luego agrégala en GitHub → Settings → SSH and GPG keys
```

---

### Para configurar Python con pyenv y uv (10-15 minutos)

**macOS:**
```bash
# Instalar pyenv
brew install pyenv

# Configurar shell
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc

# Instalar Python
pyenv install 3.12.0
pyenv global 3.12.0

# Instalar uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc

# Crear primer proyecto
mkdir mi-proyecto
cd mi-proyecto
uv init
```

**Windows (PowerShell como Administrador):**
```powershell
# Instalar pyenv-win
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"

# Reiniciar PowerShell

# Instalar Python
pyenv install 3.12.0
pyenv global 3.12.0

# Instalar uv
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Crear primer proyecto
mkdir mi-proyecto
cd mi-proyecto
uv init
```

---

## 💡 Consejos

- **Lee las guías completas** - Los quick starts son útiles, pero las guías tienen información importante
- **Sigue el orden** - Configura GitHub primero, luego Python
- **Guarda tus llaves SSH** - Son importantes, no las pierdas
- **Usa pyproject.toml** - Es el estándar moderno de Python
- **Aprovecha uv** - Es mucho más rápido que pip tradicional

---

## 🆘 ¿Necesitas ayuda?

Cada guía tiene una sección de **"Problemas comunes"** al final. Si tienes algún error, revisa esa sección primero.

También puedes consultar:
- [Documentación de GitHub SSH](https://docs.github.com/es/authentication/connecting-to-github-with-ssh)
- [Documentación de pyenv](https://github.com/pyenv/pyenv)
- [Documentación de uv](https://github.com/astral-sh/uv)

---

## ✅ Checklist general

### Git y GitHub
- [ ] Instalé Git
- [ ] Configuré mi nombre y email en Git
- [ ] Configuré SSH para GitHub
- [ ] Puedo clonar repositorios con SSH

### Python y entornos virtuales
- [ ] Instalé pyenv
- [ ] Instalé Python con pyenv
- [ ] Instalé uv
- [ ] Creé mi primer entorno virtual
- [ ] Entiendo cómo usar pyproject.toml

---

**¡Buena suerte con tu configuración!** 🚀
