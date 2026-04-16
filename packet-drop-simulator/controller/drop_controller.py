"""
SDN Packet Drop Simulator Controller
Project 17: Packet Drop Simulator using Ryu Controller
"""

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ipv4, tcp, udp, icmp
from ryu.lib import hub
import time
from collections import defaultdict

class PacketDropController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(PacketDropController, self).__init__(*args, **kwargs)
        
        # Drop rules configuration
        self.drop_rules = []
        self.dropped_packets_log = []
        self.stats = defaultdict(int)
        
        # Initialize default drop rules (modify as needed)
        self.init_drop_rules()
        
        # Start monitoring thread
        self.monitor_thread = hub.spawn(self._monitor_stats)
        
    def init_drop_rules(self):
        """Initialize packet drop rules - Configure based on your needs"""
        self.drop_rules = [
            # Rule 1: Drop ICMP (ping) between specific hosts
            {
                'name': 'drop_icmp_h1_h2',
                'protocol': 'icmp',
                'src_ip': '10.0.0.1',
                'dst_ip': '10.0.0.2',
                'active': True,
                'description': 'Drop ICMP from h1 to h2'
            },
            # Rule 2: Drop TCP port 80 (HTTP) traffic
            {
                'name': 'drop_tcp_port_80',
                'protocol': 'tcp',
                'dst_port': 80,
                'active': True,
                'description': 'Drop all TCP port 80 traffic'
            },
            # Rule 3: Drop UDP traffic from specific source
            {
                'name': 'drop_udp_h1',
                'protocol': 'udp',
                'src_ip': '10.0.0.1',
                'active': False,  # Initially disabled - can enable dynamically
                'description': 'Drop UDP from h1'
            }
        ]
        
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        """Handle switch connection and install default table-miss flow"""
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        
        # Install table-miss flow entry
        actions = []
        match = parser.OFPMatch()
        self.add_flow(datapath, 0, match, actions, timeout=0)
        
        self.logger.info(f"Switch {datapath.id} connected")
        
    def add_flow(self, datapath, priority, match, actions, idle_timeout=0, hard_timeout=0):
        """Add a flow entry to the switch"""
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        
        mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=priority,
            match=match,
            instructions=inst,
            idle_timeout=idle_timeout,
            hard_timeout=hard_timeout
        )
        datapath.send_msg(mod)
        
    def install_drop_flow(self, datapath, match, rule_name):
        """Install a drop flow rule (no actions = drop)"""
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        
        # Drop rule with high priority (100)
        actions = []  # Empty actions = drop packet
        self.add_flow(datapath, 100, match, actions)
        
        self.logger.info(f"DROP FLOW INSTALLED: {rule_name} - Match: {match}")
        
    def create_match_from_rule(self, rule, parser):
        """Create OFPMatch object from rule configuration"""
        match_params = {}
        
        if rule.get('protocol') == 'icmp':
            match_params['eth_type'] = 0x0800
            match_params['ip_proto'] = 1
        elif rule.get('protocol') == 'tcp':
            match_params['eth_type'] = 0x0800
            match_params['ip_proto'] = 6
            if rule.get('dst_port'):
                match_params['tcp_dst'] = rule['dst_port']
            if rule.get('src_port'):
                match_params['tcp_src'] = rule['src_port']
        elif rule.get('protocol') == 'udp':
            match_params['eth_type'] = 0x0800
            match_params['ip_proto'] = 17
            if rule.get('dst_port'):
                match_params['udp_dst'] = rule['dst_port']
                
        if rule.get('src_ip'):
            match_params['ipv4_src'] = rule['src_ip']
        if rule.get('dst_ip'):
            match_params['ipv4_dst'] = rule['dst_ip']
            
        return parser.OFPMatch(**match_params) if match_params else None
        
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        """Handle incoming packets - decide to drop or forward"""
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']
        
        # Parse the packet
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        ip_pkt = pkt.get_protocol(ipv4.ipv4)
        
        if not ip_pkt:
            # Non-IP packet - forward normally
            self._forward_packet(datapath, in_port, msg, pkt)
            return
            
        # Check drop rules
        should_drop = False
        matched_rule = None
        
        for rule in self.drop_rules:
            if not rule.get('active', True):
                continue
                
            # Check protocol match
            if rule.get('protocol') == 'icmp':
                tcp_pkt = pkt.get_protocol(tcp.tcp)
                udp_pkt = pkt.get_protocol(udp.udp)
                icmp_pkt = pkt.get_protocol(icmp.icmp)
                if not icmp_pkt:
                    continue
                    
            elif rule.get('protocol') == 'tcp':
                tcp_pkt = pkt.get_protocol(tcp.tcp)
                if not tcp_pkt:
                    continue
                if rule.get('dst_port') and tcp_pkt.dst_port != rule['dst_port']:
                    continue
                if rule.get('src_port') and tcp_pkt.src_port != rule['src_port']:
                    continue
                    
            elif rule.get('protocol') == 'udp':
                udp_pkt = pkt.get_protocol(udp.udp)
                if not udp_pkt:
                    continue
                if rule.get('dst_port') and udp_pkt.dst_port != rule['dst_port']:
                    continue
                    
            # Check IP addresses
            if rule.get('src_ip') and ip_pkt.src != rule['src_ip']:
                continue
            if rule.get('dst_ip') and ip_pkt.dst != rule['dst_ip']:
                continue
                
            should_drop = True
            matched_rule = rule
            break
            
        if should_drop:
            # Drop the packet - log it
            self._log_dropped_packet(pkt, ip_pkt, matched_rule, datapath.id)
            self.stats['dropped'] += 1
            return  # Packet dropped - no further action
            
        # Forward the packet normally
        self.stats['forwarded'] += 1
        self._forward_packet(datapath, in_port, msg, pkt)
        
    def _forward_packet(self, datapath, in_port, msg, pkt):
        """Forward packet using MAC learning"""
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto
        
        # Simple MAC learning
        eth = pkt.get_protocol(ethernet.ethernet)
        dst = eth.dst
        src = eth.src
        
        # Learn MAC
        self.mac_table = getattr(self, 'mac_table', {})
        self.mac_table[src] = in_port
        
        # Check if destination MAC is known
        if dst in self.mac_table:
            out_port = self.mac_table[dst]
            actions = [parser.OFPActionOutput(out_port)]
        else:
            # Flood if unknown
            actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
            
        # Install flow for future packets (if known destination)
        if dst in self.mac_table:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
            self.add_flow(datapath, 1, match, actions, idle_timeout=30)
            
        # Send packet out
        out = parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=msg.data
        )
        datapath.send_msg(out)
        
    def _log_dropped_packet(self, pkt, ip_pkt, rule, switch_id):
        """Log dropped packet information"""
        log_entry = {
            'timestamp': time.time(),
            'switch': switch_id,
            'src_ip': ip_pkt.src,
            'dst_ip': ip_pkt.dst,
            'protocol': self._get_protocol_name(pkt),
            'rule': rule['name'],
            'rule_description': rule['description']
        }
        self.dropped_packets_log.append(log_entry)
        
        self.logger.warning(
            f"PACKET DROPPED: {ip_pkt.src} -> {ip_pkt.dst} "
            f"Protocol: {log_entry['protocol']} Rule: {rule['name']}"
        )
        
    def _get_protocol_name(self, pkt):
        """Get protocol name from packet"""
        if pkt.get_protocol(tcp.tcp):
            return "TCP"
        elif pkt.get_protocol(udp.udp):
            return "UDP"
        elif pkt.get_protocol(icmp.icmp):
            return "ICMP"
        return "OTHER"
        
    def _monitor_stats(self):
        """Periodic monitoring thread"""
        while True:
            hub.sleep(10)  # Print stats every 10 seconds
            self.logger.info(f"STATS - Forwarded: {self.stats['forwarded']}, Dropped: {self.stats['dropped']}")
            
    def add_drop_rule(self, rule_config):
        """Dynamically add a drop rule"""
        self.drop_rules.append(rule_config)
        self.logger.info(f"New drop rule added: {rule_config['name']}")
        
    def remove_drop_rule(self, rule_name):
        """Remove a drop rule"""
        self.drop_rules = [r for r in self.drop_rules if r['name'] != rule_name]
        self.logger.info(f"Drop rule removed: {rule_name}")
        
    def enable_rule(self, rule_name, enable=True):
        """Enable or disable a drop rule"""
        for rule in self.drop_rules:
            if rule['name'] == rule_name:
                rule['active'] = enable
                self.logger.info(f"Rule {rule_name} {'enabled' if enable else 'disabled'}")
                return
        self.logger.warning(f"Rule {rule_name} not found")
        
    def get_stats(self):
        """Get current statistics"""
        return {
            'forwarded': self.stats['forwarded'],
            'dropped': self.stats['dropped'],
            'total_drops': len(self.dropped_packets_log),
            'active_rules': [r['name'] for r in self.drop_rules if r.get('active', True)]
        }
