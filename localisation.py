from tkinter import Canvas
import tkinter as tk
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



import serial
import time

# Remplace 'COM3' par ton port (ex: '/dev/ttyUSB0' sur Linux/Mac)
# Tu peux trouver le port dans l'IDE Arduino -> Outils -> Port
port_arduino = 'COM4' 
vitesse = 115200

# try:
#     # Initialisation de la connexion
#     arduino = serial.Serial(port_arduino, vitesse, timeout=1)
#     print(f"Connexion établie sur le port {port_arduino}")
#     time.sleep(2) # Pause pour laisser l'Arduino rebooter à la connexion

#     while True:
#         if arduino.in_waiting > 0:
#             # Lecture de la ligne reçue
#             donnee = arduino.readline().decode('utf-8').rstrip()
#             print(f"Valeur reçue de l'Arduino : {donnee}")

# except serial.SerialException as e:
#     print(f"Erreur : {e}")
# except KeyboardInterrupt:
#     print("\nArrêt du programme...")
# finally:
#     if 'arduino' in locals() and arduino.is_open:
#         arduino.close()
#         print("Connexion fermée.")


print("Reading distance... Press Ctrl+C to stop.")

try:
    def change_point_position(coords):
        
        canvas.coords(point, coords[1]*10 - 15 +200, coords[2]*10 - 15 +200, coords[1]*10 + 15 +200, coords[2]*10  + 15 +200)
        print(f"Current Coordinates: {coords}")
        canvas.itemconfig(point, fill=f'#{(int(coords[0]))%256:02x}{(int(coords[0]))%256:02x}{(int(coords[0]))%256:02x}')
        

    arduino = serial.Serial(port_arduino, vitesse, timeout=1)
    print(f"Connexion établie sur le port {port_arduino}")

    while True:
        print("attente de la configuration...")
        if arduino.in_waiting > 0:
            print("configuration reçue")
            # Lecture de la ligne reçue
            donnee = arduino.readline().decode('utf-8').rstrip()
            if donnee == "--- Setup OK ---":
                break
    print("Configuration réussie, démarrage de la lecture des données...")

    while True:
        if arduino.in_waiting > 0:
            # Lecture de la ligne reçue
            donnee = arduino.readline().decode('utf-8').rstrip()
            coords = list(map(float, donnee.split(",")))
            change_point_position(coords)
            root.update()   
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nShutting down...")
except serial.SerialException as e:
    print(f"Erreur : {e}")
finally:
    if 'arduino' in locals() and arduino.is_open:
        arduino.close()
        print("Connexion fermée.")