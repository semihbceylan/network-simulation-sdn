import tkinter as tk
from tkinter import ttk
import math

class NetworkSimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Coverage Simulation")
        
        # Initialize parameters
        self.antennas = []
        self.drone = None  # To track the drone node
        self.antenna_range = tk.DoubleVar(value=150)  # Default range of antennas
        
        # Create the GUI layout
        self.create_widgets()
        
    def create_widgets(self):
        # Create a frame for the controls
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Add a label and entry for the antenna range
        ttk.Label(control_frame, text="Antenna Range:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(control_frame, textvariable=self.antenna_range).grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Create a canvas for the network visualization
        self.canvas = tk.Canvas(self.root, width=1200, height=700, bg="white")
        self.canvas.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Bind the left mouse click event to place antennas
        self.canvas.bind("<Button-1>", self.on_canvas_left_click)
        
        # Bind the right mouse click event to delete antennas
        self.canvas.bind("<Button-3>", self.on_canvas_right_click)
        
    def on_canvas_left_click(self, event):
        """Event handler for placing an antenna at the clicked position."""
        x, y = event.x, event.y
        self.place_antenna_at(x, y)
        
    def on_canvas_right_click(self, event):
        """Event handler for deleting the closest antenna or drone to the right-click position."""
        x, y = event.x, event.y
        self.delete_closest_node(x, y)
        
    def place_antenna(self):
        """Add a new antenna at a predefined position (for testing purposes)."""
        x, y = 400, 300  # Central position
        self.place_antenna_at(x, y)
        
    def place_antenna_at(self, x, y):
        """Add a new antenna at the specified position."""
        antenna = {'x': x, 'y': y, 'range': self.antenna_range.get()}
        self.antennas.append(antenna)
        self.draw_antenna(antenna)
        
    def draw_antenna(self, antenna):
        """Draw an antenna and its coverage area on the canvas."""
        x, y, r = antenna['x'], antenna['y'], antenna['range']
        
        # Draw the coverage area (circle)
        self.canvas.create_oval(x - r, y - r, x + r, y + r, outline="blue", width=2, tags="coverage")
        
        # Draw the antenna as a small circle
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red", tags="antenna")
        
        # Visualize connections between antennas
        self.update_connections()
        
    def delete_closest_node(self, x, y):
        """Find and delete the closest antenna or drone to the clicked position."""
        if not self.antennas and not self.drone:
            return
        
        closest_node = None
        min_distance = float('inf')
        
        # Find the closest antenna by comparing distances
        for antenna in self.antennas:
            dist = self.distance_from_point(antenna, x, y)
            if dist < min_distance:
                min_distance = dist
                closest_node = antenna
        
        # Check the drone as well
        if self.drone:
            dist = self.distance_from_point(self.drone, x, y)
            if dist < min_distance:
                min_distance = dist
                closest_node = self.drone
        
        # Remove the node if it's within a reasonable click distance (20 pixels radius)
        if closest_node and min_distance <= 20:
            if closest_node == self.drone:
                self.drone = None
                self.canvas.delete("drone")
                self.canvas.delete("drone_connections")
            else:
                self.antennas.remove(closest_node)
            self.redraw_canvas()

            # After deleting, re-evaluate network connectivity
            if not self.is_network_connected():
                self.place_drone_optimally()
            else:
                # Clear any existing drone connections if the network is now fully connected
                self.drone = None
                self.canvas.delete("drone_connections")
                self.canvas.delete("drone")

        
    def redraw_canvas(self):
        """Clear the canvas and redraw all antennas and connections."""
        self.canvas.delete("all")  # Clear everything
        for antenna in self.antennas:
            self.draw_antenna(antenna)  # Redraw antennas and connections
        if self.drone:
            self.draw_drone(self.drone)
        
    def update_connections(self):
        """Update the connections between antennas based on their range."""
        self.canvas.delete("connections")  # Remove existing connections
        
        for i, ant1 in enumerate(self.antennas):
            for j, ant2 in enumerate(self.antennas):
                if i != j:
                    dist = self.distance(ant1, ant2)
                    if dist <= ant1['range']:  # If in range, draw a line
                        self.canvas.create_line(ant1['x'], ant1['y'], ant2['x'], ant2['y'], fill="green", tags="connections")
        
    def place_drone_optimally(self):
        """Place the drone at the optimal position to connect the closest nodes between clusters."""
        clusters = self.find_clusters()
        if len(clusters) < 2:
            return  # No need for a drone if the network is still connected
        
        # Find the closest pair of nodes between different clusters
        min_distance = float('inf')
        best_pair = None
        
        for i, cluster1 in enumerate(clusters):
            for j, cluster2 in enumerate(clusters):
                if i != j:
                    for ant1 in cluster1:
                        for ant2 in cluster2:
                            dist = self.distance(ant1, ant2)
                            if dist < min_distance:
                                min_distance = dist
                                best_pair = (ant1, ant2)
        
        if best_pair:
            # Place the drone at the midpoint between the closest nodes
            ant1, ant2 = best_pair
            drone_x = (ant1['x'] + ant2['x']) / 2
            drone_y = (ant1['y'] + ant2['y']) / 2
            self.drone = {'x': drone_x, 'y': drone_y, 'range': self.antenna_range.get() * 1.5}  # Larger range for the drone
            
            # Draw the drone in a different color (green)
            self.draw_drone(self.drone)
            
            # Connect the drone to the closest nodes
            self.canvas.create_line(drone_x, drone_y, ant1['x'], ant1['y'], fill="green", tags="drone_connections")
            self.canvas.create_line(drone_x, drone_y, ant2['x'], ant2['y'], fill="green", tags="drone_connections")
    
    def draw_drone(self, drone):
        """Draw the drone on the canvas."""
        x, y, r = drone['x'], drone['y'], drone['range']
        
        # Draw the drone as a larger circle
        self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="green", tags="drone")
        
    def find_clusters(self):
        """Find all connected clusters of antennas."""
        clusters = []
        visited = set()
        
        for i, antenna in enumerate(self.antennas):
            if i not in visited:
                cluster = []
                self.dfs(i, visited, cluster)
                clusters.append(cluster)
        
        return clusters
    
    def dfs(self, index, visited, cluster):
        """Depth-first search to find all antennas in the same cluster."""
        visited.add(index)
        cluster.append(self.antennas[index])
        
        for i, other in enumerate(self.antennas):
            if i not in visited and self.distance(self.antennas[index], other) <= self.antennas[index]['range']:
                self.dfs(i, visited, cluster)
                
    def is_network_connected(self):
        """Check if the current network is fully connected."""
        if len(self.antennas) < 2:
            return True  # A single antenna is always connected
        
        visited = set()
        self.dfs(0, visited, [])
        return len(visited) == len(self.antennas)
    
    def distance(self, ant1, ant2):
        """Calculate the distance between two antennas."""
        return math.sqrt((ant1['x'] - ant2['x']) ** 2 + (ant1['y'] - ant2['y']) ** 2)
    
    def distance_from_point(self, antenna, x, y):
        """Calculate the distance between an antenna and a point (x, y)."""
        return math.sqrt((antenna['x'] - x) ** 2 + (antenna['y'] - y) ** 2)

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkSimulationApp(root)
    root.mainloop()