"""Lecture des données d'une carte Arduino via une connexion série."""

import serial
import time
from collections import deque

from constante import *
from kalman import *

def setup_arduino()->serial.Serial:
    """Setup de la connexion série avec l'Arduino.

    Raises:
        TimeoutError: Si la configuration n'est pas reçue dans le délai imparti.

    Returns:
        serial.Serial: L'objet de connexion série configuré et prêt à être utilisé.
    """
    print("\nCréation de la connexion série...")
    arduino:serial.Serial = serial.Serial(PORT_ARDUINO, VITESSE, timeout=1)
    print(f"Connexion établie sur le port {PORT_ARDUINO}")
    timeout:float = time.time() + TIMEOUT_CONFIGURATION  # Timeout pour la configuration
    while time.time() < timeout:
        if arduino.in_waiting > 0:
            donnee:str = arduino.readline().decode('utf-8').rstrip()
            if donnee == "--- Setup OK ---":
                print("Configuration arduino réussie, démarrage de la lecture des données...")
                return arduino
    raise TimeoutError("Configuration non reçue dans le délai imparti.")
    
def setup_filtres(arduino:serial.Serial)->tuple:
    """On initialise les filtres pour éviter d'avoir des valeur fausses au démarrage du programme

    Args:
        arduino (serial.Serial): L'objet de connexion série avec l'Arduino.

    Returns:
        tuple: Les filtres intermédiaire et de Kalman pour les 3 coordonnées
    """
    filtres_inter:tuple = (FiltreInter(TAILLE_MEMOIRE), FiltreInter(TAILLE_MEMOIRE), FiltreInter(TAILLE_MEMOIRE))
    filtres_kalman:tuple = (FiltreKalman(0.0, INCERTITUDE, Q, R), FiltreKalman(0.0, INCERTITUDE, Q, R), FiltreKalman(0.0, INCERTITUDE, Q, R))

    i = 0
    while i < TAILLE_MEMOIRE*3: # On lit au moins 3 fois la taille de la mémoire pour être sûr d'avoir des valeurs stables
        coords:list|None = lecture_donnees(arduino)
        if coords is not None:
            filtrage_kalman(filtres_inter,filtres_kalman,coords)
            i += 1
    print("Initialisation des filtres terminée.")
    return filtres_inter, filtres_kalman

def lecture_donnees(arduino:serial.Serial)->list|None:
    """Lecture des données écrite sur la connexion série.

    Args:
        arduino (serial.Serial): L'objet de connexion série avec l'Arduino.

    Returns:
        list|None: La liste des coordonnées lues [z,x,y]. On préfère renvoyer None que des listes par défaut pour éviter, en cas de lag de la carte arduino, de remplire la mémoire de valeurs fausses.
    """
    if arduino.in_waiting > 0:
        # Lecture de la ligne reçue
        donnee:str = arduino.readline().decode('utf-8').rstrip()
        return list(map(int, donnee.split(",")))