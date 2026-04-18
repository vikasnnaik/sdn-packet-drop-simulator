# 📦 Packet Drop Simulator using SDN (Mininet + POX)

## 📌 Project Overview

This project demonstrates a **Software Defined Networking (SDN)** based packet drop simulator using **Mininet** and **POX controller**. The system selectively drops ICMP packets between specific hosts (h1 ↔ h2) and blocks TCP port 80 traffic while allowing normal communication between other hosts.

---

## 🎯 Objective

* Simulate a virtual network using Mininet with 3 hosts and 1 switch
* Implement SDN controller using POX with custom drop logic
* Apply packet drop rules between specific hosts (h1 and h2)
* Block TCP traffic on port 80 (HTTP)
* Analyze network behavior (packet loss, connectivity, bandwidth)

---

## 🛠️ Technologies Used

* Mininet (Network Emulator)
* POX Controller (SDN Controller)
* OpenFlow Protocol
* Python 3
* Ubuntu (VMware)

---

## 🧠 Concept

In SDN, the **control plane** is separated from the **data plane**.
The controller installs flow rules in switches to control traffic behavior.

In this project:

* Normal network → All packets allowed (h1 ↔ h3 works)
* Modified rules → Selected packets dropped (h1 ↔ h2 blocked)
* Port-based blocking → TCP port 80 traffic dropped

---

## ⚙️ Setup Instructions

### 1. Install Mininet

```bash
sudo apt update
sudo apt install mininet -y
2. Install POX Controller
bash
sudo apt install git -y
git clone https://github.com/noxrepo/pox
cd pox
3. Copy Controller File
bash
cp controller/drop_controller.py ~/pox/pox/misc/
▶️ Execution Steps
Step 1: Start Controller (Terminal 1)
bash
cd ~/pox
./pox.py misc.drop_controller
Expected Output:

text
==================================================
Packet Drop Controller Started - Project 17
==================================================
Active drop rules:
  * drop_icmp_h1_h2: Drop ICMP from h1 to h2
  * drop_tcp_port_80: Drop all TCP port 80 traffic
  * drop_icmp_h2_h1: Drop ICMP from h2 to h1
==================================================
Step 2: Run Mininet (Terminal 2)
bash
sudo mn --controller=remote,ip=127.0.0.1,port=6633 --topo=single,3 --mac
Step 3: Test Connectivity
bash
mininet> pingall
Expected Output:

text
h1 -> X h3
h2 -> X h3
h3 -> h1 h2
Results: 33% dropped (4/6 received)
🚫 Packet Drop Implementation
Block ICMP traffic between h1 and h2
The POX controller applies these drop rules:

python
Rule 1: ICMP from 10.0.0.1 → 10.0.0.2 = DROP
Rule 2: ICMP from 10.0.0.2 → 10.0.0.1 = DROP
Rule 3: TCP port 80 (any source/destination) = DROP
Test blocked traffic
bash
mininet> h2 ping h1 -c 3
Expected:

text
3 packets transmitted, 0 received, 100% packet loss
Test allowed traffic
bash
mininet> h1 ping h3 -c 3
Expected:

text
3 packets transmitted, 3 received, 0% packet loss
📊 Results
Scenario	Command	Result
Normal Network (h1→h3)	h1 ping h3	0% packet loss ✅
Blocked Traffic (h2→h1)	h2 ping h1	100% packet loss ✅
After Applying Rule	pingall	33% dropped ✅
TCP Bandwidth	iperf h1 h2	24.5 Mbits/sec ✅
Port 80 Block	curl :80	Connection refused ✅
📸 Proof of Execution
Include screenshots of:

✅ POX controller startup with drop rules

✅ Mininet topology (nodes, net commands)

✅ h2 ping h1 (100% packet loss)

✅ h1 ping h3 (0% packet loss)

✅ pingall (33% dropped)

✅ iperf bandwidth results

✅ Flow table dump (ovs-ofctl dump-flows s1)

📈 Analysis
SDN allows centralized control of network behavior through a single controller

Packet dropping successfully simulates firewall and security policies

Flow rules dynamically affect network traffic without hardware changes

ICMP blocking demonstrates protocol-specific filtering

Port 80 blocking shows application-layer traffic control

Normal traffic (h1↔h3) remains unaffected, proving selective filtering

🌍 Applications
Network Security (Firewall)

Traffic Engineering

QoS Management

Intrusion Detection Systems

Access Control Lists (ACL)

DDoS Attack Mitigation

⚠️ Challenges Faced
Ryu compatibility issues with newer Python versions (switched to POX)

Controller connection errors (ensured controller starts before Mininet)

Port conflicts (used port 6633)

xterm display issues in VM (used direct Mininet CLI commands)

🔚 Conclusion
This project successfully demonstrates how SDN can be used to control and manipulate network traffic dynamically. The POX controller effectively drops ICMP packets between specific hosts (h1 and h2) and blocks TCP port 80 traffic while allowing all other communication. The packet dropping behavior highlights the flexibility and power of centralized network control for implementing security policies.

📚 References
https://mininet.org

https://github.com/noxrepo/pox

OpenFlow Documentation

SDN Research Papers

Mininet Walkthrough Guide

👨‍💻 Author
Vikas N Naik
