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


    while True:
        lugar = input(
            "Para empezar, dime cualquier lugar del mundo el cual quieres consultar: "
        )
        datos_clima_actual = obtenerJsonTiempoActual(lugar)
        datos_clima_5dias = obtenerJsonTiempoEn5Dias(lugar)

        if datos_clima_actual is not None and datos_clima_5dias is not None:
            return lugar, datos_clima_actual, datos_clima_5dias
        else:
            print("Lugar no encontrado. Introduce un lugar válido.")


def obtenerJsonTiempoActual(lugar):
    urlTiempoActual = f"https://api.openweathermap.org/data/2.5/weather?q={lugar}&units=metric&appid=ddccd66e42b270c765e7ea196e4e220c"
    try:
        # Realiza la solicitud GET a la urlTiempoActual para comprobar que comunica.
        responseActual = requests.get(urlTiempoActual)
        if responseActual.status_code == 200:
            return responseActual.json()
        else:
            print(
                f"Error al realizar la solicitud al intentar obtener los datos del tiempo Actual. Código de estado: {responseActual.status_code}"
            )
    # Si hay algún otro error cualquiera que no podemos controlar, salta la excepción.
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")


def obtenerJsonTiempoEn5Dias(lugar):
    urlTiempo5Dias = f"https://api.openweathermap.org/data/2.5/forecast?q={lugar}&units=metric&appid=ddccd66e42b270c765e7ea196e4e220c"
    try:
        # Realiza la solicitud GET a la urlTiempoActual para comprobar que comunica.
        response5Dias = requests.get(urlTiempo5Dias)
        if response5Dias.status_code == 200:
            return response5Dias.json()
        else:
            print(
                f"Error al realizar la solicitud al intentar obtener los datos del tiempo en 5 Días Código de estado: {response5Dias.status_code}"
            )
    # Si hay algún otro error cualquiera que no podemos controlar, salta la excepción.
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")


def opcion1(datosClimaActual):
    print("--------------------Opción1-------------------- \n")
    # Cargamos en variables desde el json todos los datos que vamos a necesitar
    tempActual = datosClimaActual["main"]["temp"]
    tempMax = datosClimaActual["main"]["temp_max"]
    tempMin = datosClimaActual["main"]["temp_min"]
    velViento = datosClimaActual["wind"]["speed"]
    nubes = datosClimaActual["clouds"]["all"]
    sensTermica = datosClimaActual["main"]["feels_like"]

    # Condiciones para saber si está nublado o no
    nubosidad = comprobarNubosidad(nubes)

    print(f"La temperatura actual en {lugarConsultado} es de : {tempActual} ºC")
    print(f"La sensación térmica es de : {sensTermica} ºC")
    print(f"La velocidad del viento es de : {velViento} KM/h")
    print(f"El nivel de nubes es de : {nubes} %, por lo tanto está {nubosidad}")
    print("--------------------------------------------")


def opcion2(datosClima5Dias):
    print("--------------------Opción2--------------------")
    # bucle for tradicional para usar el range y poder iterar en los 4 días siguientes
    for i in range(1, 5):
        fechaAProcesar = fechaProximosDiasString(datetime.now(), i)
        maxTemp = obtenerTemperaturaMaximaDia(fechaAProcesar)
        minTemp = obtenerTemperaturaMinimaDia(fechaAProcesar)
        print(f"La temperatura máxima para {fechaAProcesar} es de {maxTemp} ºC")
        print(f"La temperatura mínima para {fechaAProcesar} es de {minTemp} ºC\n")
    print("--------------------------------------------")


def fechaProximosDiasString(fecha, dias):
    fechaActual = datetime.now()
    fechaDiaDeseado = fechaActual + timedelta(days=dias)
    return fechaDiaDeseado.strftime(
        "%Y-%m-%d"
    )  # Lo devuelvo en ese formato para que se pueda comparar con el json que nos devuelve la api.


