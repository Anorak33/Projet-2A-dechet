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
def move_point(event):
    if event.keysym == 'Up':
        canvas.move(point, 0, -1)
      
    elif event.keysym == 'Down':
        canvas.move(point, 0, 1)
    if event.keysym == 'Left':
        canvas.move(point, -1, 0)
    elif event.keysym == 'Right':
        canvas.move(point, 1, 0)

def change_point_position(x, y):
    canvas.coords(point, x-5, y-5, x+5, y+5)

root.bind('<Key>', move_point)
root.mainloop()
