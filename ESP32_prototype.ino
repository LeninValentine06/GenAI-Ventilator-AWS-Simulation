#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <DHT.h>

// WiFi and MQTT credentials
const char* ssid = "your-ssid";
const char* password = "your-password";
const char* mqttServer = "your-mqtt-server";
const int mqttPort = 8883;

// DHT11 settings
#define DHTPIN 23     // Pin D23 where the DHT11 is connected
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// MQTT client
WiFiClientSecure wifiClient;
PubSubClient client(wifiClient);

// Certificates
const char* AWS_ROOT_CA = /* Your AWS Root CA */;
const char* CLIENT_CERT = /* Your Client Certificate */;
const char* PRIVATE_KEY = /* Your Private Key */;

void setup() {
  Serial.begin(115200);
  dht.begin();

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Set certificates
  wifiClient.setCACert(AWS_ROOT_CA);
  wifiClient.setCertificate(CLIENT_CERT);
  wifiClient.setPrivateKey(PRIVATE_KEY);

  // Set MQTT server
  client.setServer(mqttServer, mqttPort);
  
  // Connect to MQTT broker
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
    if (client.connect("ESP32Client")) {
      Serial.println("Connected to MQTT broker");
    } else {
      Serial.print("Failed MQTT connection, rc=");
      Serial.print(client.state());
      delay(2000);
    }
  }
}

void loop() {
  // Read temperature data from DHT11 sensor
  float temperature = dht.readTemperature();  // Returns temperature in Celsius

  // Check if the reading is valid
  if (isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Create a JSON object
  StaticJsonDocument<200> doc;
  doc["TEMPERATURE"] = temperature;  // Store temperature in Celsius

  // Serialize the JSON data to a string
  char jsonBuffer[512];
  serializeJson(doc, jsonBuffer);

  // Publish the JSON string to the MQTT topic
  if (client.publish("sensor/temperature", jsonBuffer)) {
    Serial.println("Temperature data sent successfully:");
    Serial.println(jsonBuffer);
  } else {
    Serial.println("Failed to send temperature data");
  }

  // Wait for a few seconds before sending the next reading
  delay(5000);
}
