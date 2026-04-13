"""Module d'affichage console raffiné, qui affiche les coordonnées de manière plus explicite que le module d'affichage console basique."""

def affichage(coords:tuple)->None:
    """Affichage descriptif en console des coordonnées.

    Args:
        coords (tuple): coordonnées à afficher, sous la forme (z,x,y)
    """
    print(f"Coordonnées filtrées: distance du déchet = {coords[0]}, x = {coords[1]}, y = {coords[2]}")

if __name__ == "affichages.affichage_console_raffine":
    #SETUP
    print("Affichage console raffiné sélectionné.")

    