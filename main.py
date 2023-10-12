import requests
import json
from datetime import datetime, timedelta


# Funciones necesarias


def menu():
    print("\n--------------------Menu--------------------")
    print("1. Tiempo actual")
    print("2. Tiempo en los próximos 4 días")
    print("3. Tiempo en un día y hora concreta")
    print("4. Cambiar el lugar a consultar")
    print("5. Salir")
    print("--------------------------------------------")


def obtenerTemperaturaMaximaDia(fecha):
    maxTemp = -200
    tempMaxItemActual = -200
    for item in datosClima5Dias["list"]:
        itemFecha = item["dt_txt"].split(" ")[
            0
        ]  # Con esto obtengo la fecha del item actual, y la divido en dos partes, la fecha y la hora, y me quedo con la fecha
        if fecha == itemFecha:
            tempMaxItemActual = float(item["main"]["temp_max"])
            if tempMaxItemActual > maxTemp:
                maxTemp = tempMaxItemActual
    return maxTemp


def obtenerTemperaturaMinimaDia(fecha):
    minTemp = 200
    minTempItemActual = 200

    for item in datosClima5Dias["list"]:
        fechaItemActual = item["dt_txt"].split(" ")[0]
        if fechaItemActual == fecha:
            minTempItemActual = item["main"]["temp_min"]
            if minTempItemActual < minTemp:
                minTemp = minTempItemActual

    return minTemp


def obtenerJsonTiempoActual(lugar):
    urlTiempoActual = f"https://api.openweathermap.org/data/2.5/weather?q={lugar}&units=metric&appid=ddccd66e42b270c765e7ea196e4e220c"
    try:
        # Realiza la solicitud GET a la urlTiempoActual para comprobar que comunica.
        responseActual = requests.get(urlTiempoActual)
        if responseActual.status_code == 200:
            return responseActual.json()
        else:
            print(
                f"Error al realizar la solicitud. Código de estado: {responseActual.status_code}, seleccione la opción 4 para cambiar el lugar a consultar."
            )
    # Si hay algún otro error cualquiera que no podemos controlar, salta la excepción.
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")


def obtenerJsonTiempoEn5Dias(lugar):
    urlTiempo5Dias = f"https://api.openweathermap.org/data/2.5/forecast?q={lugarConsultado}&units=metric&appid=ddccd66e42b270c765e7ea196e4e220c"
    try:
        # Realiza la solicitud GET a la urlTiempoActual para comprobar que comunica.
        response5Dias = requests.get(urlTiempo5Dias)
        if response5Dias.status_code == 200:
            return response5Dias.json()
        else:
            print(
                f"Error al realizar la solicitud. Código de estado: {response5Dias.status_code}, seleccione la opción 4 para cambiar el lugar a consultar."
            )
    # Si hay algún otro error cualquiera que no podemos controlar, salta la excepción.
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")


def opcion1(datosClimaActual):
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
    print(f"La temperatura actual en {lugarConsultado} es de : {tempActual} ºC")
    print(f"La sensación térmica es de : {sensTermica} ºC")
    print(f"La velocidad del viento es de : {velViento} KM/h")
    print(f"El nivel de nubes es de : {nubes} %, por lo tanto está {nubosidad}")


def opcion2(datosClima5Dias):
    # bucle for tradicional para usar el range y poder iterar en los 4 días siguientes
    for i in range(1, 5):
        fechaAProcesar = fechaProximosDiasString(datetime.now(), i)
        maxTemp = obtenerTemperaturaMaximaDia(fechaAProcesar)
        minTemp = obtenerTemperaturaMinimaDia(fechaAProcesar)
        print(f"La temperatura máxima para {fechaAProcesar} es de {maxTemp}")
        print(f"La temperatura mínima para {fechaAProcesar} es de {minTemp}")


def fechaProximosDiasString(fecha, dias):
    fechaActual = datetime.now()
    fechaDiaDeseado = fechaActual + timedelta(days=dias)
    return fechaDiaDeseado.strftime(
        "%Y-%m-%d"
    )  # Lo devuelvo en ese formato para que se pueda comparar con el json que nos devuelve la api.


# engine.say("Bienvenido a tu meteorólogo de confianza, selecciona una opción para ")
print("Bienvenido a tu meteorólogo de confianza")
# Solicitar el nombre de la lugarConsultado
lugarConsultado = input(
    "Para empezar, dime cualquier lugar del mundo el cual quieres consultar: "
)

# Declaramos dos variables globales que nos van a servir en nuestro programa:
datosClimaActual = obtenerJsonTiempoActual(lugarConsultado)
datosClima5Dias = obtenerJsonTiempoEn5Dias(lugarConsultado)


# Menú


# Pregunto al usuario que quiere saber
salir = False
while salir == False:
    menu()
    opcion = int(
        input(f"Tienes seleccinado {lugarConsultado}, elige una opción del 1 al 5: ")
    )
    if opcion in range(1, 6):
        if opcion == 1:
            opcion1(datosClimaActual)
        elif opcion == 2:
            opcion2(datosClima5Dias)
        elif opcion == 3:
            print("En desarrollo")
        elif opcion == 4:
            lugarConsultado = input("Dime un nuevo lugar a consultar: ")
            print(f"Has elegido {lugarConsultado}")
            datosClimaActual = obtenerJsonTiempoActual(lugarConsultado)
            datosClima5Dias = obtenerJsonTiempoEn5Dias(lugarConsultado)
        elif opcion == 5:
            print("¡Que tenga un buen día!")
            salir = True
    else:
        print("Opción incorrecta, elige una opción del 1 al 5.")
