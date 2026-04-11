#include <SoftwareSerial.h>

const int trigPinX = 8; // Trigger (émission du signal)
const int echoPinX = 7; // Echo (réception du signal)
const int trigPinY = 10; // Trigger (emission)
const int echoPinY = 9; // Echo (réception)

const int offsetX = 2; // Décalage en cm entre le capteur ultrason X et le centre du LiDAR
const int offsetY = 1; // Décalage en cm entre le capteur ultrason Y et le centre du LiDAR

SoftwareSerial tfLuna(2, 3);


long duree1; // durée de l'echo
long duree2;
int distance1;
int distance2; // distance


int distanceCalibree = 0;
const int seuil = 2; // On met un seuil en cm




void setup() {
  Serial.begin(115200);
  tfLuna.begin(115200);
  delay(1000); // On laisse 3 secondes pour bien stabiliser

  pinMode(trigPinX, OUTPUT); // Configuration du port du Trigger comme une SORTIE
  pinMode(echoPinX, INPUT); // Configuration du port de l'Echo comme une ENTREE
  pinMode(trigPinY, OUTPUT); // Configuration du port du Trigger comme une SORTIE
  pinMode(echoPinY, INPUT); // Configuration du port de l'Echo comme une ENTREE

  Serial.println("--- Setup OK ---");


}




void loop() {
  delay(5);
  if (tfLuna.available() >= 9) {
    if (tfLuna.read() == 0x59) {
      if (tfLuna.peek() == 0x59) {
        tfLuna.read(); // Consomme le deuxième 0x59
        uint8_t low = tfLuna.read();
        uint8_t high = tfLuna.read();
        int dist = low + (high << 8);
        for(int i=0; i<5; i++) tfLuna.read(); // Vide la trame


      

        // Filtre les valeurs aberrantes
        if (dist > 0 && dist < 256) {
          digitalWrite(trigPinX, LOW);  // Stabilisation du signal
          delayMicroseconds(5);         
          digitalWrite(trigPinX, HIGH); // Déclenchement de l'impulsion 
          delayMicroseconds(10);        // Durée d'impulsion requise pour le capteur
          digitalWrite(trigPinX, LOW);  // Arrêt de l'impulsion

          // Mesure le temps de retour (timeout de 30ms pour éviter de bloquer la carte)
          duree1 = pulseIn(echoPinX, HIGH, 50000);
          distance1 = duree1*0.034/2 + offsetX; // d = v * t * 1/2, v la vitesse du son (0.034 m/ms) et 1/2 pour prendre en compte l'aller-retour

          digitalWrite(trigPinY, LOW);
          delayMicroseconds(5);
          digitalWrite(trigPinY, HIGH);
          delayMicroseconds(10);
          digitalWrite(trigPinY, LOW);

          duree2 = pulseIn(echoPinY, HIGH,50000);
          distance2 = duree2*0.034/2 + offsetY;
          
          Serial.print(dist);
          Serial.print(",");
          Serial.print(distance1);
          Serial.print(",");
          Serial.println(distance2);
          
        }
      }
    }
  }




  // Nettoyage rapide du tampon
  if (tfLuna.available() > 15) {
    while(tfLuna.available()) tfLuna.read();
  }
}
