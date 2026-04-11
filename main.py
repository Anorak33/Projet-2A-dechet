from collections import deque
from typing import Callable
from importlib import import_module

from constante import *
from lecture_serial import *
from kalman import filtrage_kalman



def main(affichage:Callable):
    arduino:serial.Serial = setup_arduino()
    memoire_coords = setup_memoire(arduino)
    try:
        while True:
            coords = lecture_donnees(arduino)
            if coords is not None:
                memoire_coords.append(coords)
                coords_filtree = filtrage_kalman(memoire_coords)
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
    choix_valide = False
    while not choix_valide:
        try:
            choix = int(input("Entrez le numéro du mode d'affichage : "))
            if 1 <= choix <= len(MODULES_AFFICHAGES):
                module_affichage = import_module(f"affichages.{MODULES_AFFICHAGES[choix-1][1]}")
                choix_valide = True
            else:
                raise ValueError
        except ValueError:
            print(f"Veuillez entrer un numéro entre 1 et {len(MODULES_AFFICHAGES)}.")
        except ImportError as e:
            print(f"Module d'affichage mal implémenté : {e}")

    main(module_affichage.affichage)
    