from telethon import TelegramClient, events
from telethon.tl.custom import Button
import os
import re
from datetime import datetime

# Configuración de tu API de Telegram
api_id = '28092530'
api_hash = 'dcedc3ea5fbfb53690f7d80873e0d5d6'
bot_token = '7054644239:AAEW7CeuGvshPfdM_iN_LQFFdwmTgr_IiHI'

# Iniciar el cliente de Telegram
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

# Carpeta donde se encuentran los archivos de preguntas y actividades
preguntas_folder = r'Preguntas'

# Diccionario para mantener las selecciones de respuestas
selecciones_pregunta = {}

# Lista para mantener a los usuarios activos
usuarios_activos = set()

# Almacenar las respuestas de un usuario
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

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
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

@client.on(events.NewMessage(pattern='/respuestas'))
async def ver_respuestas(event):
    if event.sender.username != 'aeropedrax':
        await event.respond("No tienes permiso para usar este comando.")
        return

    username = event.raw_text.split(' ')[1]
    if username.startswith('@'):
        username = username[1:]  # Remove '@' from username

    try:
        user = await client.get_entity(username)
        user_id = user.id
        if user_id in respuestas_de_usuarios:
            respuesta_texto = ""  # Iniciar un string vacío para acumular las respuestas
            for respuesta in respuestas_de_usuarios[user_id]:
                respuesta_texto += respuesta + "\n\n"  # Añadir respuesta y dos saltos de línea
            print(f"[ADMIN] Respuestas almacenadas para {username}:\n\n{respuesta_texto}")
            await event.respond("Respuestas del usuario impresas en la consola.")
        else:
            await event.respond("No se encontraron respuestas para este usuario.")
    except ValueError:
        await event.respond("Usuario no encontrado.")



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

        # Almacenar las respuestas
        if event.sender_id not in respuestas_de_usuarios:
            respuestas_de_usuarios[event.sender_id] = []
        resumen_respuesta = f"Usuario {event.sender.username} ha respondido la pregunta {numero_pregunta} del tema {''.join(re.findall(r'\d+', archivo_seleccionado))} \n{resultado}"
        respuestas_de_usuarios[event.sender_id].append(resumen_respuesta)

        # Restablecer selecciones a False después de enviar la respuesta
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