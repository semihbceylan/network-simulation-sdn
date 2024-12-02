class Topology:
    """A generic topology class for network simulation."""

    def __init__(self):
        self.hosts = []
        self.switches = []
        self.links = []

    def add_host(self, host_name):
        self.hosts.append(host_name)
        print(f"Host '{host_name}' added.")
        return host_name

    def add_switch(self, switch_name):
        self.switches.append(switch_name)
        print(f"Switch '{switch_name}' added.")
        return switch_name

    def add_link(self, node1, node2, **params):
        params_tuple = tuple(params.items())  # Convert params to a tuple of key-value pairs
        self.links.append((node1, node2, params_tuple))
        print(f"Link added between '{node1}' and '{node2}' with params: {params}")


class Network:
    """A generic network class for managing the topology and simulation."""

    def __init__(self, topology):
        self.topology = topology
        self.status = "Initialized"
        self.active_links = {link: True for link in self.topology.links}

    def start(self):
        """Start the network simulation."""
        self.status = "Network simulation started"
        print(self.status)

    def simulate_failure(self, node1, node2):
        """Simulate a failure between two nodes."""
        for link in self.topology.links:
            if (node1, node2) == link[:2]:
                self.active_links[link] = False
                print(f"Simulating failure: Link between '{node1}' and '{node2}' is down.")
                self.status = f"Link between '{node1}' and '{node2}' disabled"
                return
        print(f"No active link found between '{node1}' and '{node2}'.")

    def restore_link(self, node1, node2):
        """Restore the link between two nodes."""
        for link in self.topology.links:
            if (node1, node2) == link[:2]:
                self.active_links[link] = True
                print(f"Restoring link: Link between '{node1}' and '{node2}' is up.")
                self.status = f"Link between '{node1}' and '{node2}' restored."
                return
        print(f"No link found between '{node1}' and '{node2}' to restore.")

    def stop(self):
        """Stop the network simulation."""
        self.status = "Network simulation stopped"
        print(self.status)

    def get_status(self):
        """Get the current status of the network."""
        return self.status


class Drone:
    """A class representing a drone that can restore network links."""

    def __init__(self, name):
        self.name = name
        self.status = "Ready"

    def fly_to_location(self, node1, node2):
        """Simulate the drone flying to the location of the broken link."""
        print(f"Drone '{self.name}' flying to location of link between '{node1}' and '{node2}'...")
        self.status = "In Transit"

    def repair_link(self, network, node1, node2):
        """Simulate the drone repairing the broken link."""
        for link in network.topology.links:
            if (node1, node2) == link[:2] and not network.active_links[link]:
                print(f"Drone '{self.name}' repairing link between '{node1}' and '{node2}'...")
                network.restore_link(node1, node2)
                self.status = "Repair Completed"
                return
        print(f"Drone '{self.name}': Link between '{node1}' and '{node2}' is already active or does not exist.")

    def return_to_base(self):
        """Simulate the drone returning to base."""
        print(f"Drone '{self.name}' returning to base...")
        self.status = "Ready"


class MobileDevice:
    """A class representing a mobile device in the network."""

    def __init__(self, name, position=None):
        self.name = name
        self.position = position  # Position could be coordinates (x, y) or a region label
        self.status = "Disconnected"

    def connect_to_network(self, network, node):
        """Connect the mobile device to the network via a node."""
        print(f"Mobile device '{self.name}' connecting to network through '{node}'...")
        self.status = "Connected"
        network.topology.add_link(self.name, node, bw=10, delay="1ms", loss=0)

    def disconnect_from_network(self, network):
        """Disconnect the mobile device from the network."""
        print(f"Mobile device '{self.name}' disconnecting from network...")
        self.status = "Disconnected"
        network.topology.links = [
            link for link in network.topology.links if self.name not in link[:2]
        ]

    def move(self, new_position):
        """Simulate the mobile device moving to a new position."""
        print(f"Mobile device '{self.name}' moving from '{self.position}' to '{new_position}'...")
        self.position = new_position