def opcion3(datosClima5Dias):
    print("--------------------Opción3--------------------")
    print(
        "En esta opción, indícame un día \n(como mínimo un día después de hoy y como máximo 4 días después de hoy) y una hora"
    )

    # Busco el límite de días.
    diaHoy = datetime.now().strftime("%Y-%m-%d").split("-")[2]
    limiteDia = fechaProximosDiasString(datetime.now(), 4).split("-")[2]
    # Ahora, pido al usuario el día que quiere dentro de los límites del JSON
    # Tiene que elegir un día entre el de hoy y rangoDias
    diaDeseado = int(
        input(
            f"Introduce un día teniendo en cuenta que hoy es {diaHoy} y el límite es {limiteDia}:"
        )
    )
    while diaDeseado not in range(int(diaHoy), int(limiteDia) + 1):
        print("El día introducido no está dentro del rango de los 4 días siguientes")
        diaDeseado = int(
            input(
                f"Introduce un día teniendo en cuenta que hoy es {diaHoy} y el límite es {limiteDia}:"
            )
        )
    print(f"El día deseado es {diaDeseado}")
    # Ahora, voy a pedir la hora
    horaDeseada = int(input("Introduce una hora: (00, 03, 06, 09, 12, 15, 18, 21): "))
    print(f"La hora deseada es {horaDeseada}")
    while horaDeseada not in range(
        0, 24, 3
    ):  # El tercer parámetro del range es el salto que dará, en este caso de 3 en 3
        print("La hora introducida no es múltiplo de 3")
        horaDeseada = int(
            input("Introduce una hora: (00, 03, 06, 09, 12, 15, 18, 21): ")
        )
    horaDeseada = str(horaDeseada).zfill(2)  # Con esto añado un 0 a la izquierda

    # Voy a buscar esa fecha y a mostrar sus características
    for item in datosClima5Dias["list"]:
        itemDia = item["dt_txt"].split(" ")[0].split("-")[2]

        itemHora = item["dt_txt"].split(" ")[1].split(":")[0]
        # print(
        #    f"El día del item es {itemDia}, y el día deseado es {diaDeseado}, la hora del item es {itemHora}, y la hora deseada es {horaDeseada}"
        # )
        if str(itemDia) == str(diaDeseado) and str(itemHora) == str(horaDeseada):
            temp = item["main"]["temp"]
            tempMax = item["main"]["temp_max"]
            tempMin = item["main"]["temp_min"]
            velViento = item["wind"]["speed"]
            nubes = item["clouds"]["all"]
            sensTermica = item["main"]["feels_like"]
            nubosidad = comprobarNubosidad(nubes)

            print(f"Tiempo para el día {diaDeseado} a las {horaDeseada}:")
            print(f"La temperatura será de : {temp} ºC")
            print(f"La sensación térmica será de : {sensTermica} ºC")
            print(f"La velocidad del viento será de : {velViento} KM/h")
            print(
                f"El nivel de nubes es de : {nubes} %, por lo tanto estará {nubosidad}"
            )


def comprobarNubosidad(nubes):
    if 0 < nubes < 50:
        nubosidad = "algo nublado"
    elif nubes >= 50:
        nubosidad = "muy nublado"
    else:
        nubosidad = "despejado de nubes"
    return nubosidad


print("Bienvenido a tu meteorólogo de confianza")
# Declaramos variables globales
lugarConsultado, datosClimaActual, datosClima5Dias = obtener_datos_clima()

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
            opcion3(datosClima5Dias)
        elif opcion == 4:
            print("--------------------Opción4--------------------")
            lugarConsultado, datosClimaActual, datosClima5Dias = obtener_datos_clima()
            print("--------------------------------------------")
        elif opcion == 5:
            print("¡Que tenga un buen día!")
            print("Cerrando el programa...")
            salir = True
    else:
        print("Opción incorrecta, elige una opción del 1 al 5.")
        print("Volviendo al menú...")
