"""
Custom Mininet Topology for Packet Drop Testing
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.node import RemoteController, OVSSwitch

class DropTestTopology(Topo):
    """
    Simple topology:
    
        h1 -- s1 -- h2
               |
               h3
    """
    
    def build(self):
        # Add switches
        s1 = self.addSwitch('s1')
        
        # Add hosts
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')
        h3 = self.addHost('h3', ip='10.0.0.3/24')
        
        # Add links
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)
        
class LinearTopology(Topo):
    """Linear topology: h1 - s1 - s2 - h2"""
    
    def build(self, n=2):
        switches = []
        
        # Add switches
        for i in range(n):
            switches.append(self.addSwitch(f's{i+1}'))
            
        # Add links between switches
        for i in range(n-1):
            self.addLink(switches[i], switches[i+1])
            
        # Add hosts
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        self.addLink(h1, switches[0])
        
        h2 = self.addHost('h2', ip='10.0.0.2/24')
        self.addLink(h2, switches[-1])
        
        h3 = self.addHost('h3', ip='10.0.0.3/24')
        self.addLink(h3, switches[0])

def run_topology(controller_ip='127.0.0.1', topology_type='star'):
    """Run the Mininet topology with remote controller"""
    
    setLogLevel('info')
    
    if topology_type == 'star':
        topo = DropTestTopology()
    else:
        topo = LinearTopology()
        
    net = Mininet(
        topo=topo,
        controller=lambda name: RemoteController(name, ip=controller_ip, port=6653),
        switch=OVSSwitch
    )
    
    net.start()
    print("\n=== Topology Started ===")
    print("Available hosts: h1, h2, h3")
    print("Switch: s1")
    print("\nUseful commands:")
    print("  pingall - Test connectivity between all hosts")
    print("  h1 ping h2 - Ping from h1 to h2")
    print("  iperf h1 h2 - Test bandwidth")
    print("\n" + "="*40)
    
    CLI(net)
    net.stop()

if __name__ == '__main__':
    import sys
    controller_ip = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
    run_topology(controller_ip)
