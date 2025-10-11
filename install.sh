#!/bin/bash

# WiFi Security Tester Installation Script
# ========================================

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                WiFi Security Tester Installer                ║"
echo "║                                                              ║"
echo "║  WARNING: FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY!      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "[!] Please don't run this installer as root!"
   echo "[!] Run as normal user, sudo will be used when needed"
   exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install packages on different distributions
install_packages() {
    echo "[*] Installing system packages..."
    
    if command_exists apt-get; then
        # Debian/Ubuntu
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip aircrack-ng wireless-tools net-tools
    elif command_exists yum; then
        # CentOS/RHEL
        sudo yum install -y python3 python3-pip aircrack-ng wireless-tools net-tools
    elif command_exists dnf; then
        # Fedora
        sudo dnf install -y python3 python3-pip aircrack-ng wireless-tools net-tools
    elif command_exists pacman; then
        # Arch Linux
        sudo pacman -S --noconfirm python python-pip aircrack-ng wireless_tools net-tools
    else
        echo "[!] Unsupported package manager. Please install manually:"
        echo "    - python3"
        echo "    - python3-pip"
        echo "    - aircrack-ng"
        echo "    - wireless-tools"
        echo "    - net-tools"
        exit 1
    fi
}

# Function to install Python dependencies
install_python_deps() {
    echo "[*] Installing Python dependencies..."
    
    # Upgrade pip
    python3 -m pip install --upgrade pip
    
    # Install requirements
    if [[ -f "requirements.txt" ]]; then
        python3 -m pip install -r requirements.txt
    else
        # Fallback installation
        python3 -m pip install scapy>=2.4.5
    fi
}

# Function to make scripts executable
make_executable() {
    echo "[*] Making scripts executable..."
    chmod +x wifi_security_tester.py
    chmod +x wifi_tester_gui.py
    chmod +x install.sh
}

# Function to create desktop shortcut (optional)
create_shortcut() {
    read -p "[?] Create desktop shortcut? (y/N): " create_shortcut
    if [[ $create_shortcut =~ ^[Yy]$ ]]; then
        DESKTOP_FILE="$HOME/Desktop/WiFi-Security-Tester.desktop"
        CURRENT_DIR=$(pwd)
        
        cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=WiFi Security Tester
Comment=WiFi Security Testing Tool
Exec=sudo python3 $CURRENT_DIR/wifi_tester_gui.py
Icon=network-wireless
Terminal=true
Categories=Network;Security;
EOF
        
        chmod +x "$DESKTOP_FILE"
        echo "[+] Desktop shortcut created: $DESKTOP_FILE"
    fi
}

# Function to check wireless adapter
check_wireless() {
    echo "[*] Checking wireless interfaces..."
    
    if command_exists iwconfig; then
        INTERFACES=$(iwconfig 2>/dev/null | grep "IEEE 802.11" | awk '{print $1}')
        
        if [[ -z "$INTERFACES" ]]; then
            echo "[!] No wireless interfaces found!"
            echo "[!] Please ensure you have a compatible WiFi adapter"
        else
            echo "[+] Found wireless interfaces:"
            for iface in $INTERFACES; do
                echo "    - $iface"
            done
        fi
    else
        echo "[!] iwconfig not found. Cannot check wireless interfaces."
    fi
}

# Main installation process
main() {
    echo "[*] Starting installation..."
    echo
    
    # Install system packages
    install_packages
    
    # Install Python dependencies
    install_python_deps
    
    # Make scripts executable
    make_executable
    
    # Check wireless adapters
    check_wireless
    
    # Create desktop shortcut (optional)
    create_shortcut
    
    echo
    echo "[+] Installation completed!"
    echo
    echo "Usage:"
    echo "  Command line: sudo python3 wifi_security_tester.py --help"
    echo "  Interactive:  sudo python3 wifi_tester_gui.py"
    echo
    echo "Important notes:"
    echo "  - Always run with sudo (root privileges required)"
    echo "  - Only test networks you own or have permission to test"
    echo "  - Make sure your WiFi adapter supports monitor mode"
    echo
    echo "Recommended WiFi adapters for penetration testing:"
    echo "  - Alfa AWUS036ACS"
    echo "  - Panda PAU09"
    echo "  - TP-Link AC600 T2U Plus"
    echo
}

# Run main function
main