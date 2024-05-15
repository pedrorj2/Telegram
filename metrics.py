import csv

def ranking_usuarios(archivo='respuestas.csv'):
    with open(archivo, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        ranking = {}
        for row in reader:
            if len(row) >= 4:
                username, tema_pregunta, numero_pregunta, puntuacion, _ = row
                if username not in ranking:
                    ranking[username] = 0
                ranking[username] += int(puntuacion.replace('%', ''))
        ranking_ordenado = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
        return ranking_ordenado


def media_puntuacion(archivo='respuestas.csv'):
    with open(archivo, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        puntuaciones = []
        for row in reader:
            if len(row) >= 4:
                _, _, _, puntuacion, _ = row
                puntuaciones.append(int(puntuacion.replace('%', '')))
        puntuacion_media = sum(puntuaciones) / len(puntuaciones)
        return puntuacion_media
    

def media_intentos(archivo='respuestas.csv'): #quiero ver los intentos medios de los alumnos antes de responder correctamente una pregunta por primera vez
    with open(archivo, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        intentos = {}
        for row in reader:
            if len(row) >= 4:
                username, tema_pregunta, numero_pregunta, puntuacion, _ = row
                if username not in intentos:
                    intentos[username] = 0
                intentos[username] += 1
        intentos_medios = sum(intentos.values()) / len(intentos)
        return intentos_medios

