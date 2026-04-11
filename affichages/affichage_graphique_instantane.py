from tkinter import Canvas
import tkinter as tk

from constante import *

def affichage(coords):
    
    canvas.coords(point, coords[1]*6 - 15 +200, coords[2]*6 - 15 +200, coords[1]*6 + 15 +200, coords[2]*6  + 15 +200)
    print(f"Current Coordinates: {coords}")
    canvas.itemconfig(point, fill=couleur_depuis_hauteur(coords[0]))
    root.update()

if __name__ == "affichages.affichage_graphique_instantane":
    #SETUP
    from affichages.couleur import couleur_depuis_hauteur

    print("Affichage graphique instantané sélectionné.")
    
    root = tk.Tk()
    root.title("Dynamic Point Grid")

    canvas = Canvas(root, width=4000, height=4000, bg='white')
    canvas.pack()

    # Draw grid
    for i in range(0, 4001, 40):
        canvas.create_line(i, 0, i, 4000, fill='lightgray')
        canvas.create_line(0, i, 4000, i, fill='lightgray')

    # Create a point
    point = canvas.create_oval(180, 180, 220, 220, fill='red')
    point0 = canvas.create_oval(195, 195, 205, 205, fill='black')

