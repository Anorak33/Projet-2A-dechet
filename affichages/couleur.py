"""Module de génération de couleurs en fonction de la hauteur mesurée par le LiDAR."""

import numpy as np

from constante import *

def couleur_depuis_hauteur(hauteur:int)->str:
    """Génère une couleur en fonction de la hauteur mesurée par le LiDAR, en utilisant une interpolation non linéaire pour que les changements soient plus visibles hors de l'eau.

    Args:
        hauteur (int): La hauteur mesurée par le LiDAR en cm, entre 0 et HAUTEUR_LIDAR.

    Returns:
        str: La couleur générée sous forme de chaîne hexadécimale.
    """
    #Normalisation de x entre 0 et 1
    t:float = hauteur / HAUTEUR_LIDAR
    
    #Calcul de la puissance 'p' pour que le changement de couleur se voie surtout pour des valeur inferieur à HAUTEUR_EAU (ie pour les déchets au dessus de l'eau)

    p:float = np.log(RATIO_COULEUR_EAU) / np.log((HAUTEUR_LIDAR - HAUTEUR_EAU) / HAUTEUR_LIDAR)
    
    #Application de la courbe
    factor:float = np.power(t, p)
    
    #Interpolation entre la couleur au fond de l'eau et la couleur au niveau du capteur
    c0:np.ndarray = np.array([int(COULEUR_HAUTEUR_0[i:i+2], 16) for i in range(1, 7, 2)]) #coefficient de couleur au niveau du capteur
    cA:np.ndarray = np.array([int(COULEUR_HAUTEUR_MAX[i:i+2], 16) for i in range(1, 7, 2)]) #coefficient de couleur au fond de l'eau
    
    #Résultat : (1-factor)*c0 + factor*cA
    result_color:np.ndarray = (1 - factor) * c0 + factor * cA

    #Conversion du résultat en chaîne hexadécimale
    return f'#{int(result_color[0]):02x}{int(result_color[1]):02x}{int(result_color[2]):02x}'