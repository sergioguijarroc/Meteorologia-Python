Este programa está basado en python, y es un meteorólogo que te permite consultar el clima actual y el pronóstico para los próximos 4 días en una ubicación específica. Al iniciar el programa, te pedirá que ingreses la ubicación que deseas consultar. Luego, te mostrará un menú con 5 opciones diferentes para elegir.

Requsitos previos
Necesitamos tener instalado en nuestro equipo Git, Docker y tener una cuenta en Github.

Para poder ejecutar el programa, primero tenemos que instalarlo en nuestro equipo.
Esta guía está pensada para ejecutarlo en linux, pero también se puede adaptar fácilmente a otros SO como Windows o Mac.

Una vez cumplamos los requisitos, seguimos los siguientes pasos:
1º Creamos una carpeta donde queramos instalar nuestro programa:
mkdir proyecto
Nos metemos dentro con :
cd proyecto
2º Una vez dentro, nos traemos el repositorio donde está alojado el programa en Github, para ello, ejecutamos el git 
git clone https://github.com/sergioguijarroc/Meteorologia-Python.git
(seguramente nos pida nuestros credenciales de nuestra cuenta personal de python).
3º Una vez clonado el repositorio, creamos la imagen de docker que vamos a necesitar con el siguiente comando docker build -t imagen-metereologo ./Meteorologia-Python
4º Cuando esté creada la imagen, ejecutamos directamente el programa con el comando docker run -it --name metereologo imagen-metereologo


Explicación de las diferentes funciones:

La primera opción te mostrará el clima actual en la ubicación que ingresaste.
La segunda opción te mostrará las temperaturas máximas y mínimas de los próximos 4 días.
La tercera opción te permitirá elegir un día (dentro del rango de los 4 días posteriores a la fecha de hoy) y una hora específica y te mostrará el pronóstico del clima para ese día y esa hora en concreto.
La cuarta opción te permitirá cambiar la ubicación que ingresaste al inicio del programa sin necesidad de reiniciar el programa.
La quinta opción te permitirá salir del programa. (Hasta que no selecciones esta opción no se acaba, se repite el menú)

El programa utiliza datos de dos apis de clima, una en tiempo real de una fuente en línea y otra del tiempo en los próximos días, en esta última, el programa utiliza funciones para redondear las horas ya que la api nos la devuelve de 3 en 3.