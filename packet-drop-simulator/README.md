# SDN Packet Drop Simulator

## Project 17: Packet Drop Simulator using SDN

### Problem Statement
Implement an SDN-based packet drop simulator that selectively drops packets based on configurable rules using OpenFlow and Ryu controller.

### Features
- Selective packet dropping based on IP, protocol, port
- Dynamic rule management (add/remove/enable/disable)
- Packet drop logging and statistics
- Two test scenarios: Normal vs Blocked, Dynamic rule changes
- Regression testing for rule persistence

### Prerequisites
- Ubuntu 20.04/22.04
- Mininet
- Ryu Controller
- Python 3.8+

### Installation & Setup

```bash
# Clone repository
git clone https://github.com/yourusername/packet-drop-simulator
cd packet-drop-simulator

# Make scripts executable
chmod +x tests/validation.sh

# Install dependencies
pip3 install -r requirements.txt
# SDN Packet Drop Simulator
