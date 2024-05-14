from telethon import TelegramClient, events
from telethon.tl.custom import Button
from datetime import datetime

from config import api_id, api_hash, bot_token

import os
import re
import csv

# Configuración de tu API de Telegram, la importo del archivo config.py
# No es público por seguridad, sólo contiene estos tres datos de a continuación:
# api_id = ' '
# api_hash = ' '
# bot_token = ''

# Iniciar el cliente de Telegram
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

# Carpeta donde se encuentran los archivos de preguntas y actividades
preguntas_folder = r'Preguntas'

# Diccionario para mantener las selecciones de respuestas
selecciones_pregunta = {}

# Lista para mantener a los usuarios activos
usuarios_activos = set()

# Almacenar las respuestas de un usuario con mejor estructura
respuestas_de_usuarios = {}

# Función para obtener las preguntas desde el archivo
def obtener_preguntas_desde_archivo(archivo):
    ruta_completa = os.path.join(preguntas_folder, archivo)
    with open(ruta_completa, 'r', encoding='utf-8') as file:
        contenido = file.read()

    preguntas = re.findall(r'::(.*?)\{(.*?)\}', contenido, re.DOTALL)
    preguntas_procesadas = []

    for titulo, opciones in preguntas:
        titulo_limpio = titulo.replace(':: ', '').strip()
        # Transformamos el formato multirespuesta de %positivo% y %negativo%
        opciones = re.sub(r'~%-\d+%', '~', opciones)
        opciones = re.sub(r'~%\d+%', '=', opciones)
        # Leemos la separación entre respuestas
        opciones = re.findall(r'([=~])(.*?)\s*(?=\n|\Z)', opciones)
        # Procesamos las respuestas correctas '='
        opciones_procesadas = [(opcion.strip()[0].upper() + opcion.strip()[1:].lower(), tipo == '=') for tipo, opcion in opciones]
        preguntas_procesadas.append((titulo_limpio, opciones_procesadas))

    return preguntas_procesadas

# Función para listar los archivos de preguntas disponibles
def listar_archivos_preguntas(prefijo):
    archivos = [f for f in os.listdir(preguntas_folder) if f.startswith(prefijo) and f.endswith('.txt')]
    return archivos

