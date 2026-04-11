import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtCore, QtWidgets
import serial
import sys

# --- CONFIGURATION ---
TAILLE_GRILLE = 50
PORT_ARDUINO = 'COM4'
VITESSE = 115200

class Visualiseur3D:
    def __init__(self, taille=50):
        self.taille = taille
        
        # 1. Configuration de l'application Qt
        self.app = QtWidgets.QApplication(sys.argv)
        self.view = gl.GLViewWidget()
        self.view.setWindowTitle('Visualisation 3D Temps Réel (PyQtGraph)')
        self.view.setCameraPosition(distance=80)
        self.view.show()

        # 2. Création de la surface initiale
        # On initialise Z avec des zéros
        self.Z = np.zeros((self.taille, self.taille))
        
        # Création de l'objet Surface
        # shader='heightColor' permet d'avoir des couleurs liées à la hauteur (comme viridis)
        self.surface = gl.GLSurfacePlotItem(
            z=self.Z, 
            shader='heightColor', 
            computeNormals=False, 
            smooth=False
        )
        
        # On scale la surface pour qu'elle soit centrée et visible
        self.surface.scale(1, 1, 1) 
        self.surface.translate(-self.taille/2, -self.taille/2, 0)
        self.view.addItem(self.surface)

        # 3. Connexion Série
        try:
            self.ser = serial.Serial(PORT_ARDUINO, VITESSE, timeout=0.01)
            print(f"Connecté sur {PORT_ARDUINO}")
        except Exception as e:
            print(f"Erreur port série: {e}")
            sys.exit()

        # 4. Timer pour la mise à jour (équivalent FuncAnimation)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(10)  # 10ms = 100 FPS théoriques

    def update_data(self, ligne, colonne, hauteur):
        """Met à jour un bloc de la matrice Z"""
        X_BLOC = 3
        l_start = int(max(0, min(ligne - X_BLOC//2, self.taille - X_BLOC)))
        c_start = int(max(0, min(colonne - X_BLOC//2, self.taille - X_BLOC)))
        
        # Mise à jour rapide via NumPy
        self.Z[l_start:l_start+X_BLOC, c_start:c_start+X_BLOC] = hauteur

    def update(self):
        """Lecture série et rafraîchissement graphique"""
        if self.ser.in_waiting > 0:
            try:
                line = self.ser.readline().decode('utf-8').rstrip()
                vals = list(map(float, line.split(",")))
                
                if len(vals) >= 3:
                    h, x, y = vals[0], int(vals[1]), int(vals[2])
                    
                    # Mise à jour de la matrice Z
                    self.update_data(x, y, h)
                    
                    # Injection des nouvelles données dans l'objet surface
                    # C'est ici que PyQtGraph est très performant
                    self.surface.setData(z=self.Z)
                    
            except Exception as e:
                print(f"Erreur : {e}")

    def run(self):
        # Lancement de la boucle d'événements Qt
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtWidgets.QApplication.instance().exec()

# --- MAIN ---
if __name__ == "__main__":
    visu = Visualiseur3D(TAILLE_GRILLE)
    visu.run()