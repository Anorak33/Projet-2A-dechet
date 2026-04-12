"""Module de filtrage de Kalman
   Considerant le fait que nous recréons un nouveau filtre de Kalman à chaque itération, ce module pourrait être optimisé.
   Pour autant, il ne cause pas de problème de performance, et est plus simple d'utilisation, nous le conservons donc tel quel.
"""

import collections
import numpy as np

from constante import *

class FiltreInter:
    """Filtre intermédiaire pour lisser les mesures avant de les passer au Kalman. Utilise la médianne des valeurs.
    """
    def __init__(self, memoire:int):
        """Setup du filtre intermédiaire

        Args:
            memoire (int): Nombre de mesures à conserver pour le filtrage intermédiaire
        """
        self.valeurs:collections.deque = collections.deque(maxlen = memoire)


    def filtrer(self, nouvelle_valeur:float)->float:
        """Filtre la nouvelle valeur en utilisant la médianne des valeurs conservées

        Args:
            nouvelle_valeur (float): La nouvelle mesure à filtrer

        Returns:
            float: La valeur filtrée
        """
        self.valeurs.append(nouvelle_valeur)
        return float(np.mean(self.valeurs))

class FiltreKalman:
    """Filtre de Kalman pour estimer la position à partir des mesures filtrées par le filtre intermédiaire.
    """
    def __init__(self, position:float, incertitude:float, q:float, r:float):
        """Setup du filtre de Kalman

        Args:
            position (float): La position initiale estimée
            incertitude (float): L'incertitude initiale
            q (float): Confiance de processus
            r (float): Confiance de mesure
        """
        self.position:float = position
        self.incertitude:float = incertitude
        self.q:float = q
        self.r:float = r


    def mettre_a_jour(self, mesure:float)->float:
        """Met à jour l'estimation avec la nouvelle mesure

        Args:
            mesure (float): La nouvelle mesure

        Returns:
            float: La valeur estimée
        """
        # 1. Étape de Prédiction (on suppose une vitesse constante à court terme)
        prediction:float = self.incertitude + self.q
        # 2. Étape de Correction (Calcul du gain de Kalman)
        k:float = prediction / (prediction + self.r)
        # Mise à jour de l'estimation avec la nouvelle mesure
        self.position = self.position + k * (mesure - self.position)
        # Mise à jour de l'incertitude
        self.incertitude = (1 - k) * prediction

        return self.position

def filtrage_mesure(incertitude:float, q:float, r:float, liste_mesure:list)->float:
    """filtre la mesure en utilisant le filtre de Kalman

    Args:
        incertitude (float): L'incertitude initiale
        q (float): Confiance de processus
        r (float): Confiance de mesure
        liste_mesure (list): La liste des mesures à filtrer

    Returns:
        float: La valeur filtrée
    """

    filtre_inter:FiltreInter = FiltreInter(len(liste_mesure))

    kalman:FiltreKalman = FiltreKalman(position=0.0, incertitude=incertitude, q=q, r=r)

    for i in range(len(liste_mesure)):
        valeur_brut:float = liste_mesure[i]
        valeur_filtre_inter:float = filtre_inter.filtrer(valeur_brut)
        valeur_filtre_kalman:float = kalman.mettre_a_jour(valeur_filtre_inter)
       
    return valeur_filtre_kalman



def filtrage_kalman(memoire_coords:collections.deque)->tuple:
    """Filtre les coordonnées en utilisant le filtre de Kalman

    Args:
        memoire_coords (collections.deque): La mémoire des coordonnées à filtrer, doit contenir des tuples (z, x, y)

    Returns:
        tuple: Les coordonnées filtrées (z, x, y)
    """
    mesure_x:list = [coord[1] for coord in memoire_coords]
    mesure_y:list = [coord[2] for coord in memoire_coords]
    mesure_z:list = [coord[0] for coord in memoire_coords]

    x_filtree:int = int(filtrage_mesure(INCERTITUDE, Q, R, mesure_x))
    y_filtree:int = int(filtrage_mesure(INCERTITUDE, Q, R, mesure_y))
    z_filtree:int = int(filtrage_mesure(INCERTITUDE, Q, R, mesure_z))

    return (z_filtree, x_filtree, y_filtree)