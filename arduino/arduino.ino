#include <SoftwareSerial.h>

const int trigPinX = 8; // Trigger (émission du signal)
const int echoPinX = 7; // Echo (réception du signal)
const int trigPinY = 10; // Trigger (emission)
const int echoPinY = 9; // Echo (réception)

const int offsetX = 1; // Décalage en cm entre le capteur ultrason X et le centre du LiDAR
const int offsetY = 1; // Décalage en cm entre le capteur ultrason Y et le centre du LiDAR

SoftwareSerial tfLuna(2, 3);


long dureeX; // durée de l'echo
long dureeY;
int distanceX;  // distance calculée en cm
int distanceY; 

void setup() {
  Serial.begin(115200);
  tfLuna.begin(115200);
  delay(1000); // On laisse 3 secondes pour bien stabiliser

  pinMode(trigPinX, OUTPUT); // Configuration du port du TriggerX comme une SORTIE
  pinMode(echoPinX, INPUT); // Configuration du port de l'EchoX comme une ENTREE
  pinMode(trigPinY, OUTPUT); // Configuration du port du TriggerY comme une SORTIE
  pinMode(echoPinY, INPUT); // Configuration du port de l'EchoY comme une ENTREE

  Serial.println("--- Setup OK ---");
}




void loop() {
  if (tfLuna.available() >= 9) {
    if (tfLuna.read() == 0x59) {
      if (tfLuna.peek() == 0x59) {
        tfLuna.read(); // Consomme le deuxième 0x59
        uint8_t low = tfLuna.read();
        uint8_t high = tfLuna.read();
        int distanceZ = low + (high << 8);
        for(int i=0; i<5; i++) tfLuna.read(); // Vide la trame


      

        // Filtre les valeurs aberrantes
        if (distanceZ > 0 && distanceZ < 255) {
          digitalWrite(trigPinX, LOW);  // Stabilisation du signal
          delayMicroseconds(5);         
          digitalWrite(trigPinX, HIGH); // Déclenchement de l'impulsion 
          delayMicroseconds(10);        // Durée d'impulsion requise pour le capteur
          digitalWrite(trigPinX, LOW);  // Arrêt de l'impulsion

          // Mesure le temps de retour (timeout de 50ms pour éviter de bloquer la carte)
          dureeX = pulseIn(echoPinX, HIGH, 50000);
          distanceX = dureeX*0.034/2 + offsetX; // d = v * t * 1/2, v la vitesse du son (0.034 m/ms) et 1/2 pour prendre en compte l'aller-retour

          digitalWrite(trigPinY, LOW);
          delayMicroseconds(5);
          digitalWrite(trigPinY, HIGH);
          delayMicroseconds(10);
          digitalWrite(trigPinY, LOW);

          dureeY = pulseIn(echoPinY, HIGH,50000);
          distanceY = dureeY*0.034/2 + offsetY;
          
        
          Serial.print(distanceZ);
          Serial.print(",");
          Serial.print(distanceX);
          Serial.print(",");
          Serial.println(distanceY);
          
        }
      }
    }
  }




  // Nettoyage rapide du tampon
  if (tfLuna.available() > 15) {
    while(tfLuna.available()) tfLuna.read();
  }
}
