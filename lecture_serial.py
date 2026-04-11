import serial
import time
from collections import deque

from constante import *

def setup_arduino():
    print("\nSetting up the lecture environment...")
    arduino = serial.Serial(PORT_ARDUINO, VITESSE, timeout=1)
    print(f"Connexion établie sur le port {PORT_ARDUINO}")
    timeout = time.time() + TIMEOUT_CONFIGURATION  # Timeout pour la configuration
    while time.time() < timeout:
        if arduino.in_waiting > 0:
            donnee = arduino.readline().decode('utf-8').rstrip()
            if donnee == "--- Setup OK ---":
                print("Configuration arduino réussie, démarrage de la lecture des données...")
                return arduino
    raise TimeoutError("Configuration non reçue dans le délai imparti.")
    
def setup_memoire(arduino):
    memoire = deque(maxlen=TAILLE_MEMOIRE)
    while len(memoire) < TAILLE_MEMOIRE:
        coords = lecture_donnees(arduino)
        if coords is not None:
            memoire.append(coords)
    print("Initialisation de la mémoire terminée.")
    return memoire

def lecture_donnees(arduino):
    if arduino.in_waiting > 0:
        # Lecture de la ligne reçue
        donnee = arduino.readline().decode('utf-8').rstrip()
        return (list(map(int, donnee.split(","))))