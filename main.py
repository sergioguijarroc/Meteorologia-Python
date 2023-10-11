import requests
import json

# import pyttsx3

# Inicializar el motor de voz
# engine = pyttsx3.init()


# engine.say("Bienvenido a tu meteorólogo de confianza, selecciona una opción para ")
print("Bienvenido a tu meteorólogo de confianza, selecciona una opción para ")
# Solicitar el nombre de la provincia
provincia = input("Dime cualquier lugar del mundo el cual quieres consultar: ")

# URL de la API de pronóstico del tiempo (sustituye por la URL correcta)
url = f"https://api.openweathermap.org/data/2.5/weather?q={provincia}&units=metric&appid=ddccd66e42b270c765e7ea196e4e220c"

try:
    # Realiza la solicitud GET a la URL para comprobar que comunica.
    response = requests.get(url)

    # Si la solicitud se hace con éxito, el código de la respuesta devuelve 200.
    if response.status_code == 200:
        datosClima = response.json()

        # prompt = f"Los datos del pronóstico del tiempo en {provincia} son los siguientes:\n\n- Temperatura actual: {tempActual}°C\n- Temperatura máxima: {tempMax}°C\n- Temperatura mínima: {tempMin}°C\n- Sensación térmica: {sensTermica}°C\n- Velocidad del viento: {velViento} m/s\n- Nivel de nubes: {nubes}%\n\n ¿Qué conclusiones podemos sacar de esta información? ¿Cómo afectará esta temperatura a las actividades al aire libre en {provincia}? ¿Algún consejo basado en estos datos para los residentes?"

    # Realiza la solicitud GET a la URL para comprobar que comunica.
    response = requests.get(url)
    # Si la solicitud se hace con éxito, el código de la respuesta devuelve 200.
    if response.status_code == 200:
        datosClima = response.json()

        # Menú
        print("--------------------Menu--------------------")
        print("1. Temperatura actual")
        print("2. Temperatura máxima")
        print("3. Temperatura mínima")
        print("4. Sensación térmica")
        print("5. Velocidad del viento")
        print("6. Nivel de nubes")
        print("7. Salir")
        print("--------------------------------------------")
        # print("--------------------Menu--------------------\n1. Temperatura actual\n2. Temperatura máxima\n3. Temperatura mínima\n4. Sensación térmica\n5. Velocidad del viento\n6. Nivel de nubes\n7. Salir\n--------------------------------------------")

        # Pregunto al usuario que quiere saber
        salir = False
        while salir == False:
            opcion = int(input("Elige una opción: "))
            if opcion in range(1, 8):
                if opcion == 1:
                    tempActual = datosClima["main"]["temp"]
                    print(
                        f"La temperatura actual en {provincia} es de : {tempActual} ºC"
                    )
                elif opcion == 2:
                    tempMax = datosClima["main"]["temp_max"]
                    print(f"La temperatura máxima en {provincia} es de : {tempMax} ºC")
                elif opcion == 3:
                    tempMin = datosClima["main"]["temp_min"]
                    print(f"La temperatura mínima en {provincia} es de : {tempMin} ºC")
                elif opcion == 4:
                    sensTermica = datosClima["main"]["feels_like"]
                    print(
                        f"La sensación térmica en {provincia} es de : {sensTermica} ºC"
                    )
                elif opcion == 5:
                    velViento = datosClima["wind"]["speed"]
                    print(
                        f"La velocidad del viento en {provincia} es de : {velViento} KM/h"
                    )
                elif opcion == 6:
                    nubes = datosClima["clouds"]["all"]
                    if 0 < nubes < 50:
                        nubosidad = "algo nublado"
                    elif nubes >= 50:
                        nubosidad = "muy nublado"
                    else:
                        nubosidad = "despejado de nubes"
                    print(
                        f"El nivel de nubes en {provincia} es de : {nubes} %, por lo tanto está {nubosidad}"
                    )
                elif opcion == 7:
                    print("¡Que tenga un buen día!")
                    salir = True
            else:
                print("Opción incorrecta, elige una opción del 1 al 7.")

    # Si hay un error en la petición, devuelve esto:
    else:
        print(
            f"Error al realizar la solicitud. Código de estado: {response.status_code}"
        )
# Si hay algún otro error cualquiera que no podemos controlar, salta la excepción.
except requests.exceptions.RequestException as e:
    print(f"Error de conexión: {e}")
