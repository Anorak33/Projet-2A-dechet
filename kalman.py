"""Module du filtre de Kalman"""

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

def filtrage_mesure(filtre_inter:FiltreInter, filtre_kalman:FiltreKalman, incertitude:float, q:float, r:float, mesure:int)->float:
    """filtre la mesure en utilisant le filtre de Kalman

    Args:
        filtre_inter (FiltreInter): Le filtre intermédiaire
        filtre_kalman (FiltreKalman): Le filtre de Kalman
        incertitude (float): L'incertitude initiale
        q (float): Confiance de processus
        r (float): Confiance de mesure
        mesure (int): La mesure à filtrer

    Returns:
        float: La valeur filtrée
    """

    valeur_brut:float = float(mesure)
    valeur_filtre_inter:float = filtre_inter.filtrer(valeur_brut)
    valeur_filtre_kalman:float = filtre_kalman.mettre_a_jour(valeur_filtre_inter)

    return valeur_filtre_kalman



def filtrage_kalman(filtres_inter:tuple,filtres_kalman:tuple,coords:list)->tuple:
    """Filtre les coordonnées en utilisant le filtre de Kalman

    Args:
        coords (list): La coordonnée brute à filtrer (z, x, y)
        filtres_inter (tuple): Les filtres intermédiaires pour les 3 coordonnées
        filtres_kalman (tuple): Les filtres de Kalman pour les 3 coordonnées

    Returns:
        tuple: Les coordonnées filtrées (z, x, y)
    """
    

    x_filtree:int = int(filtrage_mesure(filtres_inter[1], filtres_kalman[1], INCERTITUDE, Q, R, coords[1])) 
    y_filtree:int = int(filtrage_mesure(filtres_inter[2], filtres_kalman[2], INCERTITUDE, Q, R, coords[2])) 
    z_filtree:int = int(filtrage_mesure(filtres_inter[0], filtres_kalman[0], INCERTITUDE, Q, R, coords[0]))

    return (z_filtree, x_filtree, y_filtree)