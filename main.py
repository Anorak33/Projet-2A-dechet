"""Programme principal du projet de détection des déchets."""

from types import ModuleType, FunctionType
from importlib import import_module

from constante import *
from lecture_serial import *
from kalman import filtrage_kalman



def main(affichage:FunctionType)->None:
    """Fonction principale du programme. Elle gère la connexion avec l'Arduino, la lecture des données, le filtrage de Kalman et l'affichage des coordonnées filtrées.

    Args:
        affichage (FunctionType): La fonction d'affichage à utiliser, choisie par l'utilisateur au lancement du programme. Elle doit prendre en argument un tuple de coordonnées (z,x,y).
    """
    arduino:serial.Serial = setup_arduino()
    filtres_inter, filtres_kalman = setup_filtres(arduino)
    try:
        while True:
            coords:list|None = lecture_donnees(arduino)
            # On vérifie que les coordonnées sont valides et dans les limites du bac avant de les ajouter à la mémoire et de les afficher
            if coords is not None and 0 < coords[1] < TAILLE_X_BAC and 0 < coords[2] < TAILLE_Y_BAC:
                coords_filtree:tuple = filtrage_kalman(filtres_inter,filtres_kalman,coords)
                affichage(coords_filtree)
            time.sleep(0.01)           
    #Arrêt en faisant ctrl+c dans le terminal
    except KeyboardInterrupt:
        print(f"\nArrêt du programme...")
    #Arrêt en fermant la fenêtre d'affichage
    except RuntimeError as e:
        print(e)
    except serial.SerialException as e:
        print(f"Erreur : {e}")
    finally:
        # On s'assure de fermer la connexion série avec l'Arduino à la fin du programme
        if arduino.is_open:
            arduino.close()


if __name__ == "__main__":
    #Menu de sélection du mode d'affichage
    print("Choisissez un mode d'affichage :")
    for i, affichage in enumerate(MODULES_AFFICHAGES):
        print(f"{i+1}. {affichage[0]}")
    choix_valide:bool = False
    while not choix_valide:
        try:
            choix:int = int(input("Entrez le numéro du mode d'affichage : "))
            if 1 <= choix <= len(MODULES_AFFICHAGES):
                # Import dynamique du module d'affichage choisi pour eviter de charger tous les modules inutiles en mémoire
                module_affichage:ModuleType = import_module(f"affichages.{MODULES_AFFICHAGES[choix-1][1]}")
                choix_valide = True
            else:
                raise ValueError
        except ValueError:
            print(f"Veuillez entrer un numéro entre 1 et {len(MODULES_AFFICHAGES)}.")
        except ImportError as e:
            print(f"Module d'affichage mal implémenté : {e}")

    main(module_affichage.affichage)
    