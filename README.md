# WiFi Security Testing Tool

## ⚠️ DISCLAIMER

**THIS TOOL IS FOR EDUCATIONAL AND AUTHORIZED TESTING PURPOSES ONLY!**

- Only use this tool on networks you own or have explicit written permission to test
- Unauthorized use of this tool against networks you don't own is illegal and unethical
- The authors are not responsible for any misuse of this tool
- Always comply with local laws and regulations

## 📋 Description

This is a comprehensive WiFi penetration testing tool written in Python that implements various attack methods to test the security of wireless networks. The tool is designed for security professionals, network administrators, and researchers to assess the security of their own WiFi networks.

## ✨ Features

### Attack Methods
1. **Deauthentication Attack** - Disconnects clients from target network
2. **Beacon Flooding** - Creates fake access points to clutter the airwaves
3. **Authentication Flooding** - Overwhelms AP with authentication requests
4. **Probe Request Flooding** - Floods network with probe requests

### Additional Features
- Network scanning and discovery
- Monitor mode setup and management
- Multiple interface support
- Configurable packet counts and timing
- Real-time attack statistics
- Automatic cleanup and interface restoration

## 🔧 Requirements

### System Requirements
- Linux operating system (Ubuntu/Debian/Kali recommended)
- Root privileges (sudo access)
- Wireless network interface capable of monitor mode

### Software Dependencies
- Python 3.6+
- aircrack-ng suite
- Scapy library

### Hardware Requirements
- WiFi adapter that supports monitor mode and packet injection
- Recommended adapters:
  - Alfa AWUS036ACS
  - Panda PAU09
  - TP-Link AC600 T2U Plus

## 📦 Installation

1. **Clone or download the tool:**
   ```bash
   git clone <repository-url>
   cd wifi-security-tester
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install aircrack-ng suite:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install aircrack-ng
   
   # Arch Linux
   sudo pacman -S aircrack-ng
   
   # CentOS/RHEL
   sudo yum install aircrack-ng
   ```

4. **Make the script executable:**
   ```bash
   chmod +x wifi_security_tester.py
   ```

## 🚀 Usage

### Basic Usage

1. **Run with root privileges:**
   ```bash
   sudo python3 wifi_security_tester.py
   ```

2. **Scan for networks:**
   ```bash
   sudo python3 wifi_security_tester.py --scan
   ```

### Attack Examples

#### Deauthentication Attack
```bash
# Target all clients on a network
sudo python3 wifi_security_tester.py --deauth -t AA:BB:CC:DD:EE:FF

# Target specific client
sudo python3 wifi_security_tester.py --deauth -t AA:BB:CC:DD:EE:FF -c 11:22:33:44:55:66

# Limited packet count
sudo python3 wifi_security_tester.py --deauth -t AA:BB:CC:DD:EE:FF --count 100
```

#### Beacon Flooding
```bash
# Create 1000 fake access points
sudo python3 wifi_security_tester.py --beacon-flood --count 1000

# Continuous beacon flooding (Ctrl+C to stop)
sudo python3 wifi_security_tester.py --beacon-flood
```

#### Authentication Flooding
```bash
# Flood target AP with auth requests
sudo python3 wifi_security_tester.py --auth-flood -t AA:BB:CC:DD:EE:FF --count 5000
```

#### Probe Request Flooding
```bash
# Flood with probe requests for specific SSID
sudo python3 wifi_security_tester.py --probe-flood --ssid "TargetNetwork" --count 2000
```

### Advanced Options

```bash
# Specify interface and channel
sudo python3 wifi_security_tester.py --deauth -i wlan0 -t AA:BB:CC:DD:EE:FF --channel 6

# Scan with custom duration
sudo python3 wifi_security_tester.py --scan --duration 30

# Interactive mode (scan and select target)
sudo python3 wifi_security_tester.py --deauth
```

## 📖 Command Line Options

```
-h, --help            Show help message
-i, --interface       Wireless interface to use
-s, --scan           Scan for networks
-t, --target         Target BSSID
--ssid               Target SSID
-c, --client         Target client MAC (for deauth)
--channel            Channel to use
--count              Number of packets to send (0 = unlimited)
--duration           Scan duration in seconds

Attack Types:
--deauth             Deauthentication attack
--beacon-flood       Beacon flooding attack
--auth-flood         Authentication flooding attack
--probe-flood        Probe request flooding attack
```

## 🛡️ Legal and Ethical Guidelines

### Legal Use Cases
- Testing your own home/office network
- Authorized penetration testing with written permission
- Educational purposes in controlled environments
- Security research with proper authorization

### Illegal Use Cases
- Testing networks without permission
- Disrupting public WiFi services
- Attacking networks in public spaces
- Any malicious use against others

### Best Practices
1. Always obtain written permission before testing
2. Document all testing activities
3. Use in isolated/controlled environments
4. Respect privacy and data protection laws
5. Report vulnerabilities responsibly

## 🔍 How It Works

### Deauthentication Attack
Sends deauthentication frames to disconnect clients from the target access point. This exploits the lack of authentication in management frames in older WiFi standards.

### Beacon Flooding
Creates numerous fake access points by sending beacon frames with random SSIDs and BSSIDs, making it difficult for users to identify legitimate networks.

### Authentication Flooding
Overwhelms the target access point with authentication requests from random MAC addresses, potentially causing denial of service.

### Probe Request Flooding
Sends numerous probe requests for the target SSID, which can be used to test how the network handles high volumes of probe requests.

## 🛠️ Troubleshooting

### Common Issues

1. **"No wireless interfaces found"**
   - Ensure your WiFi adapter is connected and recognized
   - Check with `iwconfig` command

2. **"Failed to set monitor mode"**
   - Try different wireless adapter
   - Ensure aircrack-ng is properly installed
   - Kill conflicting processes: `sudo airmon-ng check kill`

3. **"Permission denied"**
   - Run with sudo/root privileges
   - Check file permissions

4. **"Interface not found"**
   - List available interfaces: `iwconfig`
   - Use correct interface name

### Interface Restoration
If your interface gets stuck in monitor mode:
```bash
sudo airmon-ng stop wlan0mon
sudo systemctl restart NetworkManager
```

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚖️ Responsible Disclosure

If you discover vulnerabilities while using this tool:
1. Do not exploit them maliciously
2. Report to the network owner
3. Follow responsible disclosure practices
4. Consider coordinated disclosure timelines

## 📞 Support

For questions, issues, or contributions:
- Create an issue on GitHub
- Follow responsible disclosure for security issues
- Provide detailed information for bug reports

---

**Remember: With great power comes great responsibility. Use this tool ethically and legally!**