# -*- coding: utf-8 -*-
import redis
import json
import settings
from classifier import SentimentClassifier
import time

db = redis.Redis(host='redis', port= settings.REDIS_PORT, db=0)

model = SentimentClassifier()

def sentiment_from_score(score):
    """
    Esta función recibe como entrada el score de positividad
    de nuestra sentencia y dependiendo su valor devuelve uno
    de las siguientes clases:
        - "Positivo": Cuando el score es mayor a 0.55.
        - "Neutral": Cuando el score se encuentra entre 0.45 y 0.55.
        - "Negativo": Cuando el score es menor a 0.45.

    Attributes
    ----------
    score : float
        Porcentaje de positividad.

    Returns
    -------
    sentiment : str
        Una de las siguientes etiquetas: "Negativo", "Neutral" o "Positivo".
    """
    ####################################################################
    if score<.45:
        sentiment = 'Negativo'
    elif .45 < score < 0.55:
        sentiment = 'Neutral'
    else:
        sentiment = 'Positivo'
    #raise NotImplementedError
    ####################################################################

    return sentiment


def predict(text):
    """
    Esta función recibe como entrada una oración y devuelve una
    predicción de su sentimiento acompañado del score de positividad.

    Attributes
    ----------
    text : str
        Sentencia para analizar

    Returns
    -------
    sentiment : str
        Una de las siguientes etiquetas: "Negativo", "Neutral" o "Positivo".
    score : float
        Porcentaje de positividad.
    """
    sentiment = None
    score = None

    score = model.predict(text)
    sentiment = sentiment_from_score(score)
    # sleep para simular un computo complejo
    time.sleep(10)
    
    return sentiment, score


def classify_process():
    """
    Obtiene trabajos encolados por el cliente desde Redis. Los procesa
    y devuelve resultados.
    Toda la comunicación se realiza a travez de Redis, por ello esta
    función no posee atributos de entrada ni salida.
    """
    # Iteramos intentando obtener trabajos para procesar
    while True:
        queue = db.lrange('service_queue', 0, 9)

        # Iteramos por cada trabajo obtenido
        for q in queue:
            # 1)
            q = json.loads(q.decode('utf-8'))
            job_id = q['id']
            sentiment, score = predict(q['text'])

            # 2)
            response = {'prediction': sentiment, 'score': score}

            # 3)
            db.set(job_id, json.dumps(response))

        db.ltrim(settings.REDIS_QUEUE, len(queue), -1)
        time.sleep(2)


if __name__ == "__main__":
    print('Launching ML service...')
    classify_process()
