#include <WiFi.h>

int TRIG_PIN = 26, ECHO_PIN = 34, LED = 27;

#define SOUND_SPEED 0.034

long duration;
float distanceCm;
int cnt, i;

const char* ssid = "AlienMesh";       // Change this to your network SSID
const char* password = "";            // Change this to your network password
const uint16_t port = 2004;
const char * host = "192.168.1.195";  // Change this to your host ip

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
  WiFiClient client;

  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  
  duration = pulseIn(ECHO_PIN, HIGH);
  
  distanceCm = duration * SOUND_SPEED / 2;
  
  Serial.print("Distance: ");
  Serial.print(distanceCm);
  Serial.println(" cm");
 
  if(distanceCm < 20) {
    cnt = 0;
    for(i = 0; i < 5; i++) {
      digitalWrite(TRIG_PIN, HIGH);
      delayMicroseconds(10);
      digitalWrite(TRIG_PIN, LOW);
      
      duration = pulseIn(ECHO_PIN, HIGH);
      
      distanceCm = duration * SOUND_SPEED / 2;

      if(distanceCm < 20) {
        cnt++;
      }

      delay(10);
    }

    if(cnt == 5) {
      digitalWrite(LED, HIGH);

      if (!client.connect(host, port)) {
          Serial.println("Connection to host failed");
          delay(1000);
          return;
        }
      
      Serial.println("Connected to server successful!");
      String parsedData = parseValue(String(distanceCm));
      Serial.println("Parsed");
      client.print(parsedData);
      Serial.println("Disconnecting...");
      client.stop();
  
      while(distanceCm < 20) {
        digitalWrite(TRIG_PIN, HIGH);
        delayMicroseconds(10);
        digitalWrite(TRIG_PIN, LOW);
        
        duration = pulseIn(ECHO_PIN, HIGH);
        
        distanceCm = duration * SOUND_SPEED / 2;
      }
    }
  }
  else {
    digitalWrite(LED, LOW);
  }

  delay(100);
}

String parseValue(String value) {
  //String data = "{'py/object': 'data.ultrasonic', 'packetType': 'Distance', 'Distance': [{'Ultrasonic_1': '" + value + "'}], 'timestamp': 1653474018.4336076}";
  String data = "{'py/object': 'data.Test.Test', 'packetType': 'Sensor', 'inferredData': [{'name': 'speech', 'value': '0.5'}, {'name': 'sound', 'value': '0.2'}, {'name': 'table', 'value': '0.1'}, {'name': 'footstep', 'value': '0.1'}, {'name': 'unknown', 'value': '0.1'}], 'timestamp': 1653474018.4336076, 'audioData': null}";
  return data;
}
