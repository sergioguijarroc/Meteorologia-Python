import requests
import json
from datetime import datetime, timedelta


# engine.say("Bienvenido a tu meteorólogo de confianza, selecciona una opción para ")
print("Bienvenido a tu meteorólogo de confianza")
# Solicitar el nombre de la lugarConsultado
lugarConsultado = input(
    "Para empezar, dime cualquier lugar del mundo el cual quieres consultar: "
)

# urlTiempoActual de la API de pronóstico del tiempo (sustituye por la urlTiempoActual correcta)
urlTiempoActual = f"https://api.openweathermap.org/data/2.5/weather?q={lugarConsultado}&units=metric&appid=ddccd66e42b270c765e7ea196e4e220c"
urlTiempo5Dias = f"https://api.openweathermap.org/data/2.5/forecast?q={lugarConsultado}&units=metric&appid=ddccd66e42b270c765e7ea196e4e220c"


try:
    # Realiza la solicitud GET a la urlTiempoActual para comprobar que comunica.
    responseActual = requests.get(urlTiempoActual)
    response5Dias = requests.get(urlTiempo5Dias)

    # Si la solicitud se hace con éxito, el código de la respuesta devuelve 200.
    if responseActual.status_code == 200 and response5Dias.status_code == 200:
        datosClimaActual = responseActual.json()
        datosClima5Dias = response5Dias.json()

        # prompt = f"Los datos del pronóstico del tiempo en {lugarConsultado} son los siguientes:\n\n- Temperatura actual: {tempActual}°C\n- Temperatura máxima: {tempMax}°C\n- Temperatura mínima: {tempMin}°C\n- Sensación térmica: {sensTermica}°C\n- Velocidad del viento: {velViento} m/s\n- Nivel de nubes: {nubes}%\n\n ¿Qué conclusiones podemos sacar de esta información? ¿Cómo afectará esta temperatura a las actividades al aire libre en {lugarConsultado}? ¿Algún consejo basado en estos datos para los residentes?"

        # Menú
        print("--------------------Menu--------------------")
        print("1. Tiempo actual")
        print("2. Tiempo en los próximos 5 días")
        print("3. Tiempo en un día y hora concreta")
        print("4. Salir")
        print("--------------------------------------------")
        # Pregunto al usuario que quiere saber
        salir = False
        while salir == False:
            opcion = int(input("Elige una opción: "))
            if opcion in range(1, 5):
                if opcion == 1:
                    # Cargamos en variables desde el json todos los datos que vamos a necesitar
                    tempActual = datosClimaActual["main"]["temp"]
                    tempMax = datosClimaActual["main"]["temp_max"]
                    tempMin = datosClimaActual["main"]["temp_min"]
                    velViento = datosClimaActual["wind"]["speed"]
                    nubes = datosClimaActual["clouds"]["all"]
                    sensTermica = datosClimaActual["main"]["feels_like"]

                    # Condiciones para saber si está nublado o no
                    if 0 < nubes < 50:
                        nubosidad = "algo nublado"
                    elif nubes >= 50:
                        nubosidad = "muy nublado"
                    else:
                        nubosidad = "despejado de nubes"
                    print(
                        f"La temperatura actual en {lugarConsultado} es de : {tempActual} ºC, y puede evolucionar en las próximas horas a : {tempMax} ºC o a : {tempMin} ºC"
                    )
                    print(f"La sensación térmica es de : {sensTermica} ºC")
                    print(f"La velocidad del viento es de : {velViento} KM/h")
                    print(
                        f"El nivel de nubes es de : {nubes} %, por lo tanto está {nubosidad}"
                    )

                elif opcion == 2:
                    # En esta opción, debemos coger la fecha del día actual, e ignorar los datos que coincidan en el día actual del json que nos devuelve la API de 5 días.
                    # Primero, obtenemos la fecha actual
                    fechaActual = datetime.now()
                    # Obtenemos la fecha de mañana
                    fechaMañana = fechaActual + timedelta(days=1)

                    # Transformamos la fecha actual y la de mañana a formato string
                    fechaActualString = fechaActual.strftime("%Y-%m-%d")
                    fechaMañanaString = fechaMañana.strftime("%Y-%m-%d")

                    # Quiero almacenar en una variable el valor actual del día, recorrer todas las fechas del json e ignorar los que coincidan con el día actual. El objetivo es recorrer desde las 00:00 del día siguiente hasta las 00:00 del siguiente día a dicho día, me almacene en una variable minTemp la temperatura mínima de todo ese día y en maxTemp la temperatura máxima de todo ese otro día
                    # Inicializo los valores de forma que sean la mínima muy alta y la máxima muy baja
                    minTemp = 200
                    maxTemp = -200
                    tempMinItemActual = 200
                    tempMaxItemActual = -200
                    # Voy a recorrer los datos en el JSON
                    for item in datosClima5Dias["list"]:
                        itemFecha = item["dt_txt"].split(" ")[0]
                        if fechaMañanaString == itemFecha:
                            tempMinItemActual = float(item["main"]["temp_min"])
                            tempMaxItemActual = float(item["main"]["temp_max"])
                        if minTemp > tempMinItemActual:
                            minTemp = tempMinItemActual
                        if maxTemp < tempMaxItemActual:
                            maxTemp = tempMaxItemActual

                    print(
                        f"La temperatura máxima para {fechaMañanaString} es de {maxTemp}"
                    )
                    print(
                        f"La temperatura mínima para {fechaMañanaString} es de {minTemp}"
                    )
                elif opcion == 3:
                    print("En desarrollo")
                elif opcion == 4:
                    print("¡Que tenga un buen día!")
                    salir = True
            else:
                print("Opción incorrecta, elige una opción del 1 al 4.")

    # Si hay un error en la petición, devuelve esto:
    else:
        print(
            f"Error al realizar la solicitud. Código de estado: {responseActual.status_code}"
        )
# Si hay algún otro error cualquiera que no podemos controlar, salta la excepción.
except requests.exceptions.RequestException as e:
    print(f"Error de conexión: {e}")
