import requests
import openai
import json


print("Bienvenido a tu meteorólogo de confianza, selecciona una opción para ")
# Solicitar el nombre de la provincia
provincia = input("Dime la provincia que quieres consultar: ")

# URL de la API de pronóstico del tiempo (sustituye por la URL correcta)
url = f"https://api.openweathermap.org/data/2.5/weather?q={provincia}&units=metric&appid=ddccd66e42b270c765e7ea196e4e220c"

try:
    # Realiza la solicitud GET a la URL para comprobar que comunica.
    response = requests.get(url)

    # Si la solicitud se hace con éxito, el código de la respuesta devuelve 200.
    if response.status_code == 200:
        datosClima = response.json()

        tempActual = datosClima["main"]["temp"]
        tempMax = datosClima["main"]["temp_max"]
        tempMin = datosClima["main"]["temp_min"]

        openai.api_key = "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"
        completion = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Este es el tiempo en {provincia}, la temperatura actual es de {tempActual}ºC, la temperatura máxima es de {tempMax}ºC y la temperatura mínima es de {tempMin}ºC. ¿Podrías hacerme un resumen y un comentario gracioso acerca estos datos?",
            max_tokens=2048,
        )

        # prompt = f"Los datos del pronóstico del tiempo en {provincia} son los siguientes:\n\n- Temperatura actual: {tempActual}°C\n- Temperatura máxima: {tempMax}°C\n- Temperatura mínima: {tempMin}°C\n- Sensación térmica: {sensTermica}°C\n- Velocidad del viento: {velViento} m/s\n- Nivel de nubes: {nubes}%\n\n ¿Qué conclusiones podemos sacar de esta información? ¿Cómo afectará esta temperatura a las actividades al aire libre en {provincia}? ¿Algún consejo basado en estos datos para los residentes?"

        print(completion.choices[0].text)

        # Imprimo la información
        print(
            f"La temperatura actual en {provincia} es de : {tempActual} ºC, la máxima es de {tempMax} ºC y  la mínima es de {tempMin} ºC"
        )

        respuesta = input("¿Quieres ampliar información? (Responde con sí o no )")
        while respuesta != "si" and respuesta != "no":
            respuesta = input("Respuesta errónea, debes responder con sí o no ")
        if respuesta == "si":
            sensTermica = datosClima["main"]["feels_like"]
            velViento = datosClima["wind"]["speed"]
            nubes = datosClima["clouds"]["all"]
            nubosidad = ""
            if nubes == 0:
                nubosidad = "despejado de nubes"
            if nubes > 0 < 50:
                nubosidad = "algo nublado"
            if nubes > 50:
                nubosidad = "muy nublado"
            print(
                f"De acuerdo, aquí tienes la velocidad del viento, {velViento} KM/h, la sensación térmica es de {sensTermica} ºC, y el cielo está {nubosidad}"
            )
        elif respuesta == "no":
            print("Usted se lo pierde, ¡Que tenga un buen día!")

    # Si hay un error en la petición, devuelve esto:
    else:
        print(
            f"Error al realizar la solicitud. Código de estado: {response.status_code}"
        )
# Si hay algún otro error cualquiera que no podemos controlar, salta la excepción.
except requests.exceptions.RequestException as e:
    print(f"Error de conexión: {e}")
