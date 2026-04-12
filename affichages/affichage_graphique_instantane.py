"""Module d'affichage graphique instantané des coordonnées mesurées par le LiDAR.
Il affiche un point sur un canvas en fonction des coordonnées fournies, avec une couleur qui dépend de la hauteur mesurée"""

from tkinter import Canvas
import tkinter as tk

def affichage(coords:tuple)->None:
    """Affiche un point sur un canvas en fonction des coordonnées fournies.

    Args:
        coords (tuple): Les coordonnées à afficher, sous la forme (z, x, y).

    Raises:
        RuntimeError: Si l'application graphique a été fermée.
    """
    try:
        x_effectif: int = coords[1]*COEFF_AGRANDISSEMENT
        y_effectif: int = TAILLE_Y_BAC*COEFF_AGRANDISSEMENT-coords[2]*COEFF_AGRANDISSEMENT
        canvas.coords(point, y_effectif - RAYON_POINT, x_effectif - RAYON_POINT, y_effectif + RAYON_POINT, x_effectif + RAYON_POINT)
        canvas.itemconfig(point, fill=couleur_depuis_hauteur(coords[0]))
        root.update()
    except Exception as e:
        if repr(e) == "TclError('invalid command name \".!canvas\"')":
            raise RuntimeError ("\nL'application graphique a été fermée. Arrêt du programme...")
        print(f"Erreur lors de l'affichage : {e}")


if __name__ == "affichages.affichage_graphique_instantane":
    #SETUP
    from constante import *
    from affichages.couleur import couleur_depuis_hauteur

    print("Affichage graphique instantané sélectionné.")
    
    root:tk.Tk = tk.Tk()
    root.title("Dynamic Point Grid")

    canvas:Canvas = Canvas(root, width=TAILLE_Y_BAC*COEFF_AGRANDISSEMENT, height=TAILLE_X_BAC*COEFF_AGRANDISSEMENT, bg='white')
    canvas.pack()

    # Dessine une grille de carré de 5cm x 5cm
    for i in range(0, max(TAILLE_Y_BAC, TAILLE_X_BAC)*COEFF_AGRANDISSEMENT, 5*COEFF_AGRANDISSEMENT):
        canvas.create_line(i, 0, i, max(TAILLE_Y_BAC, TAILLE_X_BAC)*COEFF_AGRANDISSEMENT, fill='lightgray')
        canvas.create_line(0, i, max(TAILLE_Y_BAC, TAILLE_X_BAC)*COEFF_AGRANDISSEMENT, i, fill='lightgray')

    # Create a point
    point = canvas.create_oval(0, 0, RAYON_POINT*2, RAYON_POINT*2, fill=COULEUR_HAUTEUR_MAX)

