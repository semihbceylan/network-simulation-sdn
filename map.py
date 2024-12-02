# This code shows Geolocation data on a map.
# This can be used on antenna code on main.py

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json

# Fixed GeoJSON file path
GEOJSON_FILE_PATH = "data/turkey-admin-level-4.geojson"

def get_city_names(geojson_data):
    """Extract and sort city names from GeoJSON data."""
    return sorted(
        feature["properties"]["name"]
        for feature in geojson_data.get("features", [])
        if "name" in feature["properties"]
    )

def plot_city_map(geojson_data, city_name, canvas_frame):
    """Plot the map of the selected city."""
    for feature in geojson_data.get("features", []):
        if feature["properties"].get("name") == city_name:
            coordinates = feature["geometry"]["coordinates"][0]
            break
    else:
        print(f"Boundary for {city_name} not found.")
        return

    lons, lats = zip(*coordinates)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(lons, lats, color="blue")
    ax.fill(lons, lats, color="lightblue", alpha=0.5)
    ax.set_title(f"Map of {city_name}")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.axis("equal")

    for widget in canvas_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()

def initialize_dropdown():
    """Initialize the city dropdown with sorted city names."""
    global geojson_data
    try:
        with open(GEOJSON_FILE_PATH, 'r', encoding='utf-8') as f:
            geojson_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {GEOJSON_FILE_PATH}")
        geojson_data = None
        return

    city_names = get_city_names(geojson_data)
    city_selector['values'] = city_names
    city_selector.set("Select a City")
    city_selector["state"] = "readonly"

def on_continue():
    """Open the map viewer application with the selected city."""
    selected_city = city_selector.get()
    if not selected_city:
        print("Please select a city first.")
        return

    if geojson_data is None:
        print("Error: GeoJSON data not loaded.")
        return

    # Open a new window for the map viewer
    map_viewer = tk.Toplevel(root)
    map_viewer.title(f"Map Viewer - {selected_city}")
    map_canvas_frame = tk.Frame(map_viewer)
    map_canvas_frame.pack(fill=tk.BOTH, expand=True)
    map_viewer.geometry("800x600")

    plot_city_map(geojson_data, selected_city, map_canvas_frame)

# Tkinter application
root = tk.Tk()
root.title("City Selection")

# Controls frame
controls_frame = tk.Frame(root)
controls_frame.pack(fill=tk.X, pady=10)

# Dropdown for city selection
city_selector = ttk.Combobox(controls_frame, state="disabled")
city_selector.pack(side=tk.LEFT, padx=10)

# Continue button (always active)
continue_button = tk.Button(controls_frame, text="Continue", command=on_continue)
continue_button.pack(side=tk.LEFT, padx=10)

# Initialize the dropdown with city data
geojson_data = None
initialize_dropdown()

# Start the Tkinter event loop
root.geometry("400x100")
root.mainloop()
