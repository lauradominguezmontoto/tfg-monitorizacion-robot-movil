#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <Wire.h>
#include <LittleFS.h>
#include <math.h>
#include "DFRobot_MICS.h"


// WiFi

const char* nombre_wifi = "NOMBRE_WIFI";
const char* contrasenha = "CONTRASENA_WIFI";

WiFiClient wifi;


// MQTT

const char* broker_mqtt = "IP_BROKER_MQTT";
const int puerto_mqtt = 1883;
const char* topic = "robot/sensores";

PubSubClient mqtt(wifi);


// Sensores

const int pin_dht = 4;
const int pin_ldr = 34;
const int pin_gas = 32;
const int pin_en_gas = 27;

DHT dht(pin_dht, DHT11);
DFRobot_MICS_ADC mics(pin_gas, pin_en_gas);


// IMU

const int pin_sda = 21;
const int pin_scl = 22;
const byte direccion_imu = 0x68;

float pitch_anterior = 0.0;
float roll_anterior = 0.0;
bool primera_lectura = true;


// LittleFS

const char* archivo_datos = "/datos.txt";


void guardarDato(String mensaje) {

  File archivo = LittleFS.open(archivo_datos, FILE_APPEND);

  if (archivo) {
    archivo.println(mensaje);
    archivo.close();
    Serial.println("Guardado en LittleFS");
  }
}


void enviarPendientes() {

  if (!LittleFS.exists(archivo_datos)) {
    return;
  }

  File archivo = LittleFS.open(archivo_datos, FILE_READ);

  if (!archivo) {
    return;
  }

  String pendientes = "";

  while (archivo.available()) {

    String mensaje = archivo.readStringUntil('\n');
    mensaje.trim();

    if (mensaje.length() == 0) {
      continue;
    }

    if (mqtt.connected() && mqtt.publish(topic, mensaje.c_str())) {
      Serial.println("Dato pendiente enviado");
    }

    else {
      pendientes += mensaje + "\n";
    }
  }

  archivo.close();

  File archivo_nuevo = LittleFS.open(archivo_datos, FILE_WRITE);

  if (archivo_nuevo) {
    archivo_nuevo.print(pendientes);
    archivo_nuevo.close();
  }
}


void setup() {

  Serial.begin(115200);

  LittleFS.begin(true);

  dht.begin();
  pinMode(pin_ldr, INPUT);

  mics.begin();

  if (mics.getPowerState() == SLEEP_MODE) {
    mics.wakeUpMode();
  }


  // IMU

  Wire.begin(pin_sda, pin_scl);

  Wire.beginTransmission(direccion_imu);
  Wire.write(0x6B);
  Wire.write(0x00);
  Wire.endTransmission();


  // WiFi

  WiFi.begin(nombre_wifi, contrasenha);


  // MQTT

  mqtt.setServer(broker_mqtt, puerto_mqtt);
}


void loop() {

  // WiFi

  if (WiFi.status() != WL_CONNECTED) {
    WiFi.reconnect();
  }


  // MQTT

  if (WiFi.status() == WL_CONNECTED && !mqtt.connected()) {

    if (mqtt.connect("esp32")) {
      Serial.println("MQTT conectado");

      // Primero se envían los datos pendientes
      enviarPendientes();
    }
  }

  if (mqtt.connected()) {
    mqtt.loop();
  }


  // DHT11

  float temperatura = dht.readTemperature();
  float humedad = dht.readHumidity();

  if (isnan(temperatura) || isnan(humedad)) {
    Serial.println("Error al leer el DHT11");
    delay(2000);
    return;
  }


  // LDR

  analogReadResolution(12);
  int luz = analogRead(pin_ldr);


  // Gas

  analogReadResolution(10);
  int gas = mics.getADCData(OX_MODE);


  // IMU

  Wire.beginTransmission(direccion_imu);
  Wire.write(0x3B);
  Wire.endTransmission(false);

  Wire.requestFrom(direccion_imu, (byte) 6);

  int16_t ax = 0;
  int16_t ay = 0;
  int16_t az = 0;

  if (Wire.available() == 6) {
    ax = (Wire.read() << 8) | Wire.read();
    ay = (Wire.read() << 8) | Wire.read();
    az = (Wire.read() << 8) | Wire.read();
  }

  else {
    Serial.println("Error al leer la IMU");
    delay(2000);
    return;
  }


  float x = ax / 16384.0;
  float y = ay / 16384.0;
  float z = az / 16384.0;

  float roll = atan2(y, z) * 180.0 / PI;
  float pitch = atan2(-x, sqrt(y * y + z * z)) * 180.0 / PI;


  // Posible caída

  bool posible_caida = false;

  if (!primera_lectura) {

    bool caida_pitch = abs(pitch) >= 85.0 && abs(pitch - pitch_anterior) >= 25.0;
    bool caida_roll = abs(roll) >= 85.0 && abs(roll - roll_anterior) >= 25.0;

    posible_caida = caida_pitch || caida_roll;
  }

  pitch_anterior = pitch;
  roll_anterior = roll;
  primera_lectura = false;


  // Crear JSON

  String mensaje = "{";
  mensaje += "\"temperatura\":" + String(temperatura, 1) + ",";
  mensaje += "\"humedad\":" + String(humedad, 1) + ",";
  mensaje += "\"luz\":" + String(luz) + ",";
  mensaje += "\"gas\":" + String(gas) + ",";
  mensaje += "\"pitch\":" + String(pitch, 2) + ",";
  mensaje += "\"roll\":" + String(roll, 2) + ",";
  mensaje += "\"posible_caida\":" + String(posible_caida ? "true" : "false");
  mensaje += "}";


  // Enviar muestra actual

  bool enviado = false;

  if (mqtt.connected()) {
    enviado = mqtt.publish(topic, mensaje.c_str());
  }

  if (enviado) {
    Serial.println("Mensaje MQTT enviado");
  }

  else {
    guardarDato(mensaje);
  }


  Serial.println(mensaje);

  delay(2000);
}