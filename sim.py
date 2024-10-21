from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink
import time

class DisasterResilientSDNTopo(Topo):
    """A custom Mininet topology representing a disaster-resilient SDN network."""
    
    def build(self):
        h1 = self.addHost('h1')  # Host 1
        h2 = self.addHost('h2')  # Host 2

        s1 = self.addSwitch('s1', cls=OVSSwitch)  # Switch 1
        s2 = self.addSwitch('s2', cls=OVSSwitch)  # Switch 2

        self.addLink(h1, s1, cls=TCLink, bw=100, delay='5ms', loss=1)
        self.addLink(h2, s2, cls=TCLink, bw=100, delay='5ms', loss=1)
        self.addLink(s1, s2, cls=TCLink, bw=100, delay='10ms', loss=1)

        # Backup link
        self.addLink(s1, s2, cls=TCLink, bw=100, delay='20ms', loss=0)

class SimulationManager:
    def __init__(self):
        self.net = None
        self.simulation_status = "Initialized"
    
    def start_simulation(self):
        """Starts the Mininet simulation."""
        topo = DisasterResilientSDNTopo()
        self.net = Mininet(topo=topo, controller=lambda name: RemoteController(name='c0'))
        self.net.start()
        self.simulation_status = "Simulation started"
        print(self.simulation_status)
    
    def simulate_failure(self):
        """Simulates a network failure in the SDN."""
        print("Simulating failure: disabling link s1-s2")
        self.net.configLinkStatus('s1', 's2', 'down')  # Disable link
        self.simulation_status = "Link s1-s2 disabled"
        time.sleep(5)  # Simulate some downtime
        self.net.configLinkStatus('s1', 's2', 'up')
        self.simulation_status = "Link s1-s2 restored"
        print(self.simulation_status)
    
    def stop_simulation(self):
        """Stops the Mininet simulation."""
        if self.net:
            CLI(self.net)
            self.net.stop()
        self.simulation_status = "Simulation stopped"
        print(self.simulation_status)
    
    def get_status(self):
        """Returns the current status of the simulation."""
        return self.simulation_status

if __name__ == "__main__":
    setLogLevel('info')
    sim_manager = SimulationManager()
    sim_manager.start_simulation()
    sim_manager.simulate_failure()
    sim_manager.stop_simulation()
