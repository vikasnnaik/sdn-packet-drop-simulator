# 📦 Packet Drop Simulator using SDN (Mininet + POX)

## 📌 Project Overview

This project demonstrates a **Software Defined Networking (SDN)** based packet drop simulator using **Mininet** and **POX controller**. The system simulates network behavior and applies flow rules to selectively drop packets between hosts.

---

## 🎯 Objective

* Simulate a virtual network using Mininet
* Implement SDN controller using POX
* Apply packet drop rules between specific hosts
* Analyze network behavior (packet loss, connectivity)

---

## 🛠️ Technologies Used

* Mininet (Network Emulator)
* POX Controller (SDN Controller)
* OpenFlow Protocol
* Ubuntu (VMware)

---

## 🧠 Concept

In SDN, the **control plane** is separated from the **data plane**.
The controller installs flow rules in switches to control traffic behavior.

In this project:

* Normal network → All packets allowed
* Modified rules → Selected packets dropped

---

## ⚙️ Setup Instructions

### 1. Install Mininet

```bash
sudo apt update
sudo apt install mininet -y
```

### 2. Install POX Controller

```bash
sudo apt install git -y
git clone https://github.com/noxrepo/pox
cd pox
```

---

## ▶️ Execution Steps

### Step 1: Start Controller

```bash
cd pox
./pox.py forwarding.hub
```

### Step 2: Run Mininet (New Terminal)

```bash
sudo mn --topo single,3 --controller remote
```

### Step 3: Test Connectivity

```bash
pingall
```

Expected Output:

```
0% dropped
```

---

## 🚫 Packet Drop Implementation

### Block traffic from h1 → h2

```bash
h1 iptables -A OUTPUT -d 10.0.0.2 -j DROP
```

### Test again

```bash
h1 ping h2
```

Expected:

* Packet loss observed
* Communication blocked

---

## 📊 Results

| Scenario            | Result               |
| ------------------- | -------------------- |
| Normal Network      | 0% packet loss       |
| After Applying Rule | Packet loss observed |

---

## 📸 Proof of Execution

Include screenshots of:

* Mininet topology
* pingall (0% loss)
* Packet drop result
* Controller running
* Flow/iptables rules

---

## 📈 Analysis

* SDN allows centralized control of network behavior
* Packet dropping simulates firewall and congestion control
* Flow rules dynamically affect network traffic

---

## 🌍 Applications

* Network Security (Firewall)
* Traffic Engineering
* QoS Management
* Intrusion Detection Systems

---

## ⚠️ Challenges Faced

* Ryu compatibility issues with Python 3.12
* Controller connection errors
* Port conflicts (6633)

---

## 🔚 Conclusion

This project successfully demonstrates how SDN can be used to control and manipulate network traffic dynamically. Packet dropping behavior highlights the flexibility and power of centralized network control.

---

## 📚 References

1. https://mininet.org
2. https://github.com/noxrepo/pox
3. OpenFlow Documentation
4. SDN Research Papers

---

## 👨‍💻 Author

Vikas N Naik
