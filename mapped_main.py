import tkinter as tk
from tkinter import ttk
import random
import math
import json
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Fixed GeoJSON file path
GEOJSON_FILE_PATH = "data/turkey-admin-level-4.geojson"

class Antenna:
    def __init__(self, name, position, range_radius, antenna_range):
        self.name = name
        self.position = position
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

class MobileDevice:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.connected_antenna = None

class NetworkSimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Simulation")
        self.antennas = []
        self.mobile_devices = []
        self.city_polygon = None
        self.create_widgets()
        self.load_city_border()
    
    def get_city_names(geojson_data):
        """Extract and sort city names from GeoJSON data."""
        return sorted(
            feature["properties"]["name"]
            for feature in geojson_data.get("features", [])
            if "name" in feature["properties"]
    )
    
    def create_widgets(self):
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

        ttk.Label(control_frame, text="Antenna Range:").grid(row=0, column=0, sticky=tk.W)
        self.antenna_range = tk.IntVar(value=100)
        ttk.Entry(control_frame, textvariable=self.antenna_range).grid(row=0, column=1, sticky=(tk.W, tk.E))

        ttk.Label(control_frame, text="Antenna-to-Antenna Range:").grid(row=1, column=0, sticky=tk.W)
        self.antenna_to_antenna_range = tk.IntVar(value=200)
        ttk.Entry(control_frame, textvariable=self.antenna_to_antenna_range).grid(row=1, column=1, sticky=(tk.W, tk.E))

        ttk.Button(control_frame, text="Add Mobile Devices", command=self.add_mobile_devices).grid(row=2, column=0, columnspan=2)
        ttk.Button(control_frame, text="Show Connections", command=self.show_connections).grid(row=3, column=0, columnspan=2)

        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.canvas.bind("<Button-1>", self.add_antenna_on_click)
        self.canvas.bind("<Button-3>", self.delete_antenna_on_click)

    def load_city_border(self):
        try:
            with open(GEOJSON_FILE_PATH, 'r', encoding='utf-8') as f:
                geojson_data = json.load(f)
            for feature in geojson_data["features"]:
                if feature["properties"]["name"] == "Ankara":  # Change to your desired city name
                    coordinates = feature["geometry"]["coordinates"][0]
                    self.city_polygon = Polygon(coordinates)
                    self.draw_city_border(coordinates)
                    break
        except FileNotFoundError:
            print(f"Error: GeoJSON file not found at {GEOJSON_FILE_PATH}")

    def draw_city_border(self, coordinates):
        lons, lats = zip(*coordinates)

        # Get the canvas dimensions
        self.canvas.update()  # Ensure the canvas dimensions are updated
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Calculate the bounding box of the city's coordinates
        min_lon, max_lon = min(lons), max(lons)
        min_lat, max_lat = min(lats), max(lats)

        # Calculate scaling factors for the map to fit within the canvas
        lon_range = max_lon - min_lon
        lat_range = max_lat - min_lat

        if lon_range == 0 or lat_range == 0:
            print("Error: Invalid city boundary coordinates.")
            return

        scale_factor = min(
            (canvas_width - 20) / lon_range,  # 20 pixels padding on width
            (canvas_height - 20) / lat_range  # 20 pixels padding on height
        )

        # Calculate offsets to center the map on the canvas
        x_offset = (canvas_width - lon_range * scale_factor) / 2
        y_offset = (canvas_height - lat_range * scale_factor) / 2

        # Transform and scale the coordinates to fit on the canvas
        scaled_coords = [
            (
                (lon - min_lon) * scale_factor + x_offset,
                canvas_height - ((lat - min_lat) * scale_factor + y_offset)
            )
            for lon, lat in coordinates
        ]

        # Draw the city border
        self.canvas.create_polygon(scaled_coords, outline="blue", fill="", width=2)

        # Debugging: print scaled coordinates to check values
        print(f"Scaled coordinates: {scaled_coords}")
        print(f"Canvas size: {canvas_width}x{canvas_height}")
        print(f"Scale factor: {scale_factor}, Offsets: ({x_offset}, {y_offset})")


    def is_within_city_border(self, position):
        if self.city_polygon:
            # Transform canvas coordinates back to original longitude/latitude
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            lons, lats = zip(*list(self.city_polygon.exterior.coords))
            min_lon, max_lon = min(lons), max(lons)
            min_lat, max_lat = min(lats), max(lats)

            lon_range = max_lon - min_lon
            lat_range = max_lat - min_lat

            scale_factor = min(
                (canvas_width - 20) / lon_range,  # 20 pixels padding on width
                (canvas_height - 20) / lat_range  # 20 pixels padding on height
            )

            x_offset = (canvas_width - lon_range * scale_factor) / 2
            y_offset = (canvas_height - lat_range * scale_factor) / 2

            # Reverse transformation from canvas to geo-coordinates
            geo_x = (position[0] - x_offset) / scale_factor + min_lon
            geo_y = (canvas_height - position[1] - y_offset) / scale_factor + min_lat

            # Check if the point is inside the polygon
            point = Point(geo_x, geo_y)
            return self.city_polygon.contains(point)

        return False


    def add_antenna_on_click(self, event):
        position = (event.x, event.y)
        if self.is_within_city_border(position):
            antenna_name = f"Antenna-{len(self.antennas) + 1}"
            antenna = Antenna(antenna_name, position, self.antenna_range.get(), self.antenna_to_antenna_range.get())
            self.antennas.append(antenna)
            self.canvas.create_oval(event.x - 10, event.y - 10, event.x + 10, event.y + 10, fill="red", tags=antenna_name)
            self.canvas.create_text(event.x, event.y + 20, text=antenna_name)

    def delete_antenna_on_click(self, event):
        for antenna in self.antennas:
            x, y = antenna.position
            if (x - 10 <= event.x <= x + 10) and (y - 10 <= event.y <= y + 10):
                self.antennas.remove(antenna)
                self.canvas.delete(antenna.name)
                break

    def add_mobile_devices(self):
        for _ in range(30):
            x = random.randint(50, 750)
            y = random.randint(50, 550)
            if self.is_within_city_border((x, y)):
                device_name = f"Device-{len(self.mobile_devices) + 1}"
                device = MobileDevice(device_name, (x, y))
                self.mobile_devices.append(device)
                self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="blue", tags=device_name)

    def show_connections(self):
        self.canvas.delete("connection")
        for antenna in self.antennas:
            for device in self.mobile_devices:
                if antenna.is_within_range(device):
                    antenna.connect_device(device)
                    x1, y1 = antenna.position
                    x2, y2 = device.position
                    self.canvas.create_line(x1, y1, x2, y2, fill="green", tags="connection")

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkSimulationApp(root)
    root.mainloop()
