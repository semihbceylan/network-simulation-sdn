import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from sim import Topology, Network, Drone, MobileDevice, SimulationManager


class SimulationApp:
    def __init__(self, root):
        self.root = root
        self.simulation_manager = SimulationManager()
        self.root.title("Network Simulation App")
        self.create_widgets()

    def create_widgets(self):
        # Frame for Simulation Controls
        control_frame = tk.Frame(self.root, padx=10, pady=10)
        control_frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(control_frame, text="Simulation Controls", font=("Arial", 14)).grid(
            row=0, column=0, columnspan=2
        )

        start_btn = tk.Button(control_frame, text="Start Simulation", command=self.start_simulation)
        start_btn.grid(row=1, column=0, pady=5)

        stop_btn = tk.Button(control_frame, text="Stop Simulation", command=self.stop_simulation)
        stop_btn.grid(row=1, column=1, pady=5)

        failure_btn = tk.Button(control_frame, text="Simulate Failure", command=self.simulate_failure)
        failure_btn.grid(row=2, column=0, pady=5)

        restore_btn = tk.Button(control_frame, text="Restore Network", command=self.restore_network)
        restore_btn.grid(row=2, column=1, pady=5)

        # Frame for Adding Devices
        device_frame = tk.Frame(self.root, padx=10, pady=10)
        device_frame.grid(row=1, column=0, sticky="nsew")

        tk.Label(device_frame, text="Manage Mobile Devices", font=("Arial", 14)).grid(
            row=0, column=0, columnspan=2
        )

        tk.Label(device_frame, text="Device Name:").grid(row=1, column=0, sticky="e")
        self.device_name_entry = tk.Entry(device_frame)
        self.device_name_entry.grid(row=1, column=1, pady=5)

        tk.Label(device_frame, text="Position:").grid(row=2, column=0, sticky="e")
        self.device_position_entry = tk.Entry(device_frame)
        self.device_position_entry.grid(row=2, column=1, pady=5)

        add_device_btn = tk.Button(device_frame, text="Add Device", command=self.add_device)
        add_device_btn.grid(row=3, column=0, pady=5)

        # Frame for Status
        status_frame = tk.Frame(self.root, padx=10, pady=10)
        status_frame.grid(row=2, column=0, sticky="nsew")

        tk.Label(status_frame, text="Simulation Status", font=("Arial", 14)).grid(
            row=0, column=0, columnspan=2
        )

        self.status_label = tk.Label(status_frame, text="Status: Initialized", wraplength=300)
        self.status_label.grid(row=1, column=0, columnspan=2, pady=5)

    def update_status(self, message):
        self.status_label.config(text=f"Status: {message}")

    def start_simulation(self):
        self.simulation_manager.start_simulation()
        self.update_status(self.simulation_manager.simulation_status)

    def stop_simulation(self):
        self.simulation_manager.stop_simulation()
        self.update_status(self.simulation_manager.simulation_status)

    def simulate_failure(self):
        self.simulation_manager.simulate_failure()
        self.update_status(self.simulation_manager.network.get_status())

    def restore_network(self):
        self.simulation_manager.restore_network_with_drone()
        self.update_status(self.simulation_manager.network.get_status())

    def add_device(self):
        device_name = self.device_name_entry.get()
        position = self.device_position_entry.get()
        if device_name:
            device = self.simulation_manager.add_mobile_device(device_name, position)
            self.simulation_manager.simulate_mobile_device_connection(device_name, "h1")
            messagebox.showinfo("Device Added", f"Device '{device.name}' connected at position '{position}'.")
        else:
            messagebox.showerror("Input Error", "Device Name cannot be empty.")


if __name__ == "__main__":
    root = tk.Tk()
    app = SimulationApp(root)
    root.mainloop()
