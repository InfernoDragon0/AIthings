#include <WiFi.h>
#include "time.h"

int TRIG_PIN = 26, ECHO_PIN = 34, LED = 27, current, benchmark, past, cnt = 0;

bool initSetup = false;

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

const char* ssid = "";                   // Change this to your network SSID
const char* password = "";             // Change this to your network password
const uint16_t port = 2004;
const char * host = "192.168.1.198";              // Change this to your host ip

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

  if(!initSetup) {
    digitalWrite(LED, HIGH);
    getDistance();
    past = distanceCm;
    while(true) {
      getDistance();
      current = distanceCm;
      //Serial.println(String(cnt) + ": " + String(past) + " " + String(current));
      if(current >= (past-5) && current <= (past+5)) {
        //past = distanceCm;
        cnt++;
      }
      else {
        //Serial.println("minus");
        cnt--;
      }
      if(cnt >= 5) {
        benchmark = past;
        break;
      }
      else if(cnt <= -5) {
        past = distanceCm;
        //Serial.println("reset");
        cnt = 0;
      }
      delay(100);
    }
    initSetup = true;
    digitalWrite(LED, LOW);
  }
  
  getDistance();

  if(distanceCm < benchmark) {
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
  String data = "{\"py/object\": \"data.SensorInference\", \"packetType\": \"Sensor\", \"inferredData\": [{\"name\": \"ultrasonic\", \"value\": " + value + "}], \"timestamp\": " + time(&now) + "}";
  return data;
}