class SimulationManager:
    """A class to manage the entire network simulation process."""

    def __init__(self):
        self.network = None
        self.simulation_status = "Initialized"
        self.drones = [Drone(f"Drone-{i}") for i in range(1, 3)]
        self.mobile_devices = []

    def start_simulation(self):
        """Starts the network simulation."""
        topology = self.build_topology()
        self.network = Network(topology)
        self.network.start()
        self.simulation_status = "Simulation started"
        print(self.simulation_status)

    def simulate_failure(self):
        """Simulates a network failure."""
        print("Simulating network failure...")
        self.network.simulate_failure("s1", "s2")

    def restore_network_with_drone(self):
        """Restores the network after failure using a drone."""
        print("Deploying drone to restore network after failure...")
        drone = self.assign_drone()
        if drone:
            drone.fly_to_location("s1", "s2")
            drone.repair_link(self.network, "s1", "s2")
            drone.return_to_base()
        else:
            print("No available drones for restoration.")

    def stop_simulation(self):
        """Stops the network simulation."""
        if self.network:
            self.network.stop()
        self.simulation_status = "Simulation stopped"
        print(self.simulation_status)

    def build_topology(self):
        """Builds the generic network topology."""
        topo = Topology()
        h1 = topo.add_host("h1")
        h2 = topo.add_host("h2")

        s1 = topo.add_switch("s1")
        s2 = topo.add_switch("s2")

        topo.add_link(h1, s1, bw=100, delay="5ms", loss=1)
        topo.add_link(h2, s2, bw=100, delay="5ms", loss=1)
        topo.add_link(s1, s2, bw=100, delay="10ms", loss=1)
        topo.add_link(s1, s2, bw=100, delay="20ms", loss=0)  # Backup link
        return topo

    def assign_drone(self):
        """Assigns an available drone for the task."""
        for drone in self.drones:
            if drone.status == "Ready":
                print(f"Assigning '{drone.name}' for the repair task.")
                return drone
        print("No drones are currently available.")
        return None

    def add_mobile_device(self, name, position=None):
        """Adds a mobile device to the simulation."""
        device = MobileDevice(name, position)
        self.mobile_devices.append(device)
        print(f"Mobile device '{name}' added to the simulation.")
        return device

    def simulate_mobile_device_connection(self, device_name, node_name):
        """Simulate a mobile device connecting to the network."""
        device = next((d for d in self.mobile_devices if d.name == device_name), None)
        if device:
            device.connect_to_network(self.network, node_name)
        else:
            print(f"No mobile device named '{device_name}' found.")

    def simulate_mobile_device_disconnection(self, device_name):
        """Simulate a mobile device disconnecting from the network."""
        device = next((d for d in self.mobile_devices if d.name == device_name), None)
        if device:
            device.disconnect_from_network(self.network)
        else:
            print(f"No mobile device named '{device_name}' found.")


if __name__ == "__main__":
    import graphviz
    from PIL import Image
    from io import BytesIO

    # Function to generate a class diagram
    def visualize_classes(classes):
        dot = graphviz.Digraph(comment="Class Diagram")

        # General layout settings
        dot.attr(rankdir='TB', splines='true', bgcolor='#f8f9fa')

        # Legend
        dot.node("legend", label="""<<table border="0" cellpadding="4">
<tr><td><b>Legend:</b></td></tr>
<tr><td bgcolor="#aad4e5">Class</td></tr>
<tr><td bgcolor="#c5f7d0">Method</td></tr>
<tr><td bgcolor="#ffe2a8">Attribute</td></tr>
</table>>""", shape='plaintext')

        for cls in classes:
            # Add node for the class
            dot.node(cls.__name__, cls.__name__, shape="box", style="filled", fillcolor="#aad4e5", fontname="Arial")

            # Add inheritance relationships
            for base in cls.__bases__:
                dot.edge(base.__name__, cls.__name__, label="inherits", fontcolor="#007bff", color="#007bff", fontname="Arial")

            # Add methods and attributes
            methods = [m for m in dir(cls) if callable(getattr(cls, m)) and not m.startswith("__")]
            attributes = [a for a in dir(cls) if not callable(getattr(cls, a)) and not a.startswith("__")]

            for method in methods:
                dot.node(f"{cls.__name__}_{method}", method, shape="ellipse", style="filled", fillcolor="#c5f7d0", fontname="Arial")
                dot.edge(cls.__name__, f"{cls.__name__}_{method}", label="method", fontcolor="#28a745", color="#28a745", fontname="Arial")

            for attr in attributes:
                dot.node(f"{cls.__name__}_{attr}", attr, shape="ellipse", style="filled", fillcolor="#ffe2a8", fontname="Arial")
                dot.edge(cls.__name__, f"{cls.__name__}_{attr}", label="attribute", fontcolor="#fd7e14", color="#fd7e14", fontname="Arial")

        return dot

    # Classes to visualize
    classes_to_visualize = [Topology, Network, SimulationManager, Drone, MobileDevice]

    # Generate the class diagram
    class_diagram = visualize_classes(classes_to_visualize)

    # Render the class diagram in memory as PNG
    image_data = class_diagram.pipe(format='png')

    # Use PIL to open and display the image
    image = Image.open(BytesIO(image_data))
    image.show()
