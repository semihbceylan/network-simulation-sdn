import tkinter as tk
from tkinter import ttk
import random
import math

# Simulated city border (a rough rectangle for Istanbul)
CITY_BORDER = {
    "x_min": 50,
    "x_max": 750,
    "y_min": 50,
    "y_max": 550
}

# Parent class Antenna
class Antenna:
    def __init__(self, name, position, range_radius, antenna_range):
        self.name = name
        self.position = position  # (x, y) tuple
        self.range_radius = range_radius  # Mobile device range
        self.antenna_range = antenna_range  # Antenna-to-antenna range
        self.connected_devices = []
        self.connected_antennas = []

    def is_within_range(self, device):
        x1, y1 = self.position
        x2, y2 = device.position
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return distance <= self.range_radius

    def is_antenna_within_range(self, other_antenna):
        x1, y1 = self.position
        x2, y2 = other_antenna.position
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return distance <= self.antenna_range

    def connect_device(self, device):
        if self.is_within_range(device):
            self.connected_devices.append(device)
            device.connected_antenna = self

    def connect_antenna(self, other_antenna):
        if self.is_antenna_within_range(other_antenna):
            self.connected_antennas.append(other_antenna)

# Parent class MobileDevice
class MobileDevice:
    def __init__(self, name, position):
        self.name = name
        self.position = position  # (x, y) tuple
        self.connected_antenna = None

