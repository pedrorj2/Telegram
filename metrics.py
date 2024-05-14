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