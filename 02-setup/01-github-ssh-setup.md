# 🔐 Configuración de GitHub con Llaves SSH

## ¿Qué es SSH y por qué lo necesitas?

SSH (Secure Shell) es como una llave digital que te permite conectarte de forma segura con GitHub sin tener que escribir tu usuario y contraseña cada vez que subes o descargas código.

**Beneficios:**
- ✅ No necesitas escribir tu contraseña en cada operación
- ✅ Es más seguro que usar contraseñas
- ✅ GitHub lo recomienda como método principal

---

## 📋 Requisitos previos

- Tener una cuenta en [GitHub](https://github.com)
- Tener Git instalado en tu computadora

---

## 💻 Instalación de Git

### macOS

**Opción 1: Usando Homebrew (Recomendado)**

Si ya tienes Homebrew instalado:

```bash
brew install git
```

Si no tienes Homebrew, instálalo primero:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Luego instala Git:

```bash
brew install git
```

**Opción 2: Usando el instalador oficial**

1. Descarga Git desde [git-scm.com/download/mac](https://git-scm.com/download/mac)
2. Abre el archivo `.dmg` descargado
3. Sigue las instrucciones del instalador

**Verificar la instalación:**

```bash
git --version
```

Deberías ver algo como: `git version 2.x.x`

**Configurar Git (primera vez):**

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@ejemplo.com"
```

### Windows

**Opción 1: Usando el instalador oficial (Recomendado)**

1. Descarga Git desde [git-scm.com/download/win](https://git-scm.com/download/win)
2. Ejecuta el instalador descargado
3. Durante la instalación, usa estas configuraciones recomendadas:
   - ✅ **Editor:** Selecciona tu editor preferido (VS Code, Notepad++, etc.)
   - ✅ **PATH environment:** "Git from the command line and also from 3rd-party software"
   - ✅ **SSH executable:** "Use bundled OpenSSH"
   - ✅ **HTTPS transport backend:** "Use the OpenSSL library"
   - ✅ **Line ending conversions:** "Checkout Windows-style, commit Unix-style"
   - ✅ **Terminal emulator:** "Use MinTTY"
   - ✅ **Default behavior of git pull:** "Default (fast-forward or merge)"
   - ✅ Marca: "Enable file system caching" y "Enable Git Credential Manager"

4. Haz clic en "Install"

**Opción 2: Usando winget (Windows 10/11)**

Abre PowerShell y ejecuta:

```powershell
winget install --id Git.Git -e --source winget
```

**Opción 3: Usando Chocolatey**

Si tienes Chocolatey instalado:

```powershell
choco install git
```

**Verificar la instalación:**

Abre PowerShell o Git Bash y ejecuta:

```bash
git --version
```

Deberías ver algo como: `git version 2.x.x`

**Configurar Git (primera vez):**

Abre Git Bash o PowerShell:

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@ejemplo.com"
```

**Configuración adicional para Windows:**

```bash
# Configurar el manejo de finales de línea
git config --global core.autocrlf true

# Configurar el editor (opcional, ejemplo con VS Code)
git config --global core.editor "code --wait"
```

---

## 🍎 Configuración de SSH en macOS

### Paso 1: Verificar si ya tienes llaves SSH

Abre la Terminal y ejecuta:

```bash
ls -la ~/.ssh
```

**¿Qué buscar?**
- Si ves archivos como `id_rsa.pub`, `id_ed25519.pub` o `id_ecdsa.pub`, ya tienes llaves SSH
- Si ves un error como "No such file or directory", necesitas crear nuevas llaves

### Paso 2: Generar una nueva llave SSH

En la Terminal, ejecuta este comando (reemplaza el email con tu email de GitHub):

```bash
ssh-keygen -t ed25519 -C "tu-email@ejemplo.com"
```

**💡 Nota:** Si tu sistema es muy antiguo y no soporta ed25519, usa:
```bash
ssh-keygen -t rsa -b 4096 -C "tu-email@ejemplo.com"
```

**Durante el proceso:**

1. Te preguntará dónde guardar la llave:
   ```
   Enter file in which to save the key (/Users/tu-usuario/.ssh/id_ed25519):
   ```
   Presiona `Enter` para usar la ubicación por defecto.

2. Te pedirá una contraseña (passphrase):
   ```
   Enter passphrase (empty for no passphrase):
   ```
   Puedes dejarla vacía (solo presiona `Enter`) o escribir una contraseña adicional para más seguridad.

### Paso 3: Agregar la llave al agente SSH

Primero, inicia el agente SSH:

```bash
eval "$(ssh-agent -s)"
```

Deberías ver algo como: `Agent pid 12345`

Ahora, verifica si existe el archivo de configuración:

```bash
touch ~/.ssh/config
```

Abre el archivo de configuración:

```bash
open -e ~/.ssh/config
```

Agrega estas líneas al archivo:

```
Host github.com
  AddKeysToAgent yes
  UseKeychain yes
  IdentityFile ~/.ssh/id_ed25519
```

**💡 Nota:** Si usaste RSA en lugar de ed25519, cambia `id_ed25519` por `id_rsa`

Guarda y cierra el archivo.

Ahora agrega tu llave SSH al agente:

```bash
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

### Paso 4: Copiar la llave pública

Ejecuta este comando para copiar tu llave pública al portapapeles:

```bash
pbcopy < ~/.ssh/id_ed25519.pub
```

**💡 Alternativa:** Si el comando anterior no funciona, puedes ver la llave con:
```bash
cat ~/.ssh/id_ed25519.pub
```
Y copiarla manualmente (selecciona todo el texto que aparece).

### Paso 5: Agregar la llave a GitHub

1. Ve a [GitHub](https://github.com) e inicia sesión
2. Haz clic en tu foto de perfil (esquina superior derecha) → **Settings**
3. En el menú lateral izquierdo, haz clic en **SSH and GPG keys**
4. Haz clic en el botón verde **New SSH key**
5. En "Title", escribe un nombre descriptivo (ej: "MacBook Pro Personal")
6. En "Key", pega la llave que copiaste (Cmd + V)
7. Haz clic en **Add SSH key**
8. Si te pide tu contraseña de GitHub, ingrésala

### Paso 6: Verificar la conexión

En la Terminal, ejecuta:

```bash
ssh -T git@github.com
```

La primera vez te preguntará:
```
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```
Escribe `yes` y presiona Enter.

Si todo salió bien, verás un mensaje como:
```
Hi tu-usuario! You've successfully authenticated, but GitHub does not provide shell access.
```

¡Felicidades! 🎉 Ya tienes SSH configurado en macOS.

---

## 🪟 Configuración de SSH en Windows

### Paso 1: Verificar si ya tienes llaves SSH

Abre **PowerShell** o **Git Bash** y ejecuta:

```bash
ls -la ~/.ssh
```

**En PowerShell también puedes usar:**
```powershell
dir $HOME\.ssh
```

**¿Qué buscar?**
- Si ves archivos como `id_rsa.pub`, `id_ed25519.pub` o `id_ecdsa.pub`, ya tienes llaves SSH
- Si ves un error, necesitas crear nuevas llaves

### Paso 2: Generar una nueva llave SSH

**Opción A: Usando Git Bash (Recomendado)**

Abre Git Bash y ejecuta (reemplaza el email con tu email de GitHub):

```bash
ssh-keygen -t ed25519 -C "tu-email@ejemplo.com"
```

**Opción B: Usando PowerShell**

```powershell
ssh-keygen -t ed25519 -C "tu-email@ejemplo.com"
```

**💡 Nota:** Si tu sistema no soporta ed25519, usa:
```bash
ssh-keygen -t rsa -b 4096 -C "tu-email@ejemplo.com"
```

**Durante el proceso:**

1. Te preguntará dónde guardar la llave:
   ```
   Enter file in which to save the key (C:\Users\tu-usuario\.ssh\id_ed25519):
   ```
   Presiona `Enter` para usar la ubicación por defecto.

2. Te pedirá una contraseña (passphrase):
   ```
   Enter passphrase (empty for no passphrase):
   ```
   Puedes dejarla vacía (solo presiona `Enter`) o escribir una contraseña adicional.

### Paso 3: Agregar la llave al agente SSH

**Opción A: Usando Git Bash**

Inicia el agente SSH:

```bash
eval "$(ssh-agent -s)"
```

Agrega tu llave:

```bash
ssh-add ~/.ssh/id_ed25519
```

**Opción B: Usando PowerShell (como Administrador)**

Primero, verifica que el servicio ssh-agent esté corriendo:

```powershell
Get-Service ssh-agent | Set-Service -StartupType Automatic
Start-Service ssh-agent
```

Luego agrega tu llave:

```powershell
ssh-add $HOME\.ssh\id_ed25519
```

### Paso 4: Copiar la llave pública

**Opción A: Usando Git Bash**

```bash
cat ~/.ssh/id_ed25519.pub | clip
```

**Opción B: Usando PowerShell**

```powershell
Get-Content $HOME\.ssh\id_ed25519.pub | Set-Clipboard
```

**💡 Alternativa manual:**
1. Abre el archivo con el Bloc de notas:
   ```powershell
   notepad $HOME\.ssh\id_ed25519.pub
   ```
2. Selecciona todo el contenido (Ctrl + A)
3. Cópialo (Ctrl + C)

### Paso 5: Agregar la llave a GitHub

1. Ve a [GitHub](https://github.com) e inicia sesión
2. Haz clic en tu foto de perfil (esquina superior derecha) → **Settings**
3. En el menú lateral izquierdo, haz clic en **SSH and GPG keys**
4. Haz clic en el botón verde **New SSH key**
5. En "Title", escribe un nombre descriptivo (ej: "PC Windows Casa")
6. En "Key", pega la llave que copiaste (Ctrl + V)
7. Haz clic en **Add SSH key**
8. Si te pide tu contraseña de GitHub, ingrésala

### Paso 6: Verificar la conexión

En Git Bash o PowerShell, ejecuta:

```bash
ssh -T git@github.com
```

La primera vez te preguntará:
```
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```
Escribe `yes` y presiona Enter.

Si todo salió bien, verás un mensaje como:
```
Hi tu-usuario! You've successfully authenticated, but GitHub does not provide shell access.
```

¡Felicidades! 🎉 Ya tienes SSH configurado en Windows.

---

## 🔧 Uso de SSH con Git

### Clonar un repositorio usando SSH

En lugar de usar HTTPS:
```bash
git clone https://github.com/usuario/repositorio.git
```

Usa SSH:
```bash
git clone git@github.com:usuario/repositorio.git
```

### Cambiar un repositorio existente de HTTPS a SSH

Si ya clonaste un repositorio con HTTPS, puedes cambiar la URL remota:

```bash
git remote set-url origin git@github.com:usuario/repositorio.git
```

Verifica que el cambio se hizo correctamente:

```bash
git remote -v
```

---

## ❓ Problemas comunes

### "Permission denied (publickey)"

**Solución:**
1. Verifica que agregaste la llave correcta a GitHub
2. Asegúrate de que el agente SSH esté corriendo
3. Verifica que la llave esté agregada al agente: `ssh-add -l`

### "Could not open a connection to your authentication agent"

**macOS:**
```bash
eval "$(ssh-agent -s)"
```

**Windows (PowerShell como Administrador):**
```powershell
Start-Service ssh-agent
```

### La llave no se guarda después de reiniciar

**macOS:** Asegúrate de haber configurado el archivo `~/.ssh/config` correctamente (Paso 3).

**Windows:** Asegúrate de que el servicio ssh-agent esté configurado para iniciar automáticamente.

---

## 📚 Recursos adicionales

- [Documentación oficial de GitHub sobre SSH](https://docs.github.com/es/authentication/connecting-to-github-with-ssh)
- [Solución de problemas de SSH](https://docs.github.com/es/authentication/troubleshooting-ssh)

---

## ✅ Checklist

### Instalación de Git
- [ ] Instalé Git en mi sistema
- [ ] Verifiqué la instalación con `git --version`
- [ ] Configuré mi nombre con `git config --global user.name`
- [ ] Configuré mi email con `git config --global user.email`

### Configuración de SSH
- [ ] Generé mi llave SSH
- [ ] Agregué la llave al agente SSH
- [ ] Copié la llave pública
- [ ] Agregué la llave a mi cuenta de GitHub
- [ ] Verifiqué la conexión con `ssh -T git@github.com`
- [ ] Puedo clonar repositorios usando SSH

---

**¡Listo!** Ahora puedes trabajar con GitHub de forma segura y sin tener que escribir tu contraseña cada vez. 🚀
