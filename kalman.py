import collections
import numpy as np

from constante import *

class FiltreInter:
    def __init__(self, memoire = 5):
        self.memoire = memoire
        self.valeurs = collections.deque(maxlen = memoire)


    def filtrer(self, nouvelle_valeur):
        self.valeurs.append(nouvelle_valeur)
        return np.median(self.valeurs)

class FiltreKalman:
    def __init__(self, position, incertitude, q, r):
        """
        position : Position initiale estimée
        incertitude : Erreur initiale estimée (incertitude de départ)
        q      : Bruit du modèle (Confiance en la physique. Plus Q est grand, plus le filtre réagit vite, mais filtre moins)
        r      : Bruit de mesure (Confiance au capteur. Plus R est grand, plus on lisse, mais on ajoute de la latence)
        """
        self.position = position
        self.incertitude = incertitude
        self.q = q
        self.r = r


    def mettre_a_jour(self, mesure):
        # 1. Étape de Prédiction (on suppose une vitesse constante à court terme)
        prediction = self.r + self.q


        # 2. Étape de Correction (Calcul du gain de Kalman)
        k = prediction / (prediction + self.r)
       
        # Mise à jour de l'estimation avec la nouvelle mesure
        self.position = self.position + k * (mesure - self.position)
       
        # Mise à jour de l'incertitude
        self.incertitude = (1 - k) * prediction


        return self.position

def filtrage_mesure(incertitude, q, r, mesure):

    filtre_inter = FiltreInter(len(mesure))

    kalman = FiltreKalman(position=0.0, incertitude=incertitude, q=q, r=r)

    for i in range(len(mesure)):
        valeur_brut = mesure[i]
        valeur_filtre_inter = filtre_inter.filtrer(valeur_brut)
        valeur_filtre_kalman= kalman.mettre_a_jour(valeur_filtre_inter)
       
    return valeur_filtre_kalman



def filtrage_kalman(memoire_coords:collections.deque):
    mesure_x = [coord[1] for coord in memoire_coords]
    mesure_y = [coord[2] for coord in memoire_coords]
    mesure_z = [coord[0] for coord in memoire_coords]

    x_filtree = int(filtrage_mesure(INCERTITUDE, Q, R, mesure_x))
    y_filtree = int(filtrage_mesure(INCERTITUDE, Q, R, mesure_y))
    # z_filtree = memoire_coords[-1][0]  # On ne filtre pas z, on le retourne tel quel
    z_filtree = int(filtrage_mesure(INCERTITUDE, Q, R, mesure_z))

    return (z_filtree, x_filtree, y_filtree)