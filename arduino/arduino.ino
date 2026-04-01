#include <SoftwareSerial.h>

const int trigPin1 = 10; // Trigger (emission)
const int echoPin1 = 9; // Echo (réception)
const int trigPin2 = 12; // Trigger (emission)
const int echoPin2 = 11; // Echo (réception)


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

  pinMode(trigPin1, OUTPUT); // Configuration du port du Trigger comme une SORTIE
  pinMode(echoPin1, INPUT); // Configuration du port de l'Echo comme une ENTREE
  pinMode(trigPin2, OUTPUT); // Configuration du port du Trigger comme une SORTIE
  pinMode(echoPin2, INPUT); // Configuration du port de l'Echo comme une ENTREE

  Serial.println("--- Setup OK ---");


}




void loop() {
  delay(100);
  if (tfLuna.available() >= 9) {
    if (tfLuna.read() == 0x59) {
      if (tfLuna.peek() == 0x59) {
        tfLuna.read(); // Consomme le deuxième 0x59
        uint8_t low = tfLuna.read();
        uint8_t high = tfLuna.read();
        int dist = low + (high << 8);
        for(int i=0; i<5; i++) tfLuna.read(); // Vide la trame


      

        // Filtre les valeurs aberrantes
        if (dist > 1 && dist < 5000) {
          digitalWrite(trigPin1, LOW);
          delayMicroseconds(5);
          digitalWrite(trigPin1, HIGH);
          delayMicroseconds(10);
          digitalWrite(trigPin1, LOW);


          // Écoute de l'écho
          duree1 = pulseIn(echoPin1, HIGH);


          digitalWrite(trigPin2, LOW);
          delayMicroseconds(5);
          digitalWrite(trigPin2, HIGH);
          delayMicroseconds(10);
          digitalWrite(trigPin2, LOW);


          // Écoute de l'écho
          duree2 = pulseIn(echoPin2, HIGH);
          // Si c'est la première valeur valide, on calibre
          distance1 = duree1*0.034/2;
          distance2 = duree2*0.034/2;
          
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
