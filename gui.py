import tkinter as tk
from tkinter import ttk

class NetworkSimulationApp:
	def __init__(self, root):
		self.root = root
		self.root.title("Sim2Net Network Simulation")

		self.create_widgets()

	def create_widgets(self):
		# Create a frame for the controls
		control_frame = ttk.Frame(self.root, padding="10")
		control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

		# Add a label and entry for the number of nodes
		ttk.Label(control_frame, text="Number of Nodes:").grid(row=0, column=0, sticky=tk.W)
		self.num_nodes = tk.IntVar()
		ttk.Entry(control_frame, textvariable=self.num_nodes).grid(row=0, column=1, sticky=(tk.W, tk.E))

		# Add a button to start the simulation
		ttk.Button(control_frame, text="Start Simulation", command=self.start_simulation).grid(row=1, column=0, columnspan=2)

		# Create a canvas for the network visualization
		self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
		self.canvas.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

	def start_simulation(self):
		# Clear the canvas
		self.canvas.delete("all")

		# Get the number of nodes
		num_nodes = self.num_nodes.get()

		# Simple example: draw nodes as circles
		for i in range(num_nodes):
			x = 50 + i * 50
			y = 50 + i * 50
			self.canvas.create_oval(x, y, x + 20, y + 20, fill="blue")

if __name__ == "__main__":
	root = tk.Tk()
	app = NetworkSimulationApp(root)
	root.mainloop()