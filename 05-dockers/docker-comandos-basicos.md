# Comandos Básicos de Docker

## 🐳 Conceptos Básicos

- **Imagen**: Plantilla de solo lectura para crear contenedores (como una "clase")
- **Contenedor**: Instancia ejecutable de una imagen (como un "objeto")
- **Docker Hub**: Repositorio público de imágenes Docker

---

## 📦 Comandos de Imágenes

### Ver imágenes descargadas
```bash
docker images
# o
docker image ls
```

### Descargar una imagen
```bash
docker pull ubuntu
docker pull python:3.11
docker pull nginx
```

### Eliminar una imagen
```bash
docker rmi hello-world
docker rmi <image-id>
```

### Buscar imágenes en Docker Hub
```bash
docker search python
```

---

## 🚀 Comandos de Contenedores

### Ejecutar un contenedor
```bash
# Ejecutar y salir automáticamente
docker run hello-world

# Ejecutar en modo interactivo (-it)
docker run -it ubuntu bash

# Ejecutar en segundo plano (-d detached)
docker run -d nginx

# Ejecutar con nombre personalizado
docker run --name mi-contenedor -d nginx

# Ejecutar con puerto mapeado
docker run -d -p 8080:80 nginx
# Acceder en: http://localhost:8080
```

### Ver contenedores

```bash
# Ver contenedores en ejecución
docker ps

# Ver todos los contenedores (incluyendo detenidos)
docker ps -a

# Ver solo los IDs
docker ps -q
```

### Detener y eliminar contenedores

```bash
# Detener un contenedor
docker stop <container-id o nombre>

# Iniciar un contenedor detenido
docker start <container-id o nombre>

# Reiniciar un contenedor
docker restart <container-id o nombre>

# Eliminar un contenedor detenido
docker rm <container-id o nombre>

# Forzar eliminación de un contenedor en ejecución
docker rm -f <container-id o nombre>
```

### Limpiar contenedores detenidos
```bash
# Eliminar todos los contenedores detenidos
docker container prune

# Eliminar todo (contenedores, redes, imágenes no usadas)
docker system prune
```

---

## 🔍 Inspeccionar Contenedores

### Ver logs de un contenedor
```bash
docker logs <container-id>
docker logs -f <container-id>  # Seguir logs en tiempo real
```

### Ver procesos dentro de un contenedor
```bash
docker top <container-id>
```

### Ver detalles de un contenedor
```bash
docker inspect <container-id>
```

### Ver estadísticas de uso (CPU, memoria, etc.)
```bash
docker stats
docker stats <container-id>
```

---

## 💻 Interactuar con Contenedores

### Ejecutar comandos en un contenedor en ejecución
```bash
# Ejecutar un comando
docker exec <container-id> ls -la

# Abrir una terminal interactiva
docker exec -it <container-id> bash
# o si no tiene bash:
docker exec -it <container-id> sh
```

### Copiar archivos entre host y contenedor
```bash
# Del host al contenedor
docker cp archivo.txt <container-id>:/ruta/destino/

# Del contenedor al host
docker cp <container-id>:/ruta/archivo.txt ./
```

---

## 🛠️ Ejemplos Prácticos

### Ejemplo 1: Servidor web Nginx
```bash
# 1. Ejecutar nginx en puerto 8080
docker run -d -p 8080:80 --name mi-nginx nginx

# 2. Ver que está corriendo
docker ps

# 3. Abrir en navegador: http://localhost:8080

# 4. Ver logs
docker logs mi-nginx

# 5. Detener y eliminar
docker stop mi-nginx
docker rm mi-nginx
```

### Ejemplo 2: Python interactivo
```bash
# 1. Ejecutar Python 3.11
docker run -it python:3.11 python

# 2. Probar código Python
>>> print("Hola desde Docker!")
>>> exit()
```

### Ejemplo 3: Ubuntu con bash
```bash
# 1. Ejecutar Ubuntu
docker run -it --name mi-ubuntu ubuntu bash

# 2. Dentro del contenedor:
root@xxx:/# apt update
root@xxx:/# apt install -y curl
root@xxx:/# curl --version
root@xxx:/# exit

# 3. Volver a entrar al mismo contenedor
docker start mi-ubuntu
docker exec -it mi-ubuntu bash

# 4. Limpiar
docker stop mi-ubuntu
docker rm mi-ubuntu
```

### Ejemplo 4: Contenedor con volumen (persistencia)
```bash
# Crear un volumen para persistir datos
docker run -it -v $(pwd)/datos:/app ubuntu bash

# Dentro del contenedor:
root@xxx:/# cd /app
root@xxx:/app# echo "Hola" > archivo.txt
root@xxx:/app# exit

# El archivo estará en tu carpeta local ./datos/
```

---

## 🔧 Comandos de Limpieza

```bash
# Eliminar contenedores detenidos
docker container prune

# Eliminar imágenes sin usar
docker image prune

# Eliminar volúmenes sin usar
docker volume prune

# Eliminar redes sin usar
docker network prune

# Limpiar todo (¡cuidado!)
docker system prune -a
```

---

## 📝 Flags Importantes

- `-d` : Detached (segundo plano)
- `-it` : Interactive + TTY (terminal interactiva)
- `-p` : Port mapping (mapear puertos)
- `-v` : Volume (montar volúmenes)
- `--name` : Nombre personalizado
- `--rm` : Eliminar automáticamente al salir
- `-e` : Variables de entorno

### Ejemplo combinando flags:
```bash
docker run -d \
  --name mi-app \
  -p 3000:3000 \
  -v $(pwd):/app \
  -e NODE_ENV=production \
  node:18
```

---

## 🎯 Ejercicios Prácticos

### Ejercicio 1: Explorar Ubuntu
```bash
docker run -it ubuntu bash
# Dentro: apt update && apt install -y neofetch && neofetch
```

### Ejercicio 2: Servidor Python simple
```bash
# Crear archivo index.html
echo "<h1>Hola Docker!</h1>" > index.html

# Ejecutar servidor Python
docker run -d -p 8000:8000 -v $(pwd):/app -w /app python:3.11 \
  python -m http.server 8000

# Abrir: http://localhost:8000
```

### Ejercicio 3: Base de datos PostgreSQL
```bash
docker run -d \
  --name postgres-db \
  -e POSTGRES_PASSWORD=mipassword \
  -p 5432:5432 \
  postgres:15

# Conectar desde otro contenedor
docker exec -it postgres-db psql -U postgres
```

---

## 📚 Recursos Adicionales

- [Documentación oficial](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Docker Cheat Sheet](https://docs.docker.com/get-started/docker_cheatsheet.pdf)

---

## ⚡ Tips Rápidos

1. **Usa nombres descriptivos** para tus contenedores con `--name`
2. **Siempre limpia** contenedores e imágenes que no uses
3. **Usa `--rm`** para contenedores temporales que se eliminan al salir
4. **Mapea puertos** con `-p` para acceder desde tu navegador
5. **Usa volúmenes** con `-v` para persistir datos

```bash
# Ejemplo de contenedor temporal
docker run --rm -it python:3.11 python
```
