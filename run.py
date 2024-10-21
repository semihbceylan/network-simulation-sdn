import tkinter as tk
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

# Create the main window
window = tk.Tk()
window.title("Simulation Selector")

# Set window size
window.geometry("300x150")

# Create and place a label
label = tk.Label(window, text="Choose a Simulation to Run")
label.pack(pady=10)

# Create buttons to run the simulations
button1 = tk.Button(window, text="Run Simulation 1", command=run_simulation1)
button1.pack(pady=5)

button2 = tk.Button(window, text="Run Simulation 2", command=run_simulation2)
button2.pack(pady=5)

# Run the GUI loop
window.mainloop()
