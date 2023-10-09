import requests
import json

# Solicitar el nombre de la provincia en inglés
provincia = input("Dime la provincia en inglés que quieres consultar: ")

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
            f"La temperatura actual en la provincia de {provincia} es de : {tempActual}"
        )
        print(f"La temperatura máxima en la provincia de {provincia} es de : {tempMax}")
        print(f"La temperatura mínima en la provincia de {provincia} es de : {tempMin}")

    # Si hay un error en la petición, devuelve esto:
    else:
        print(
            f"Error al realizar la solicitud. Código de estado: {response.status_code}"
        )
# Si hay algún otro error cualquiera que no podemos controlar, salta la excepción.
except requests.exceptions.RequestException as e:
    print(f"Error de conexión: {e}")
