#Constante du monde réel
HAUTEUR_LIDAR  = 40 #En cm, la hauteur où est placé le capteur
HAUTEUR_EAU = 5 #En cm, la hauteur de l'eau dans le bac
TAILLE_X_BAC = 100 #En cm, la taille du bac en x
TAILLE_Y_BAC = 100 #En cm, la taille du bac en y


#Constante Affichage
MODULES_AFFICHAGES = [("Affichage console ([z,x,y])", "affichage_console"),
                    ("Affichage console raffiné", "affichage_console_raffine"), 
                    ("Affichage graphique instantané", "affichage_graphique_instantane"), 
                    ("Affichage graphique continu", "affichage_graphique_continu")]

#Constante Arduino
VITESSE = 115200
PORT_ARDUINO = 'COM10'  
TIMEOUT_CONFIGURATION = 10 #En secondes, le temps maximum pour recevoir la configuration de l'Arduino après le démarrage du programme

#Constante Filtrage de Kalman
TAILLE_MEMOIRE = 10
INCERTITUDE = 20
Q = 2
R = 50

#Constante Affichage Graphique Instantané


#Constante Affichage Graphique Continu
NOMBRE_LIGNES = 50
NOMBRE_COLONNES = 50
TAILLE_CASE = 10 #En pixels
TAILLE_BLOC = 2 #En nombre de cases, doit être un diviseur de NOMBRE_LIGNES et NOMBRE_COLONNES

#Constante Couleur
RATIO_COULEUR_EAU = 0.9 #Le ratio de la couleur à la hauteur d'eau par rapport à la couleur au fond de l'eau
COULEUR_HAUTEUR_0 = "#00FF00" #Vert pour 0 cm
COULEUR_HAUTEUR_MAX = "#0000FF" #Bleu pour la hauteur maximale du lidar