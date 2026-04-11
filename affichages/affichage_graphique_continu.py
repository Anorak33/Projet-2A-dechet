import tkinter as tk
from constante import *

def affichage(coords):
    try:
        app.changer_couleur_case(*coords)
        app.update()
    except Exception as e:
        if repr(e) == "TclError('invalid command name \".!canvas\"')":
            raise RuntimeError ("\nL'application graphique a été fermée. Arrêt du programme...")
    
        print(f"Erreur lors de l'affichage : {e}")




if __name__ == "affichages.affichage_graphique_continu":
    #SETUP
    
    from affichages.couleur import couleur_depuis_hauteur
    print("Affichage graphique continu sélectionné.")
    class GrilleCouleur(tk.Tk):
        def __init__(self, lignes, colonnes, taille_case):
            super().__init__()
            self.title("Grille Tkinter - couleur par carreau")
            self.lignes = lignes
            self.colonnes = colonnes
            self.taille_case = taille_case
            self.couleur_initiale = couleur_depuis_hauteur(HAUTEUR_LIDAR)

            self.canvas = tk.Canvas(
                self,
                width=colonnes * taille_case,
                height=lignes * taille_case,
                bg="white",
                highlightthickness=0,
            )
            self.canvas.pack(padx=10, pady=10)

            self.rectangles = {}  # (ligne, colonne) -> id rectangle

            self._dessiner_grille()

        def _dessiner_grille(self):
            for i in range(self.lignes):
                for j in range(self.colonnes):
                    x1 = j * self.taille_case
                    y1 = i * self.taille_case
                    x2 = x1 + self.taille_case
                    y2 = y1 + self.taille_case

                    rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.couleur_initiale, outline="black")
                    self.rectangles[(i, j)] = rect_id

        def changer_couleur_case(self, hauteur, ligne, colonne):
            if not (0 <= ligne < self.lignes and 0 <= colonne < self.colonnes):
                return
            
            couleur = couleur_depuis_hauteur(hauteur)
            
            # Regroupe les cases par blocs de TAILLE_BLOCxTAILLE_BLOC 
            ligne = (int(ligne) // TAILLE_BLOC) * TAILLE_BLOC
            colonne = (int(colonne) // TAILLE_BLOC) * TAILLE_BLOC

            for dl in range(0, TAILLE_BLOC):
                for dc in range(0, TAILLE_BLOC):
                    li = ligne + dl
                    co = colonne + dc
                    if 0 <= li < self.lignes and 0 <= co < self.colonnes:
                        rid = self.rectangles[(li, co)]
                        self.canvas.itemconfig(rid, fill=couleur)

            rect_id = self.rectangles[(int(ligne), int(colonne))]
            self.canvas.itemconfig(rect_id, fill=couleur)
            print(f"Case ({ligne}, {colonne}) mise à jour avec hauteur {hauteur} -> couleur {couleur}")


    app = GrilleCouleur(lignes=NOMBRE_LIGNES, colonnes=NOMBRE_COLONNES, taille_case=TAILLE_CASE)