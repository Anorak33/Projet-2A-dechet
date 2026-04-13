"""Fichier contenant les constantes utiles au fonctionnement des programmes"""

#*Constante du monde réel
HAUTEUR_LIDAR  = 40 #En cm, la hauteur où est placé le LiDAR
HAUTEUR_EAU = 5 #En cm, la hauteur de l'eau dans le bac
TAILLE_X_BAC = 50 #En cm, la taille du bac en x, il vaut mieux une valeur plus grande que la valeur réelle
TAILLE_Y_BAC = 30 #En cm, la taille du bac en y, idem


#*Constante Arduino
VITESSE = 115200 #En bauds, la vitesse de communication série avec l'Arduino. Doit être la même que celle configurée dans le code de l'Arduino
PORT_ARDUINO = 'COM10' #Le port série où est connecté l'Arduino, peut se voir dans l'Arduino IDE
TIMEOUT_CONFIGURATION = 10 #En secondes, le temps maximum pour recevoir la configuration de l'Arduino après le démarrage du programme

#*Constante Filtrage de Kalman
TAILLE_MEMOIRE = 15
INCERTITUDE = 0.0 #Incertitude initale du système
Q = 15.0 #Confiance au processus 
R = 3.0 #Confiance aux mesures

#*Constante Choix du module d'affichage
#Les modules d'affichage doivent être dans le dossier affichages et implémenter une fonction affichage(coords:tuple)->None
#Couples (nom affiché dans le menu de choix, nom du module d'affichage) :
MODULES_AFFICHAGES = [("Affichage console ([z,x,y])", "affichage_console"),
                    ("Affichage console raffiné", "affichage_console_raffine"), 
                    ("Affichage graphique instantané", "affichage_graphique_instantane"), 
                    ("Affichage graphique continu", "affichage_graphique_continu")]


#*Constante Affichage Graphique Instantané
COEFF_AGRANDISSEMENT = 20 #Coefficient d'agrandissement de la fenêtre
RAYON_POINT = 15 #En pixels, le rayon du point représentant les coordonnées filtrées

#*Constante Affichage Graphique Continu
TAILLE_CASE = 10 #En pixels
TAILLE_BLOC = 2 #En nombre de cases, doit être un diviseur de NOMBRE_LIGNES et NOMBRE_COLONNES

#*Constante Couleur
RATIO_COULEUR_EAU = 0.9 #Le ratio de la couleur à la hauteur d'eau par rapport à la couleur au fond de l'eau
COULEUR_HAUTEUR_0 = "#00FF00" #Couleur pour la hauteur 0, c'est à dire quand un déchet 'touche' le capteur 
COULEUR_HAUTEUR_MAX = "#0000FF" #Couleur pour la hauteur maximale de détection du lidar, c'est à dire quand il ne detecte rien

