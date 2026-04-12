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
    # 1. Normalisation de x entre 0 et 1
    t:float = hauteur / HAUTEUR_LIDAR
    
    # 2. Calcul de la puissance 'p' pour que le changement se voie surtout sous B
    # On veut que pour x=B, le ratio soit encore élevé (ex: 0.8)
    # t_B = B/A. On cherche p tel que (B/A)^p = 0.8 (ou autre seuil de "douceur")
    # Ici, on peut fixer p empiriquement ou le calculer.
    # Plus p est grand, plus la transition est tardive (proche de 0).

    p:float = np.log(RATIO_COULEUR_EAU) / np.log((HAUTEUR_LIDAR - HAUTEUR_EAU) / HAUTEUR_LIDAR)
    
    # 3. Application de la courbe
    factor:float = np.power(t, p)
    
    # 4. Interpolation linéaire entre les deux couleurs
    c0:np.ndarray = np.array([int(COULEUR_HAUTEUR_0[i:i+2], 16) for i in range(1, 7, 2)])
    cA:np.ndarray = np.array([int(COULEUR_HAUTEUR_MAX[i:i+2], 16) for i in range(1, 7, 2)])
    
    # Résultat : (1-factor)*c0 + factor*cA
    result_color:np.ndarray = (1 - factor) * c0 + factor * cA
    return f'#{int(result_color[0]):02x}{int(result_color[1]):02x}{int(result_color[2]):02x}'