import time
from telemetrix import telemetrix
# 1. Initialize the board
board = telemetrix.Telemetrix()

# Define Pins
TRIG_PIN1 = 10
ECHO_PIN1 = 9
TRIG_PIN2 = 8
ECHO_PIN2 = 7


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
point = canvas.create_oval(195, 195, 205, 205, fill='red')
point0 = canvas.create_oval(195, 195, 205, 205, fill='black')
# Move point with arrow keys




coords = tuple([0,0] for _ in range(2)) # Start at the center of the grid
# 2. The Callback Function
# This runs automatically when the sensor gets a reading
def the_callback1(data):
    global coords
    # data[2] contains the distance in centimeters
    # print(f"Distance 1: {data[2]} cm")
    
    coords[coords[0][0]+1][0] = data[2]
    coords[0][0] = (coords[0][0] + 1) % (len(coords)-1)  # Move to the next index for the next reading
def the_callback2(data):
    global coords
    # data[2] contains the distance in centimeters
    # print(f"Distance 2: {data[2]} cm")
    coords[coords[0][1]+1][1] = data[2]
    coords[0][1] = (coords[0][1] + 1) % (len(coords)-1)  # Move to the next index for the next reading

# 3. Setup the Sonar
# Parameters: (trigger_pin, echo_pin, callback)
board.set_pin_mode_sonar(TRIG_PIN1, ECHO_PIN1, the_callback1)
board.set_pin_mode_sonar(TRIG_PIN2, ECHO_PIN2, the_callback2)

print("Reading distance... Press Ctrl+C to stop.")

try:
    def change_point_position(coords):
        
        # Keep the script alive; the library handles the rest in a separate thread
        # print(f"Current Coordinates: {coords}")
        coords_moy = [sum(x)/len(x) for x in zip(*coords[1:])]  # Calculate the average of the last 5 readings
        canvas.coords(point, coords_moy[0]*10 - 5 +200, coords_moy[1]*10 - 5 +200, coords_moy[0]*10 + 5 +200, coords_moy[1]*10  + 5 +200)
        print(f"Current Coordinates: {coords_moy}")
    while True:
        change_point_position(coords)
        root.update()
        time.sleep(0.1)
    
except KeyboardInterrupt:
    print("\nShutting down...")
finally:
    # Always clean up!
    board.shutdown()