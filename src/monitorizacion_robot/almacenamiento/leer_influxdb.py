from influxdb_client import InfluxDBClient


def leer_influx(config, tipo_datos):

    influx = config["influxdb"]
    tiempo_consulta = config["dashboard"]["rango_consulta"]

    # Elegir datos

    if tipo_datos == "telemetria":
        grupo_datos = influx["measurement_telemetria"]

    elif tipo_datos == "eventos":
        grupo_datos = influx["measurement_eventos"]

    else:
        return []

    # Consulta a InfluxDB

    consulta_influx = f'''
        from(bucket: "{influx["bucket"]}")
            |> range(start: {tiempo_consulta})
            |> filter(fn: (r) => r["_measurement"] == "{grupo_datos}")
            |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
            |> group()
            |> sort(columns: ["_time"], desc: true)
    '''

    cliente = InfluxDBClient(url = influx["url"], token = influx["token"], org = influx["org"])

    try:
        resultado = cliente.query_api().query(org = influx["org"], query = consulta_influx)

        datos = []

        # Preparar datos

        for tabla in resultado:

            for registro in tabla.records:

                dato = registro.values.copy()
                dato["fecha_hora"] = registro.get_time()

                datos.append(dato)

        return datos

    finally:
        cliente.close()