# Main GUI class
class NetworkSimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Simulation")

        self.antennas = []
        self.mobile_devices = []

        self.create_widgets()

    def create_widgets(self):
        # Create a frame for the controls
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

        # Add a label for the antenna range
        ttk.Label(control_frame, text="Antenna Range:").grid(row=0, column=0, sticky=tk.W)
        self.antenna_range = tk.IntVar(value=100)  # Default range
        ttk.Entry(control_frame, textvariable=self.antenna_range).grid(row=0, column=1, sticky=(tk.W, tk.E))

        # Add a label for antenna-to-antenna range
        ttk.Label(control_frame, text="Antenna-to-Antenna Range:").grid(row=1, column=0, sticky=tk.W)
        self.antenna_to_antenna_range = tk.IntVar(value=200)  # Default range for antenna-to-antenna

        # Add button to populate space with random clusters
        ttk.Button(control_frame, text="Populate Space", command=self.populate_space_with_clusters).grid(row=2, column=0, columnspan=2)

        # Add button to show connections
        ttk.Button(control_frame, text="Show Connections", command=self.show_connections).grid(row=3, column=0, columnspan=2)

        # Create a canvas for the network visualization
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Bind left mouse click to adding an antenna, right-click to delete
        self.canvas.bind("<Button-1>", self.add_antenna_on_click)
        self.canvas.bind("<Button-3>", self.delete_antenna_on_click)

        # Draw city border (for Istanbul)
        self.draw_city_border()

    def populate_space_with_clusters(self):
        """Populate the entire space with randomly distributed mobile device clusters."""
        num_clusters = 10  # Number of clusters to generate
        devices_per_cluster = 10  # Number of devices per cluster

        for _ in range(num_clusters):
            # Randomly choose a cluster center within the city border
            cluster_x = random.randint(CITY_BORDER["x_min"] + 30, CITY_BORDER["x_max"] - 30)
            cluster_y = random.randint(CITY_BORDER["y_min"] + 30, CITY_BORDER["y_max"] - 30)

            # Create devices around this cluster center
            for i in range(devices_per_cluster):
                device_name = f"Device-{len(self.mobile_devices) + 1}"
                # Randomly offset device positions within a small range around the cluster center
                x_offset = random.randint(-20, 20)
                y_offset = random.randint(-20, 20)
                position = (cluster_x + x_offset, cluster_y + y_offset)

                # Ensure the device stays within city borders
                if self.is_within_city_border(position):
                    device = MobileDevice(device_name, position)
                    self.mobile_devices.append(device)

                    x_device, y_device = position
                    self.canvas.create_oval(
                        x_device - 5, y_device - 5, x_device + 5, y_device + 5, fill="blue", tags=device_name
                    )

    def draw_city_border(self):
        """Draw a rectangle representing the city border."""
        self.canvas.create_rectangle(CITY_BORDER["x_min"], CITY_BORDER["y_min"], CITY_BORDER["x_max"], CITY_BORDER["y_max"], outline="blue", dash=(4, 2))

    def delete_antenna_on_click(self, event):
        # Delete an antenna if right-clicked on it
        for antenna in self.antennas:
            x, y = antenna.position
            if (x - 10 <= event.x <= x + 10) and (y - 10 <= event.y <= y + 10):
                # Reset connected devices to unconnected (blue)
                for device in antenna.connected_devices:
                    device.connected_antenna = None
                    x2, y2 = device.position
                    self.canvas.create_oval(x2 - 5, y2 - 5, x2 + 5, y2 + 5, fill="blue", tags=device.name)

                # Remove antenna from list and delete visuals
                self.antennas.remove(antenna)
                self.canvas.delete(antenna.name)  # Delete antenna shape
                self.canvas.delete("connection")  # Remove connections
                self.canvas.delete(f"text_{antenna.name}")  # Remove antenna label
                break

    def add_antenna_on_click(self, event):
        # Get the mouse click coordinates and add an antenna at that position
        antenna_name = f"Antenna-{len(self.antennas) + 1}"
        position = (event.x, event.y)

        # Check if the click is inside the city border
        if self.is_within_city_border(position):
            range_radius = self.antenna_range.get()
            antenna_to_antenna_range = self.antenna_to_antenna_range.get()

            antenna = Antenna(antenna_name, position, range_radius, antenna_to_antenna_range)
            self.antennas.append(antenna)

            # Visualize the antenna on the canvas
            x, y = position
            self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="red", tags=antenna_name)
            self.canvas.create_text(x, y + 20, text=antenna_name, tags=f"text_{antenna_name}")  # Add tag to text for deletion


    def add_mobile_devices(self):
        # Create small clusters of mobile devices in random areas within the city border
        num_clusters = 3
        devices_per_cluster = 10

        for cluster in range(num_clusters):
            cluster_x = random.randint(CITY_BORDER["x_min"] + 30, CITY_BORDER["x_max"] - 30)  # Adjust to avoid going out of bounds
            cluster_y = random.randint(CITY_BORDER["y_min"] + 30, CITY_BORDER["y_max"] - 30)

            for i in range(devices_per_cluster):
                device_name = f"Device-{len(self.mobile_devices) + 1}"
                x_offset = random.randint(-20, 20)
                y_offset = random.randint(-20, 20)
                position = (cluster_x + x_offset, cluster_y + y_offset)

                # Ensure mobile devices stay within city borders
                if self.is_within_city_border(position):
                    device = MobileDevice(device_name, position)
                    self.mobile_devices.append(device)

                    x, y = position
                    self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="blue", tags=device_name)
                    #self.canvas.create_text(x, y + 20, text=device_name)

    def show_connections(self):
        # Clear previous connections
        self.canvas.delete("connection")

        # Connect mobile devices to antennas
        for antenna in self.antennas:
            for device in self.mobile_devices:
                if antenna.is_within_range(device):
                    antenna.connect_device(device)
                    x1, y1 = antenna.position
                    x2, y2 = device.position
                    # Change color to green for connected mobile devices
                    self.canvas.create_oval(x2 - 5, y2 - 5, x2 + 5, y2 + 5, fill="green", tags=device.name)
                    # Draw a line representing the connection
                    self.canvas.create_line(x1, y1, x2, y2, fill="green", tags="connection")

        # Connect antennas to each other
        for i, antenna1 in enumerate(self.antennas):
            for antenna2 in self.antennas[i+1:]:
                if antenna1.is_antenna_within_range(antenna2):
                    antenna1.connect_antenna(antenna2)
                    x1, y1 = antenna1.position
                    x2, y2 = antenna2.position
                    # Draw a line between connected antennas
                    self.canvas.create_line(x1, y1, x2, y2, fill="red", dash=(4, 2), tags="connection")

    def is_within_city_border(self, position):
        """Check if the position is within the predefined city border."""
        x, y = position
        return CITY_BORDER["x_min"] <= x <= CITY_BORDER["x_max"] and CITY_BORDER["y_min"] <= y <= CITY_BORDER["y_max"]

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkSimulationApp(root)
    root.mainloop()