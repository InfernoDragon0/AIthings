#include <WiFi.h>

int IN_PIN = 34, OUT_PIN = 26;

const char* ssid = "";
const char* password = "";
const uint16_t port = 2004;
const char * host = "192.168.2.197";

void setup() {
  pinMode (IN_PIN, INPUT);    // Connected to OUT pin on RCWL-0516 sensor
  pinMode (OUT_PIN, OUTPUT);  // Connected to external LED
  digitalWrite(OUT_PIN, LOW);

  Serial.begin(115200);
 
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("...");
  }
 
  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  WiFiClient client;
 
  if(digitalRead(IN_PIN) == HIGH) {
    digitalWrite(OUT_PIN, HIGH);

    while(digitalRead(IN_PIN) == HIGH) {
      if (!client.connect(host, port)) {
        Serial.println("Connection to host failed");
        delay(1000);
        return;
      }
    
      Serial.println("Connected to server successful!");
      String parsedData = parseValue("True");
      Serial.println("Parsed");
      client.print(parsedData);
      Serial.println("Disconnecting...");
      client.stop();

      delay(2000);
    }

    digitalWrite(OUT_PIN, LOW);
  }
  else {
    digitalWrite(OUT_PIN, LOW);
  }
}

String parseValue(String value) {
  String data = "{'py/object': 'data.microwave', 'packetType': 'Motion', 'MotionData': {'microwave_1': '" + value + "'}, 'timestamp': 1653474018.4336076}";

  return data;
}
