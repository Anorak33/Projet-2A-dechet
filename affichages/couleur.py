import numpy as np

from constante import *

def couleur_depuis_hauteur(hauteur):
    if hauteur < 10:
        return "#00FF00"  # Vert
    elif hauteur < 20:
        return "#FFFF00"  # Jaune
    elif hauteur < 30:
        return "#FFA500"  # Orange
    else:
        return "#FF0000"  # Rouge
    
def couleur_depuis_hauteur(hauteur):
    return f"#{(255-int(hauteur)*7)%256:02x}{(int(hauteur)*7)%256:02x}{(int(hauteur)*7*0)%256:02x}"

def couleur_depuis_hauteur(hauteur):
    

    """
    x: position actuelle (0 <= x <= A)
    A: limite supérieure
    B: point d'inflexion (entre 0 et A)
    color_0: tuple (R, G, B) pour x=0
    color_A: tuple (R, G, B) pour x=A
    """
    # 1. Normalisation de x entre 0 et 1
    t = hauteur / HAUTEUR_LIDAR
    
    # 2. Calcul de la puissance 'p' pour que le changement se voie surtout sous B
    # On veut que pour x=B, le ratio soit encore élevé (ex: 0.8)
    # t_B = B/A. On cherche p tel que (B/A)^p = 0.8 (ou autre seuil de "douceur")
    # Ici, on peut fixer p empiriquement ou le calculer.
    # Plus p est grand, plus la transition est tardive (proche de 0).

    p = np.log(RATIO_COULEUR_EAU) / np.log((HAUTEUR_LIDAR - HAUTEUR_EAU) / HAUTEUR_LIDAR)
    
    # 3. Application de la courbe
    factor = np.power(t, p)
    
    # 4. Interpolation linéaire entre les deux couleurs
    c0 = np.array([int(COULEUR_HAUTEUR_0[i:i+2], 16) for i in range(1, 7, 2)])
    cA = np.array([int(COULEUR_HAUTEUR_MAX[i:i+2], 16) for i in range(1, 7, 2)])
    
    # Résultat : (1-factor)*c0 + factor*cA
    result_color = (1 - factor) * c0 + factor * cA
    print(result_color)
    return f'#{int(result_color[0]):02x}{int(result_color[1]):02x}{int(result_color[2]):02x}'