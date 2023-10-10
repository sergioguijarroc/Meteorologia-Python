import requests
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
        else:
            print("Error de la respuesta, dígame otra")

    # Si hay un error en la petición, devuelve esto:
    else:
        print(
            f"Error al realizar la solicitud. Código de estado: {response.status_code}"
        )
# Si hay algún otro error cualquiera que no podemos controlar, salta la excepción.
except requests.exceptions.RequestException as e:
    print(f"Error de conexión: {e}")
