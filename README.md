<h3><ins>Aprendizaje autónomo en ingeniería mediante actividades gamificadas en Telegram</ins></h3>
<div>
  
  <!-- Título centrado -->
  <h4>👨‍🎓 Desarrollado por Pedro Rodríguez Jiménez</h4>
  
  <!-- Badge de LinkedIn centrado -->
  <a href="https://www.linkedin.com/in/pedro-rjimenez/">
    <img src="https://img.shields.io/badge/pedro__rjcl-blue.svg?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Badge">
  </a>
</div>

<br>

- 🗂️ Este repositorio recoge los avances y códigos del [Proyecto IE24.1401 de Innovación Educativa](https://innovacioneducativa.upm.es/proyectos-ie/informacion?anyo=2023-2024&id=1160)

- 🎯 Objetivo: Permitir a los estudiantes realizar actividades de autovaluación de una forma más autónoma y cercana.

- 🎓 Proyecto liderado por:
  - 🎓 Féliz Arévalo Lozano
  - 🎓 Andrés Keyvan Salehi Paniagua
  - 🎓 Marcos Chimeno Manguán
  - 🎓 Pablo García-Fogeda Nuñez  

<br>

### <ins>Documentación</ins>

 - [Documentación de Telethon](https://docs.telethon.dev/en/stable/)
 - [Memoria del proyecto](https://www.overleaf.com/read/nvbqkrzspbjp#ad7e05)

<br>

### <ins>Instalación Python y Telethon</ins>

El back-end del bot está escrito en `Python (versión 3.12.2)`.

Podemos comprobar si está instalado, ejecutandolo en la terminal/PowerShell: 

```bash
pyhton --version
```

Nos habrá devuelto algo así, es recomendable usar la misma versión o más reciente:

```
Python 3.12.2
```

Necesitamos por otra parte instalar las dependencias necesarias, en este caso, telethon.
```bash
pip install telethon
```

<br>

### <ins>Clonar el repositorio</ins>

Debemos empezar por clonar el repositorio.

Para ello abriremos Visual Code y pulsaremos `Ctrl + Shift + P`.

Aquí en la barra de búsqueda del propio Visual Code habrá aparecido un ">". Con ello buscaremos la acción `Git: Clone` y la seleccionamos.

Nos pedirá que escribamos el nombre del repositorio (o el URL), lo introducimos:

```bash
https://github.com/pedrorj2/Telegram-Gamification-UPM/
```

Nos abrirá el explorador para elegir una ruta local donde clonar dicho repositorio.

Al hacerlo nos saldrá una pestaña donde nos dice de abrir el repositorio, lo aceptamos.

<br>

### <ins>Despliegue del bot</ins>

Una vez clonado y abierto el repositorio con Visual Code, debemos rellenar los datos de identificación de nuestro bot que podemos ver en las primeras líneas comentadas, hemos de rellenarlos y descomentar dichas variables.

```bash
# Configuración de tu API de Telegram
# api_id = ' '
# api_hash = ' '
# bot_token = ' '
```

`api_id` y `api_hash` se obtienen creando una ¨Aplicación de Telegram¨ através de https://my.telegram.org/apps.

`bot_token` lo obtenemos directamente de la aplicación de Telegram a través del Bot [@BotFather](https://t.me/BotFather).
Para ello debemos crear un bot, elegir su nombre y con ello conseguiremos este `token to access the HTTP API`.

Con esto, podemos ejecutar nuestro código y nuestro ordenador alojará el back-end del bot, mientras esté ejecutándose, nuestro bot responderá a las acciones, pero si cerramos el Visual Code, dejará de funcionar dicho bot hasta que lo volvamos a iniciar.



