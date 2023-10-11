from datetime import datetime, timedelta

# Obtener la fecha de mañana a las 00:00
fecha_manana = datetime.now() + timedelta(days=1)
fecha_manana_medianoche = fecha_manana.replace(hour=0, minute=0, second=0)

# Formatear la fecha como un UNIX timestamp
fecha_unix_timestamp = int(fecha_manana_medianoche.timestamp())

print(fecha_unix_timestamp)
