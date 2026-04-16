# SDN Packet Drop Simulator - Project 17

## 📋 Project Overview

This project implements an **SDN-based Packet Drop Simulator** using **Mininet** and **POX Controller**. It selectively drops packets based on configurable rules, demonstrating OpenFlow-based network programmability.

### Problem Statement
Implement an SDN controller that can selectively drop packets based on:
- IP addresses (ICMP between specific hosts)
- Protocol types (TCP/UDP/ICMP)
- Port numbers (TCP port 80 blocking)

## ✨ Features

- ✅ **Selective Packet Dropping** - Drop ICMP packets between h1 ↔ h2 (100% loss)
- ✅ **Normal Traffic Flow** - ICMP between h1 ↔ h3 works normally (0% loss)
- ✅ **TCP Port Blocking** - All TCP port 80 traffic is blocked
- ✅ **TCP Bandwidth Working** - iperf test shows ~24-50 Mbits/sec
- ✅ **MAC Learning** - Controller learns MAC addresses for efficient forwarding
- ✅ **OpenFlow Rules** - Dynamic flow rule installation
- ✅ **Packet Logging** - All dropped packets are logged with timestamps
