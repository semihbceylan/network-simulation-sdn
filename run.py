import tkinter as tk
from tkinter import ttk
import subprocess
import os

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Function to run Simulation 1
def run_simulation1():
    subprocess.run(['python', os.path.join(current_dir, 'main.py')])

# Function to run Simulation 2
def run_simulation2():
    subprocess.run(['python', os.path.join(current_dir, 'gui.py')])

# Function to run Simulation 3
def run_simulation3():
    subprocess.run(['python', os.path.join(current_dir, 'sim.py')])

# Function to run Simulation 4
def run_simulation4():
    subprocess.run(['python', os.path.join(current_dir, 'core.py')])

# Function to run Simulation 5
def run_simulation5():
    subprocess.run(['python', os.path.join(current_dir, 'map.py')])



# Create the main window
window = tk.Tk()
window.title("Simulation Selector")

# Set window size and background color to match the style
window.geometry("400x400")  # Increased size for fourth button
window.configure(bg='#001f26')  # Dark background

# Custom styles to match the theme
style = ttk.Style()
style.theme_use('clam')

# Custom font and button styles
style.configure('TButton', 
                background='#004d66', 
                foreground='#cceeff', 
                font=('Helvetica', 12, 'bold'), 
                padding=10, 
                borderwidth=2)

style.map('TButton', 
          background=[('active', '#007acc')],
          foreground=[('active', '#ffffff')])

style.configure('TLabel', 
                background='#001f26', 
                foreground='#66ccff', 
                font=('Helvetica', 14, 'bold'))

# Create and place a label
label = ttk.Label(window, text="Choose a Simulation")
label.pack(pady=20)

# Create buttons with a matching style to run the simulations
button1 = ttk.Button(window, text="End User", command=run_simulation1)
button1.pack(pady=10)

button2 = ttk.Button(window, text="Infrastructure Provider", command=run_simulation2)
button2.pack(pady=10)

button3 = ttk.Button(window, text="Abstract Model", command=run_simulation3)
button3.pack(pady=10)

button4 = ttk.Button(window, text="Command Center", command=run_simulation4)
button4.pack(pady=10)

button5 = ttk.Button(window, text="Provinces of Turkey", command=run_simulation5)
button5.pack(pady=10)

# Add a glowing effect around the buttons
def apply_glow(widget):
    def on_enter(event):
        widget.configure(style='Glow.TButton')

    def on_leave(event):
        widget.configure(style='TButton')

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)

style.configure('Glow.TButton', 
                background='#33ccff', 
                foreground='#001f26', 
                font=('Helvetica', 12, 'bold'), 
                padding=10, 
                borderwidth=3)

apply_glow(button1)
apply_glow(button2)
apply_glow(button3)
apply_glow(button4)
apply_glow(button5)

# Run the GUI loop
window.mainloop()