def guardar_csv(usuario, datos, archivo='respuestas.csv'):
    with open(archivo, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Asegurarse de que 'datos' es una lista de tuplas (tema, pregunta, puntuación)
        for dato in datos:
            writer.writerow([usuario, *dato, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            
def cargar_csv(archivo='respuestas.csv'):
    try:
        with open(archivo, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 4:
                    username, tema_pregunta, numero_pregunta, puntuacion, _ = row
                    clave_respuesta = (tema_pregunta, numero_pregunta)
                    if username not in respuestas_de_usuarios:
                        respuestas_de_usuarios[username] = {}
                    if clave_respuesta not in respuestas_de_usuarios[username]:
                        respuestas_de_usuarios[username][clave_respuesta] = []
                    respuestas_de_usuarios[username][clave_respuesta].append(puntuacion)
    except FileNotFoundError:
        print("Archivo de resultados no encontrado, iniciando sin datos previos.")



@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    cargar_csv()  # Carga los datos justo después de iniciar el cliente
    # Añadir usuario a la lista de activos cuando inicia el bot
    usuarios_activos.add(event.sender_id)
    print(f"Usuario {event.sender.username} inició el bot - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    archivos = listar_archivos_preguntas('tema_')
    buttons = [[Button.inline(f'{archivo.replace(".txt", "").replace("_", " ").title()}', f'archivo_{archivo}')] for archivo in archivos]
    await event.respond('Elige un tema:', buttons=buttons)

@client.on(events.NewMessage(pattern='/activities'))
async def lanzar_actividad(event):
    # Verificar si el usuario es aeropedrax
    if event.sender.username != 'aeropedrax':
        await event.respond("No tienes permiso para usar este comando.")
        print(f"El usuario {event.sender.username} está intentando lanzar una actividad (sin éxito xd)")
        return
    print(f"El profesor {event.sender.username} está lanzando una actividad ")
    # Buscar archivos de actividades en la carpeta preguntas_folder
    archivos_actividad = listar_archivos_preguntas('actividad_')
    # Presentar archivos de actividad al profesor para seleccionar
    buttons = [[Button.inline(f'{archivo.replace(".txt", "").replace("_", " ").title()}', f'archivo_{archivo}')] for archivo in archivos_actividad]
    await event.respond('Elige un archivo de actividad:', buttons=buttons)

@client.on(events.NewMessage(pattern='/datos'))
async def ver_datos(event):
    username = event.sender.username if event.sender.username else f"user_{event.sender_id}"
    if username in respuestas_de_usuarios:
        # datos_usuario = respuestas_de_usuarios[username]
        # Ordenar las claves (tema y pregunta) antes de imprimir los resultados
        claves_ordenadas = sorted(respuestas_de_usuarios[username].keys(), key=lambda x: (int(x[0]), int(x[1])))
        
        respuesta_texto = "Datos almacenados:\n"
        for clave in claves_ordenadas:
            puntuaciones = respuestas_de_usuarios[username][clave]
            # Aplicar el formato sin decimales a todas las puntuaciones
            puntuaciones_formateadas = [f"{float(p.replace('%', '')):.0f}%" for p in puntuaciones]
            respuesta_texto += f"Tema {clave[0]}, Pregunta {clave[1]}: {', '.join(puntuaciones_formateadas)}\n"


        
        await event.respond(respuesta_texto)
    else:
        await event.respond("No hay datos almacenados para tu usuario.")
      



@client.on(events.CallbackQuery)
async def callback_query_handler(event):
    data = event.data.decode()

    if data.startswith('archivo_'):
        archivo_seleccionado = data.split('archivo_')[1]
        preguntas = obtener_preguntas_desde_archivo(archivo_seleccionado)
        # Inicializar selecciones para cada pregunta en este archivo
        selecciones_pregunta[archivo_seleccionado] = [[False] * len(opciones) for _, opciones in preguntas]

        buttons = [[Button.inline(f'Pregunta {i}', f'preg_{i}_{archivo_seleccionado}')] for i, _ in enumerate(preguntas, start=1)]
        buttons.append([Button.inline('🏠 Volver al inicio', 'start')])
        await event.edit('Elige una pregunta:', buttons=buttons)

    elif data.startswith('actividad_'):
        archivo_actividad = data.split('actividad_')[1]
        preguntas = obtener_preguntas_desde_archivo(archivo_actividad)
        # Aquí puedes implementar la lógica para mostrar las preguntas y enviarlas en directo

        # Por ahora, simplemente imprimimos las preguntas como ejemplo
        for titulo, opciones in preguntas:
            texto_opciones = "\n".join([f"{chr(65 + i)}. {opcion[0]}" for i, opcion in enumerate(opciones)])
            print(f'{titulo}\n\n{texto_opciones}\n')

        await event.answer('Actividad lanzada con éxito.')

    if data.startswith('preg_'):
        _, numero_pregunta, archivo_seleccionado = data.split('_', 2)
        preguntas = obtener_preguntas_desde_archivo(archivo_seleccionado)
        pregunta, opciones = preguntas[int(numero_pregunta) - 1]

        # Calcular cuántas respuestas correctas hay
        total_correctas = sum(1 for _, correcta in opciones if correcta)
        # Formular la pregunta adecuadamente según el número de respuestas correctas
        instruccion_pregunta = "la única opción correcta:" if total_correctas == 1 else f"las {total_correctas} respuestas correctas:"

        texto_pregunta = f"{pregunta}\n\nSeleccione {instruccion_pregunta}"
        texto_opciones = "\n".join([f"{chr(65 + i)}. {opcion[0]}" for i, opcion in enumerate(opciones)])
        seleccion_actual = selecciones_pregunta[archivo_seleccionado][int(numero_pregunta) - 1]
        buttons = generar_botones_pregunta(seleccion_actual, numero_pregunta, archivo_seleccionado)
        buttons.append([Button.inline('📤 Enviar respuesta', f'enviar_{numero_pregunta}_{archivo_seleccionado}')])
        buttons.append([Button.inline('🔙 Volver al tema', f'archivo_{archivo_seleccionado}')])

        await event.edit(f'{texto_pregunta}\n\n{texto_opciones}', buttons=buttons)

    elif data.startswith('select_'):
        _, numero_pregunta, opcion_seleccionada, archivo_seleccionado = data.split('_', 3)
        preguntas = obtener_preguntas_desde_archivo(archivo_seleccionado)
        pregunta, opciones = preguntas[int(numero_pregunta) - 1]

        # Actualizar las selecciones
        selecciones = selecciones_pregunta[archivo_seleccionado][int(numero_pregunta) - 1]
        selecciones[int(opcion_seleccionada)] = not selecciones[int(opcion_seleccionada)]

        # Mantener la instrucción original basada en la cantidad de respuestas correctas
        total_correctas = sum(1 for _, correcta in opciones if correcta)
        instruccion_pregunta = "la única opción correcta:" if total_correctas == 1 else f"las {total_correctas} respuestas correctas:"

        texto_pregunta = f"{pregunta}\n\nSeleccione {instruccion_pregunta}"
        texto_opciones = "\n".join([f"{chr(65 + i)}. {opcion[0]}" for i, opcion in enumerate(opciones)])
        buttons = generar_botones_pregunta(selecciones, numero_pregunta, archivo_seleccionado)
        buttons.append([Button.inline('📤 Enviar respuesta', f'enviar_{numero_pregunta}_{archivo_seleccionado}')])
        buttons.append([Button.inline('🔙 Volver al tema', f'archivo_{archivo_seleccionado}')])

        await event.edit(f'{texto_pregunta}\n\n{texto_opciones}', buttons=buttons)

    if data.startswith('enviar_'):
        _, numero_pregunta, archivo_seleccionado = data.split('_', 2)
        preguntas = obtener_preguntas_desde_archivo(archivo_seleccionado)
        pregunta, opciones = preguntas[int(numero_pregunta) - 1]
        selecciones = selecciones_pregunta[archivo_seleccionado][int(numero_pregunta) - 1]

        # Revisar si se ha hecho alguna selección
        if not any(selecciones):
            # Si no se ha seleccionado nada, informa al usuario y no hagas nada más
            await event.answer("Por favor, selecciona al menos una opción antes de enviar las respuestas.", alert=True)
            return

        # Comprobación de respuestas: verifica si alguna opción incorrecta fue seleccionada
        seleccion_incorrecta = any(seleccion and not correcta for seleccion, (_, correcta) in zip(selecciones, opciones))
        total_correctas = sum(1 for _, correcta in opciones if correcta)

        if seleccion_incorrecta:
            puntuacion = 0  # Si alguna incorrecta es seleccionada, la puntuación es cero
        else:
            correctas_seleccionadas = sum(seleccion for seleccion, (_, correcta) in zip(selecciones, opciones) if correcta)
            puntuacion = (correctas_seleccionadas / total_correctas) * 100 if total_correctas > 0 else 0

        resultado = "Respuestas:\n"
        for i, (opcion, correcta) in enumerate(opciones):
            if selecciones[i]:
                resultado += f"{chr(65 + i)} - {'Correcta' if correcta else 'Incorrecta'}\n"

        if puntuacion == 0 and total_correctas > 1:
            resultado += f"\nPuntuación: {puntuacion:.2f}%\n\nUna sola respuesta incorrecta anula el resto de respuestas."
        else:
            resultado += f"\nPuntuación: {puntuacion:.2f}%"

        tema_pregunta = ''.join(re.findall(r'\d+', archivo_seleccionado))
        username = event.sender.username if event.sender.username else f"user_{event.sender_id}"
        puntuacion_texto = f"{puntuacion:.0f}%"
        clave_respuesta = (tema_pregunta, numero_pregunta, puntuacion_texto)
        guardar_csv(username, [clave_respuesta])


        if username not in respuestas_de_usuarios:
            respuestas_de_usuarios[username] = {}
        clave_respuesta = (tema_pregunta, numero_pregunta)
        
        if clave_respuesta not in respuestas_de_usuarios[username]:
            respuestas_de_usuarios[username][clave_respuesta] = []
        
        respuestas_de_usuarios[username][clave_respuesta].append(f"{puntuacion:.2f}%")

        selecciones_pregunta[archivo_seleccionado][int(numero_pregunta) - 1] = [False] * len(opciones)

        # Enviar alerta con el resultado
        await event.answer(resultado, alert=True)

        # Restablecer la visualización de las opciones
        instruccion_pregunta = "la única opción correcta:" if total_correctas == 1 else f"las {total_correctas} respuestas correctas:"
        texto_pregunta = f"{pregunta}\n\nSeleccione {instruccion_pregunta}"
        texto_opciones = "\n".join([f"{chr(65 + i)}. {opcion[0]}" for i, opcion in enumerate(opciones)])
        buttons = generar_botones_pregunta([False] * len(opciones), numero_pregunta, archivo_seleccionado)
        buttons.append([Button.inline('📤 Enviar respuesta', f'enviar_{numero_pregunta}_{archivo_seleccionado}')])
        buttons.append([Button.inline('🔙 Volver al tema', f'archivo_{archivo_seleccionado}')])

        await event.edit(f'{texto_pregunta}\n\n{texto_opciones}', buttons=buttons)



    elif data == 'start':
        await start(event)  # Reutilizar la función de inicio

def generar_botones_pregunta(selecciones, num_pregunta, archivo):
    letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    buttons = []
    fila = []
    for i, seleccionada in enumerate(selecciones):
        texto_opcion = f'✓ {letras[i]}' if seleccionada else letras[i]
        fila.append(Button.inline(texto_opcion, f'select_{num_pregunta}_{i}_{archivo}'))
        if len(fila) == 4:
            buttons.append(fila)
            fila = []
    if fila:
        buttons.append(fila)
    return buttons

client.start()
client.run_until_disconnected()


client.disconnect()
