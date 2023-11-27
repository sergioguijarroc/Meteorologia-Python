import requests
import json
from datetime import datetime, timedelta
#App para consultar el tiempo
# Funciones necesarias
#Funciones con la obtención de datos del clima:
def obtenerJsonTiempoActual(lugar):
    urlTiempoActual = f"https://api.openweathermap.org/data/2.5/weather?q={lugar}&units=metric&appid=ddccd66e42b270c765e7ea196e4e220c"  # La url de la api con el lugar a consultar
    try:
        # Realiza la solicitud GET a la urlTiempoActual para comprobar que comunica.
        responseActual = requests.get(urlTiempoActual)
        if (
            responseActual.status_code == 200
        ):  # Si el código de estado es 200, se ha realizado correctamente la solicitud
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

#Funciones auxiliares:
def comprobarNubosidad(nubes):
    if 0 < nubes < 50:
        nubosidad = "algo nublado"
    elif nubes >= 50:
        nubosidad = "muy nublado"
    else:
        nubosidad = "despejado de nubes"
    return nubosidad

def fechaProximosDiasString(fecha, dias):
    fechaActual = datetime.now()
    fechaDiaDeseado = fechaActual + timedelta(
        days=dias
    )  # timedelta es una función que nos permite sumar días a una fecha
    return fechaDiaDeseado.strftime(
        "%Y-%m-%d"
    )  # Lo devuelvo en como String en ese formato para que se pueda comparar con el json que nos devuelve la api.

def redondearHora(hora):
    horaADevolver = hora
    if hora == 23:
        horaADevolver = 0
    elif hora % 3 == 1:  # Si el residuo es 1, le restamos 1 para redondear hacia abajo
        horaADevolver = hora - 1
    elif hora % 3 == 2:  # Si el residuo es 2, le sumamos 1 para redondear hacia arriba
        horaADevolver = hora + 1
    # Si el residuo es 0, no hacemos nada
    horaADevolver = str(horaADevolver).zfill(
        2
    )  # Si la hora es por ejemplo 3, le añadimos un 0 a la izquierda para que quede 03 para que lo lea bien el json
    return horaADevolver

#Opciones del menú:

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
        fechaAProcesar = fechaProximosDiasString(
            datetime.now(), i
        )  # Con esto, consigo el String de la fecha
        maxTemp = obtenerTemperaturaMaximaDia(fechaAProcesar)
        minTemp = obtenerTemperaturaMinimaDia(fechaAProcesar)
        print(f"\nLa temperatura máxima para {fechaAProcesar} es de {maxTemp} ºC")
        print(f"La temperatura mínima para {fechaAProcesar} es de {minTemp} ºC\n")
    print("--------------------------------------------")


