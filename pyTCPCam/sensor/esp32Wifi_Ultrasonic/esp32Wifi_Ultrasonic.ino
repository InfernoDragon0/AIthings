#include <WiFi.h>
#include "time.h"

int TRIG_PIN = 26, ECHO_PIN = 34, LED = 27;

#define SOUND_SPEED 0.034

int i;
long duration;
float distanceCm;
String state = "0";
WiFiClient client;

struct tm timeinfo;
time_t now;
const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = 0;
const int   daylightOffset_sec = 3600;

const char* ssid = "AlienMesh";                   // Change this to your network SSID
const char* password = "WinBig@0101";             // Change this to your network password
const uint16_t port = 2004;
const char * host = "192.168.1.209";              // Change this to your host ip

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

  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
}

void loop() {
  getLocalTime(&timeinfo);
  getDistance();

  if(distanceCm < 80) {
    //Serial.println(distanceCm);
    state = "1";
    digitalWrite(LED, HIGH);
  }
  else {
    state = "0";
    digitalWrite(LED, LOW);
  }

  if (!client.connect(host, port)) {
    //Serial.println("Connection to host failed");
    return;
  }
  
  String parsedData = parseValue(state);
  client.print(parsedData);
  client.stop();

  //Serial.println(parsedData);

  delay(300);
}

void getDistance() {
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  duration = pulseIn(ECHO_PIN, HIGH);
  
  distanceCm = duration * SOUND_SPEED / 2;
}

String parseValue(String value) {
  String data = "{'py/object': 'data.SensorInference', 'packetType': 'Sensor', 'inferredData': [{'name': 'ultrasonic', 'value': '" + value + "'}], 'timestamp': " + time(&now) + "}";
  return data;
}
