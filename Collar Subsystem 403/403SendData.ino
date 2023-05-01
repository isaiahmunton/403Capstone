
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

#ifndef APSSID
#define APSSID "ESPap"
#define APPSK  "thereisnospoon"
#endif

String buff;
String app;
String coords;
String in;
int i = 0;

char byteArray[11520];



const char *ssid = "ESP_not_for_you!";
const char *password = "password!";

ESP8266WebServer server(80);

void handleRoot() {
  server.send(200, "text/html", "<h1>"+String("GPS: ") + String(coords)+String("Image: ") + String(byteArray)+"</h1>");
   //server.send(200, "text/html", "<h1>"+String("GPS: ") + String(coords)+"</h1>");
}

void uwu(){
  server.send(200, "text/html", "<h1>uwu</h1>");
}



void setup() {
  
  delay(1000);
  Serial.begin(9600);
  Serial.println();
  Serial.print("Configuring access point...");
  /* You can remove the password parameter if you want the AP to be open. */
  WiFi.softAP(ssid, password);

  IPAddress myIP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(myIP);
  server.on("/", handleRoot);
  server.on("/uwu", uwu);
  server.begin();
  Serial.println("HTTP server started");


}

void loop() {
  server.handleClient(); //updates the "client"
  //Serial.print(Serial.read());

  if (Serial.available()) { //checks if serial is available

    /*in = Serial.read();

    if(in == "GPS Time"){
      coords = Serial.read();
      */
    
    // Read the incoming byte and store it in a variable
    byte incomingByte = Serial.read(); //reads a byte, places into a varaible
    sprintf(byteArray + strlen(byteArray), "%02X", (const char*)incomingByte); //this command is important to append the bytes into a byte array

    
    // Print the incoming byte to the Serial Monitor
    Serial.println(incomingByte, HEX); //this is simply for printing out what I am recieving
    i++;
  }
  delay(1);
}
  



