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
    memoire_coords:deque = setup_memoire(arduino)
    try:
        while True:
            coords:list|None = lecture_donnees(arduino)
            if coords is not None and coords[1] < TAILLE_X_BAC and coords[2] < TAILLE_Y_BAC:
                memoire_coords.append(coords)
                coords_filtree:tuple = filtrage_kalman(memoire_coords)
                if coords_filtree[1] > 100 or coords_filtree[2] > 100:
                    print(f"Coordonnées filtrées hors limites : {coords_filtree}")
                affichage(coords_filtree)
            time.sleep(0.01)           
    except KeyboardInterrupt:
        print(f"\nArrêt du programme...")
    except RuntimeError as e:
        print(e)
    except serial.SerialException as e:
        print(f"Erreur : {e}")
    finally:
        if arduino.is_open:
            arduino.close()


if __name__ == "__main__":
    print("Choisissez un mode d'affichage :")
    for i, affichage in enumerate(MODULES_AFFICHAGES):
        print(f"{i+1}. {affichage[0]}")
    choix_valide:bool = False
    while not choix_valide:
        try:
            choix:int = int(input("Entrez le numéro du mode d'affichage : "))
            if 1 <= choix <= len(MODULES_AFFICHAGES):
                module_affichage:ModuleType = import_module(f"affichages.{MODULES_AFFICHAGES[choix-1][1]}")
                choix_valide = True
            else:
                raise ValueError
        except ValueError:
            print(f"Veuillez entrer un numéro entre 1 et {len(MODULES_AFFICHAGES)}.")
        except ImportError as e:
            print(f"Module d'affichage mal implémenté : {e}")

    main(module_affichage.affichage)
    