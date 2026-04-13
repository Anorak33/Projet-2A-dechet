"""Module d'affichage des coordonnées brutes dans la console"""

def affichage(coords:tuple)->None:
    """Affichage des coordonées brutes.

    Args:
        coords (tuple): coordonnées à afficher, sous la forme (z,x,y)
    """
    print(coords)

if __name__ == "affichages.affichage_console":
    #SETUP
    print("Affichage console sélectionné.")