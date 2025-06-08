#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "LENOVO";
const char* password = "MendingTuru";

const char* serverURL = "http://192.168.1.4:85/esp32cam/hasil.php";

const int ledPin = 2;

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);  

  WiFi.begin(ssid, password);
  Serial.print("Menyambungkan ke WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Tersambung!");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverURL);
    int httpCode = http.GET();

    if (httpCode == 200) {
      String response = http.getString();
      response.trim();
      Serial.println("Respon dari server: [" + response + "]");

      if (response == "manusia") {
        digitalWrite(ledPin, HIGH); 
      } else if (response == "bukan_manusia") {
        digitalWrite(ledPin, LOW);  
      } else {
        Serial.println("Respon tidak dikenal. Matikan LED.");
        digitalWrite(ledPin, LOW);
      }
    } else {
      Serial.println("Gagal request ke server");
      digitalWrite(ledPin, LOW);
    }

    http.end();
  } else {
    Serial.println("WiFi terputus...");
    digitalWrite(ledPin, LOW);
  }

  delay(2000);
}
