"""Module d'affichage graphique continu d'une grille de colorée en fonction des données du LiDAR."""

import tkinter as tk

from constante import *

class GrilleCouleur(tk.Tk):
    def __init__(self, lignes:int, colonnes:int, taille_case:int):
        """Setup de la fenêtre principale avec une grille de rectangles colorés.
           Chaque rectangle représente un carré d'un centimètre du bac, et sa couleur dépend de la dernière hauteur mesurée par le LiDAR.

        Args:
            lignes (int):Le nombre de lignes de la grille
            colonnes (int):Le nombre de colonnes de la grille
            taille_case (int):La taille de chaque case en pixels
        """
        super().__init__()
        self.title("Grille Tkinter - couleur par carreau")
        self.lignes:int = lignes
        self.colonnes:int = colonnes
        self.taille_case:int = taille_case
        self.couleur_initiale:str = couleur_depuis_hauteur(HAUTEUR_LIDAR)

        #Création du canvas et dessin de la grille
        self.canvas:tk.Canvas = tk.Canvas(
            self,
            width=colonnes * taille_case,
            height=lignes * taille_case,
            bg=self.couleur_initiale,
            highlightthickness=0,
        )
        #On ajoute du padding autour du canvas pour que les cases soient bien séparees du bords de la fenêtre
        self.canvas.pack(padx=10, pady=10)

        self.rectangles:dict = {}  #(ligne, colonne) -> clef associée à un rectangle

        self._dessiner_grille()

    def _dessiner_grille(self)->None:
        """Dessine la grille de rectangles sur le canvas, en stockant les IDs de chaque rectangle pour pouvoir les modifier plus tard."""
        for i in range(self.lignes):
            for j in range(self.colonnes):
                x1:int = j * self.taille_case
                y1:int = i * self.taille_case
                x2:int = x1 + self.taille_case
                y2:int = y1 + self.taille_case

                rect_id:int = self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.couleur_initiale, outline="black")
                self.rectangles[(i, j)] = rect_id

    def changer_couleur_case(self, hauteur:int, ligne:int, colonne:int)->None:
        """Change la couleur d'une case de la grille en fonction de la hauteur mesurée.

        Args:
            hauteur (int):La hauteur mesurée par le LiDAR.
            ligne (int):La ligne de la case à modifier.
            colonne (int):La colonne de la case à modifier.
        """
        if not (0 <= ligne < self.lignes and 0 <= colonne < self.colonnes):
            return
        
        couleur:str = couleur_depuis_hauteur(hauteur)
        
        #On regroupe les cases par blocs de TAILLE_BLOCxTAILLE_BLOC 
        ligne = (ligne // TAILLE_BLOC) * TAILLE_BLOC
        colonne = ((TAILLE_Y_BAC-colonne) // TAILLE_BLOC) * TAILLE_BLOC 

        #On change la couleur de toutes les cases du bloc 
        for dl in range(0, TAILLE_BLOC):
            for dc in range(0, TAILLE_BLOC):
                li = ligne + dl
                co = colonne + dc
                if 0 <= li < self.lignes and 0 <= co < self.colonnes:
                    rid = self.rectangles[(li, co)]
                    self.canvas.itemconfig(rid, fill=couleur)

        #rect_id = self.rectangles[(int(ligne), int(colonne))]
        #self.canvas.itemconfig(rect_id, fill=couleur)
        print(f"Case ({ligne}, {colonne}) mise à jour avec hauteur {hauteur} -> couleur {couleur}")



def affichage(coords:tuple)->None:
    """Affiche un point sur une grille en fonction des coordonnées fournies. 
       La grille est mise à jour en continu, avec une couleur qui dépend de la hauteur mesurée.

    Args:
        coords (tuple):Les coordonnées à afficher, sous la forme (z, x, y).

    Raises:
        RuntimeError:Si l'application graphique a été fermée.
    """
    try:
        app.changer_couleur_case(*coords)
        app.update()
    except Exception as e:
        if repr(e) == "TclError('invalid command name \".!canvas\"')":
            raise RuntimeError ("\nL'application graphique a été fermée. Arrêt du programme...")
        print(f"Erreur lors de l'affichage :{e}")


if __name__ == "affichages.affichage_graphique_continu":
    #SETUP
    from affichages.couleur import couleur_depuis_hauteur

    print("Affichage graphique continu sélectionné.")

    app = GrilleCouleur(lignes=TAILLE_X_BAC, colonnes=TAILLE_Y_BAC, taille_case=TAILLE_CASE)