#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* serverUrl = "http://192.168.1.10:8000/sensor-data";
const char* deviceId = "ESP32-001";
const char* authToken = "CHANGE_ME";

#define DHTPIN 4
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  dht.begin();

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
}

void loop() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor");
    delay(2000);
    return;
  }

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    String payload = "{";
    payload += "\"device_id\":\"" + String(deviceId) + "\",";
    payload += "\"temperature\":" + String(temperature, 2) + ",";
    payload += "\"humidity\":" + String(humidity, 2) + "";
    payload += "}";

    int httpCode = http.POST(payload);
    Serial.printf("HTTP status: %d\n", httpCode);
    String response = http.getString();
    Serial.println(response);
    http.end();
  }

  delay(60000);
}
