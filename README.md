# Módulo de registro independiente para el análisis de incidentes en robótica móvil

**Laura Domínguez Montoto**  
Trabajo Fin de Grado  
Universidade da Coruña — 2026

Código correspondiente al sistema desarrollado para el TFG.

## Instalación

```bash
pip install -r requirements.txt
```

## Configuración

La configuración general se encuentra en:

```text
config/config.json
```

Para ejecutar el proyecto es necesario configurar previamente la conexión con InfluxDB.

En el modo físico también deben indicarse en el firmware del ESP32 los datos de la red Wi-Fi y la dirección del broker MQTT.