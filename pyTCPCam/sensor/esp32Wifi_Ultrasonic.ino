#include <WiFi.h>

int TRIG_PIN = 26, ECHO_PIN = 34, LED = 27;

#define SOUND_SPEED 0.034

long duration;
float distanceCm;
WiFiClient client;

const char* ssid = "AlienMesh";                   // Change this to your network SSID
const char* password = "WinBig@0101";             // Change this to your network password
const uint16_t port = 2004;
const char * host = "192.168.1.196";              // Change this to your host ip

void setup() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(LED, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  digitalWrite(TRIG_PIN, LOW);
  digitalWrite(LED, LOW);

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
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  
  duration = pulseIn(ECHO_PIN, HIGH);
  
  distanceCm = duration * SOUND_SPEED / 2;

  if(distanceCm < 20) {
    digitalWrite(LED, HIGH);
  }
  else {
    digitalWrite(LED, LOW);
  }

  if (!client.connect(host, port)) {
    Serial.println("Connection to host failed");
    return;
  }
    
  String parsedData = parseValue(String(distanceCm));
  client.print(parsedData);
  client.stop();

  delay(300);
}

String parseValue(String value) {
  String data = "{'py/object': 'data.Test.Test', 'packetType': 'Sensor', 'inferredData': [{'name': 'speech', 'value': '0.5'}, {'name': 'sound', 'value': '0.2'}, {'name': 'table', 'value': '0.1'}, {'name': 'footstep', 'value': '0.1'}, {'name': 'unknown', 'value': '0.1'}], 'timestamp': 1653474018.4336076, 'audioData': null}";
  return data;
}
