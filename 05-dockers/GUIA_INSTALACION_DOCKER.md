# 🐳 Guía de Instalación de Docker

Esta guía te ayudará a instalar Docker Desktop en macOS y Windows paso a paso.

---

## 📋 Tabla de Contenidos

- [Instalación en macOS](#instalación-en-macos)
- [Instalación en Windows](#instalación-en-windows)
- [Verificación de la Instalación](#verificación-de-la-instalación)
- [Solución de Problemas](#solución-de-problemas)

---

## 🍎 Instalación en macOS

### Requisitos del Sistema

- macOS 11 (Big Sur) o superior
- Procesador Intel o Apple Silicon (M1/M2/M3)
- Mínimo 4 GB de RAM

### Opción 1: Instalación con Homebrew (Recomendado)

#### Paso 1: Verificar si tienes Homebrew instalado

Abre la Terminal y ejecuta:

```bash
brew --version
```

Si no tienes Homebrew, instálalo primero:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Paso 2: Instalar Docker Desktop

```bash
brew install --cask docker
```

Espera a que termine la descarga e instalación. Te pedirá tu contraseña de administrador.

#### Paso 3: Abrir Docker Desktop

```bash
open -a Docker
```

O búscalo en Spotlight (Cmd + Espacio) y escribe "Docker".

#### Paso 4: Configuración inicial

1. **Acepta los términos de servicio** cuando se abra Docker Desktop
2. **Ingresa tu contraseña** si te la solicita
3. **Espera** a que el ícono de Docker (una ballena) aparezca en la barra de menú superior
4. El ícono dejará de estar animado cuando Docker esté listo

### Opción 2: Instalación Manual

#### Paso 1: Descargar Docker Desktop

1. Ve a [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. Haz clic en **"Download for Mac"**
3. Selecciona tu chip:
   - **Apple Silicon** (M1/M2/M3)
   - **Intel Chip**

#### Paso 2: Instalar

1. Abre el archivo `.dmg` descargado
2. Arrastra **Docker.app** a la carpeta **Applications**
3. Abre **Docker** desde Applications o Launchpad

#### Paso 3: Configuración inicial

Igual que en la Opción 1, paso 4.

---

## 🪟 Instalación en Windows

### Requisitos del Sistema

- Windows 10 64-bit: Pro, Enterprise, o Education (Build 19041 o superior)
- Windows 11 64-bit
- Habilitar la característica WSL 2 (Windows Subsystem for Linux)
- Procesador con soporte de virtualización
- Mínimo 4 GB de RAM

### Paso 1: Habilitar WSL 2

#### Opción A: Instalación Automática (Windows 11 o Windows 10 actualizado)

Abre **PowerShell como Administrador** y ejecuta:

```powershell
wsl --install
```

Reinicia tu computadora cuando se complete.

#### Opción B: Instalación Manual

1. Abre **PowerShell como Administrador** y ejecuta:

```powershell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
```

2. Habilita la característica de Máquina Virtual:

```powershell
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

3. **Reinicia tu computadora**

4. Descarga e instala el paquete de actualización del kernel de Linux:
   - Ve a: [https://aka.ms/wsl2kernel](https://aka.ms/wsl2kernel)
   - Descarga e instala el paquete MSI

5. Establece WSL 2 como versión predeterminada:

```powershell
wsl --set-default-version 2
```

### Paso 2: Descargar Docker Desktop

1. Ve a [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. Haz clic en **"Download for Windows"**
3. Descarga el instalador **Docker Desktop Installer.exe**

### Paso 3: Instalar Docker Desktop

1. Ejecuta **Docker Desktop Installer.exe**
2. Asegúrate de que la opción **"Use WSL 2 instead of Hyper-V"** esté marcada
3. Sigue el asistente de instalación
4. Haz clic en **"Close and restart"** cuando termine

### Paso 4: Configuración inicial

1. Después del reinicio, abre **Docker Desktop** desde el menú Inicio
2. **Acepta los términos de servicio**
3. Puedes crear una cuenta de Docker Hub o continuar sin iniciar sesión
4. Espera a que Docker Desktop se inicie completamente
5. Verás el ícono de Docker (ballena) en la bandeja del sistema

### Paso 5: Verificar WSL 2

Abre **PowerShell** y ejecuta:

```powershell
wsl --list --verbose
```

Deberías ver algo como:

```
  NAME                   STATE           VERSION
* docker-desktop         Running         2
  docker-desktop-data    Running         2
```

---

## ✅ Verificación de la Instalación

### Paso 1: Verificar la versión de Docker

Abre una terminal (Terminal en Mac, PowerShell o CMD en Windows) y ejecuta:

```bash
docker --version
```

**Salida esperada:**

```
Docker version 28.5.1, build e180ab8
```

(La versión puede variar)

### Paso 2: Verificar Docker Compose

```bash
docker compose version
```

**Salida esperada:**

```
Docker Compose version v2.40.3-desktop.1
```

### Paso 3: Ejecutar Hello World

Este es el comando más importante para verificar que todo funciona:

```bash
docker run hello-world
```

**Salida esperada:**

```
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
198f93fd5094: Pull complete
Digest: sha256:56433a6be3fda188089fb548eae3d91df3ed0d6589f7c2656121b911198df065
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (arm64v8)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

### Paso 4: Verificar que Docker está corriendo

**En macOS:**

```bash
docker ps
```

**En Windows (PowerShell):**

```powershell
docker ps
```

**Salida esperada:**

```
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

(La lista puede estar vacía, eso es normal)

### Paso 5: Prueba adicional - Ejecutar Nginx

```bash
docker run -d -p 8080:80 --name test-nginx nginx
```

Luego abre tu navegador y ve a:

```
http://localhost:8080
```

Deberías ver la página de bienvenida de Nginx.

**Limpiar después de la prueba:**

```bash
docker stop test-nginx
docker rm test-nginx
```

---

## 🔧 Solución de Problemas

### macOS

#### Problema: "command not found: docker"

**Solución:**

1. Asegúrate de que Docker Desktop esté corriendo (ícono de ballena en la barra de menú)
2. Si no está corriendo, ábrelo:

```bash
open -a Docker
```

3. Espera unos segundos y vuelve a intentar

#### Problema: "Cannot connect to the Docker daemon"

**Solución:**

1. Reinicia Docker Desktop:
   - Haz clic en el ícono de Docker en la barra de menú
   - Selecciona "Restart"

2. Si persiste, reinicia tu Mac

#### Problema: Docker Desktop no abre

**Solución:**

1. Verifica los requisitos del sistema
2. Reinstala Docker Desktop:

```bash
brew uninstall --cask docker
brew install --cask docker
```

### Windows

#### Problema: "WSL 2 installation is incomplete"

**Solución:**

1. Asegúrate de haber instalado el paquete de actualización del kernel:
   - [https://aka.ms/wsl2kernel](https://aka.ms/wsl2kernel)

2. Ejecuta en PowerShell como Administrador:

```powershell
wsl --update
```

#### Problema: "Hardware assisted virtualization and data execution protection must be enabled in the BIOS"

**Solución:**

1. Reinicia tu PC y entra al BIOS/UEFI (generalmente presionando F2, F10, F12, o Del durante el arranque)
2. Busca la opción de **Virtualization Technology** (VT-x, AMD-V, SVM)
3. **Habilítala**
4. Guarda y reinicia

#### Problema: "Docker Desktop requires a newer WSL kernel version"

**Solución:**

```powershell
wsl --update
wsl --shutdown
```

Luego reinicia Docker Desktop.

#### Problema: "An error occurred while starting Docker"

**Solución:**

1. Abre PowerShell como Administrador:

```powershell
wsl --shutdown
```

2. Reinicia Docker Desktop

3. Si persiste, reinicia Windows

#### Problema: Docker es muy lento en Windows

**Solución:**

1. Asegúrate de estar usando WSL 2 (no Hyper-V)
2. Aumenta los recursos asignados:
   - Abre Docker Desktop
   - Ve a Settings → Resources
   - Aumenta CPU y memoria

---

## 🎯 Comandos de Verificación Rápida

Copia y pega estos comandos para verificar todo de una vez:

```bash
# Verificar versiones
docker --version
docker compose version

# Ejecutar Hello World
docker run hello-world

# Ver contenedores
docker ps -a

# Ver imágenes
docker images

# Limpiar
docker system prune -a
```

---

## 📚 Recursos Adicionales

- **Documentación oficial:** [https://docs.docker.com/](https://docs.docker.com/)
- **Docker Hub:** [https://hub.docker.com/](https://hub.docker.com/)
- **Tutoriales interactivos:** [https://www.docker.com/play-with-docker](https://www.docker.com/play-with-docker)
- **Comunidad:** [https://forums.docker.com/](https://forums.docker.com/)

---

## ✨ Próximos Pasos

Una vez que Docker esté instalado y verificado:

1. **Aprende los comandos básicos** de Docker
2. **Crea tu primer Dockerfile**
3. **Usa Docker Compose** para aplicaciones multi-contenedor
4. **Explora Docker Hub** para encontrar imágenes útiles

---

## 🆘 ¿Necesitas Ayuda?

Si tienes problemas que no están cubiertos en esta guía:

1. Revisa los logs de Docker Desktop (Settings → Troubleshoot → View logs)
2. Busca en [Stack Overflow](https://stackoverflow.com/questions/tagged/docker)
3. Consulta los [foros oficiales de Docker](https://forums.docker.com/)

---

**¡Felicidades! 🎉 Ahora tienes Docker instalado y funcionando.**