def opcion3(datosClima5Dias):
    print("--------------------Opción3--------------------")
    print(
        "En esta opción, indícame un día y una hora\n(ten en cuenta que debe ser como mínimo un día después de hoy y como máximo 4 días después de hoy)"
    )

    # Busco el límite de días.
    diaHoy = fechaProximosDiasString(datetime.now(), 0).split("-")[2]
    limiteDia = fechaProximosDiasString(datetime.now(), 4).split("-")[
        2
    ]  # Con esto, obtengo el día límite de los 4 días siguientes
    # Ahora, pido al usuario el día que quiere dentro de los límites del JSON
    # Tiene que elegir un día entre el de hoy y rangoDias
    diaDeseado = int(
        input(
            f"Introduce un día teniendo en cuenta que hoy es {diaHoy} y el límite es {limiteDia}:"
        )
    )
    while diaDeseado not in range(
        int(diaHoy) + 1, int(limiteDia) + 1  # Entre mañana y el día límite
    ):  # El día de hoy se podría consultar, pero no tiene sentido ya que hay una opción para consultar el tiempo del día de hoy
        print(
            f"El día introducido no está dentro del rango de los 4 días de entre mañana y el día {limiteDia} "
        )
        diaDeseado = int(
            input(
                f"Introduce un día teniendo en cuenta que hoy es {diaHoy} y el límite es {limiteDia}:"
            )
        )
    print(f"El día deseado es {diaDeseado}")
    # Ahora, voy a pedir la hora
    if diaDeseado == int(
        limiteDia
    ):  # Si el día deseado es el último día, la hora máxima a consultar es 22
        print(
            f"El día {limiteDia} es el último día que se puede consultar, por lo tanto, la hora máxima a consultar es 22"
        )
        horaDeseada = int(input("Introduce una hora: (0-22)"))
        while horaDeseada not in range(0, 23):
            print("La hora introducida no es válida")
            horaDeseada = int(input("Introduce una hora: (entre 0-22): "))

    else:  # En cualquier otro caso, la hora máxima a consultar es 23
        horaDeseada = int(input("Introduce una hora: (0-23)"))
        while horaDeseada not in range(0, 24):
            print("La hora introducida no es válida")
            horaDeseada = int(input("Introduce una hora: (entre 0-23): "))
        if (
            horaDeseada == 23
        ):  # Si la hora introducida es 23, el día deseado será el del día siguiente
            diaDeseado = int(diaDeseado) + 1
            horaDeseada = 0
            print(
                "Te vamos a mostrar el tiempo para el día siguiente a las 00:00 horas"
            )  # Este comentario me parece necesario para la usabilidad del programa

    # Lo redondeamos para que lo entienda el json
    horaRedondeada = redondearHora(horaDeseada)
    # Voy a buscar esa fecha y a mostrar sus características
    for item in datosClima5Dias["list"]:
        itemDia = (
            item["dt_txt"].split(" ")[0].split("-")[2]
        )  # Con esto obtengo el día del item actual, y la divido en dos partes, la fecha y la hora, y me quedo con la fecha
        itemHora = (
            item["dt_txt"].split(" ")[1].split(":")[0]
        )  # Igual que antes, pero con la hora

        if str(itemDia) == str(diaDeseado) and str(itemHora) == str(horaRedondeada):
            temp = item["main"]["temp"]
            tempMax = item["main"]["temp_max"]
            tempMin = item["main"]["temp_min"]
            velViento = item["wind"]["speed"]
            nubes = item["clouds"]["all"]
            sensTermica = item["main"]["feels_like"]
            nubosidad = comprobarNubosidad(nubes)

            print(
                f"\nTiempo para el día {diaDeseado} a las {horaRedondeada}:00 horas: "
            )
            print(f"La temperatura será de : {temp} ºC")
            print(f"La sensación térmica será de : {sensTermica} ºC")
            print(f"La velocidad del viento será de : {velViento} KM/h")
            print(
                f"El nivel de nubes será de : {nubes} %, por lo tanto, estará {nubosidad}\n"
            )
#Funciones de configuración y entrada de datos:

def menu():
    print("\n--------------------Menu--------------------")
    print("1. Tiempo actual")
    print("2. Tiempo en los próximos 4 días")
    print("3. Tiempo en un día y hora concreta")
    print("4. Cambiar el lugar a consultar")
    print("5. Salir")
    print("--------------------------------------------")


def obtenerTemperaturaMaximaDia(fecha):
    maxTemp = (
        -200
    )  # Inicializo la variable a un valor muy bajo para que se pueda comparar con el primer item
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
    minTemp = 200  # Inicializo la variable a un valor muy alto para que se pueda comparar con el primer item
    minTempItemActual = 200

    for item in datosClima5Dias["list"]:
        fechaItemActual = item["dt_txt"].split(" ")[0]
        if fechaItemActual == fecha:
            minTempItemActual = item["main"]["temp_min"]
            if minTempItemActual < minTemp:
                minTemp = minTempItemActual
    return minTemp


def obtener_datos_clima():
    while True:  # Bucle infinito hasta que se introduzca un lugar válido que exista
        lugar = input(
            "Para empezar, dime cualquier lugar del mundo el cual quieres consultar: "
        )
        datosClimaActual = obtenerJsonTiempoActual(
            lugar
        )  # Llamo a la función para obtener los datos del tiempo actual
        datosClima5Dias = obtenerJsonTiempoEn5Dias(
            lugar
        )  # Llamo a la función para obtener los datos del tiempo en 5 días

        if (
            datosClimaActual is not None and datosClima5Dias is not None
        ):  # Si no son nulos, los devuelvo y así consigo salir del bucle
            return lugar, datosClimaActual, datosClima5Dias
        else:
            print("Lugar no encontrado. Introduce un lugar válido.")


# Inicio del programa
print("Bienvenido a tu meteorólogo de confianza")
# Declaramos variables globales
lugarConsultado, datosClimaActual, datosClima5Dias = obtener_datos_clima()

salir = False

while not salir:
    menu()
    opcion = int(
        input(f"Tienes seleccionado {lugarConsultado}, elige una opción del 1 al 5: ")
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
