from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink
import time

class DisasterResilientSDNTopo(Topo):
    """
    A custom Mininet topology representing a disaster-resilient SDN network.
    This topology features two switches and two hosts connected in a mesh network,
    demonstrating basic failure recovery using SDN principles.
    """
    def build(self):
        # Add hosts representing endpoints in the network
        h1 = self.addHost('h1')  # Host 1
        h2 = self.addHost('h2')  # Host 2

        # Add SDN-enabled switches for controlling traffic
        s1 = self.addSwitch('s1', cls=OVSSwitch)  # Switch 1
        s2 = self.addSwitch('s2', cls=OVSSwitch)  # Switch 2

        # Create links between hosts and switches with traffic control parameters
        # These parameters (bandwidth, delay, and loss) simulate real-world network conditions
        self.addLink(h1, s1, cls=TCLink, bw=100, delay='5ms', loss=1)
        self.addLink(h2, s2, cls=TCLink, bw=100, delay='5ms', loss=1)

        # Add a primary link between the two switches (with potential to fail)
        self.addLink(s1, s2, cls=TCLink, bw=100, delay='10ms', loss=1)

        # Optional: Add a backup link between the two switches for recovery scenarios
        # This link can be activated if the primary link fails
        self.addLink(s1, s2, cls=TCLink, bw=100, delay='20ms', loss=0)

def simulate_failure(net):
    """
    Simulates a failure scenario by disabling the primary link between switches.
    This allows SDN controllers to reroute traffic via alternate paths, demonstrating
    the adaptability of the network.
    """
    print("*** Simulating a failure: Disabling primary link between s1 and s2")
    net.configLinkStatus('s1', 's2', 'down')  # Disable the link between the switches

    # Wait to simulate network failure duration
    time.sleep(5)

    print("*** Restoring the link between s1 and s2")
    net.configLinkStatus('s1', 's2', 'up')  # Restore the link after failure period

def run():
    """
    The main function that sets up the Mininet network, starts the simulation,
    and provides a command-line interface (CLI) for interacting with the network.
    """
    # Create the custom topology
    topo = DisasterResilientSDNTopo()

    # Initialize the Mininet network with the custom topology, using two remote controllers
    net = Mininet(topo=topo, controller=RemoteController, switch=OVSSwitch, link=TCLink)

    # Add two remote controllers to simulate distributed SDN control
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)
    c1 = net.addController('c1', controller=RemoteController, ip='127.0.0.1', port=6654)

    # Start the network, including all hosts, switches, and controllers
    net.start()

    print("*** Network started. Hosts and switches are now operational.")

    # Optional: Test connectivity before failure simulation
    print("*** Testing network connectivity before failure...")
    net.pingAll()  # Perform a ping test to verify network connectivity

    # Simulate a failure in the network
    simulate_failure(net)

    # Optional: Test connectivity after recovery
    print("*** Testing network connectivity after recovery...")
    net.pingAll()  # Perform another ping test to verify recovery

    # Provide a command-line interface (CLI) for further interaction with the network
    CLI(net)

    # Stop the network and clean up resources after exiting the CLI
    net.stop()

if __name__ == '__main__':
    # Set the Mininet log level to 'info' for detailed output
    setLogLevel('info')

    # Run the network simulation
    run()
