#!/usr/bin/env python3
"""
Advanced WiFi Security Tester - VIP GUI Interface
================================================

Interactive GUI for the Advanced WiFi Security Testing Tool
"""

import os
import sys
import time
import threading
import subprocess
from wifi_advanced_tester import AdvancedWiFiTester

class AdvancedWiFiGUI:
    def __init__(self):
        self.tester = AdvancedWiFiTester()
        self.interface = None
        self.target_ip = None
        self.target_bssid = None
        self.gateway_ip = None
        self.targets = []
        self.attack_thread = None
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def main_menu(self):
        """Display main menu"""
        while True:
            self.clear_screen()
            self.tester.banner()
            
            print("\n[VIP MAIN MENU]")
            print("=" * 60)
            print("1.  🔧 Setup Interface & Network Info")
            print("2.  🔍 Advanced Network Scanning")
            print("3.  💥 Layer 2 Attacks (WiFi)")
            print("4.  🌊 Layer 3/4 Flood Attacks")
            print("5.  🎯 Targeted Attack Combinations")
            print("6.  📊 Attack Statistics & Monitoring")
            print("7.  ⚙️  Advanced Settings")
            print("8.  ❌ Exit")
            print("=" * 60)
            
            choice = input("\n[?] Select option (1-8): ").strip()
            
            if choice == '1':
                self.setup_menu()
            elif choice == '2':
                self.scanning_menu()
            elif choice == '3':
                self.layer2_attacks_menu()
            elif choice == '4':
                self.flood_attacks_menu()
            elif choice == '5':
                self.combo_attacks_menu()
            elif choice == '6':
                self.statistics_menu()
            elif choice == '7':
                self.settings_menu()
            elif choice == '8':
                self.exit_program()
            else:
                input("[!] Invalid option! Press Enter to continue...")
    
    def setup_menu(self):
        """Setup interface and network information"""
        self.clear_screen()
        print("[🔧 INTERFACE & NETWORK SETUP]")
        print("=" * 50)
        
        # Get available interfaces
        interfaces = self.tester.get_interfaces() if hasattr(self.tester, 'get_interfaces') else []
        
        # Show network interfaces
        result = subprocess.run(['ip', 'link', 'show'], capture_output=True, text=True)
        print("\n[+] Available Network Interfaces:")
        interfaces = []
        for line in result.stdout.split('\n'):
            if ': ' in line and 'lo:' not in line:
                interface = line.split(':')[1].strip().split('@')[0]
                interfaces.append(interface)
                print(f"  - {interface}")
        
        if not interfaces:
            print("[!] No network interfaces found!")
            input("Press Enter to continue...")
            return
        
        interface = input(f"\n[?] Enter interface name: ").strip()
        if interface not in interfaces:
            print("[!] Invalid interface!")
            input("Press Enter to continue...")
            return
        
        self.interface = interface
        print(f"[+] Selected interface: {interface}")
        
        # Get network information
        print("\n[*] Getting network information...")
        self.tester.get_network_info(interface)
        self.target_ip = self.tester.target_ip
        self.gateway_ip = self.tester.gateway_ip
        
        input("\nPress Enter to continue...")
    
    def scanning_menu(self):
        """Advanced scanning menu"""
        if not self.interface:
            print("[!] Please setup interface first!")
            input("Press Enter to continue...")
            return
        
        self.clear_screen()
        print("[🔍 ADVANCED NETWORK SCANNING]")
        print("=" * 50)
        print("1. Quick Network Scan (ping sweep)")
        print("2. Port Scan on Targets")
        print("3. WiFi Networks Scan")
        print("4. ARP Table Discovery")
        print("5. Back to Main Menu")
        
        choice = input("\n[?] Select scan type (1-5): ").strip()
        
        if choice == '1':
            if self.tester.network_range:
                print(f"\n[*] Scanning network: {self.tester.network_range}")
                self.targets = self.tester.scan_targets(self.tester.network_range)
                if self.targets:
                    print(f"[+] Found {len(self.targets)} live targets:")
                    for i, target in enumerate(self.targets):
                        print(f"  {i+1}. {target}")
        
        elif choice == '2':
            if self.targets:
                target = input("[?] Enter target IP: ").strip()
                if target in self.targets:
                    print(f"[*] Scanning ports on {target}...")
                    subprocess.run(['nmap', '-F', target])
        
        elif choice == '3':
            print("[*] Scanning WiFi networks...")
            subprocess.run(['iwlist', self.interface, 'scan'])
        
        elif choice == '4':
            print("[*] ARP table:")
            subprocess.run(['arp', '-a'])
        
        elif choice == '5':
            return
        
        input("\nPress Enter to continue...")
    
    def layer2_attacks_menu(self):
        """Layer 2 WiFi attacks menu"""
        self.clear_screen()
        print("[💥 LAYER 2 ATTACKS (WiFi)]")
        print("=" * 50)
        print("1. Advanced Deauthentication Attack")
        print("2. ARP Poisoning/Spoofing")
        print("3. DHCP Discover Flood")
        print("4. Advanced Beacon Flooding")
        print("5. Back to Main Menu")
        
        choice = input("\n[?] Select attack (1-5): ").strip()
        
        if choice == '1':
            self.deauth_attack_config()
        elif choice == '2':
            self.arp_poison_config()
        elif choice == '3':
            self.dhcp_flood_config()
        elif choice == '4':
            self.beacon_flood_config()
        elif choice == '5':
            return
    
    def flood_attacks_menu(self):
        """Layer 3/4 flood attacks menu"""
        self.clear_screen()
        print("[🌊 LAYER 3/4 FLOOD ATTACKS]")
        print("=" * 50)
        print("1. UDP Flood Attack")
        print("2. TCP SYN Flood Attack")
        print("3. ICMP Flood Attack")
        print("4. DNS Amplification Attack")
        print("5. Bandwidth Consumption Attack")
        print("6. Back to Main Menu")
        
        choice = input("\n[?] Select attack (1-6): ").strip()
        
        if choice == '1':
            self.udp_flood_config()
        elif choice == '2':
            self.syn_flood_config()
        elif choice == '3':
            self.icmp_flood_config()
        elif choice == '4':
            self.dns_amp_config()
        elif choice == '5':
            self.bandwidth_attack_config()
        elif choice == '6':
            return
    
    def combo_attacks_menu(self):
        """Combination attacks menu"""
        self.clear_screen()
        print("[🎯 TARGETED ATTACK COMBINATIONS]")
        print("=" * 50)
        print("1. Full WiFi Disruption (Deauth + Beacon Flood)")
        print("2. Network Takeover (ARP Poison + DHCP Flood)")
        print("3. Bandwidth Exhaustion (UDP + ICMP + SYN)")
        print("4. DNS Infrastructure Attack")
        print("5. Custom Multi-Attack")
        print("6. Back to Main Menu")
        
        choice = input("\n[?] Select combination (1-6): ").strip()
        
        if choice == '1':
            self.wifi_disruption_combo()
        elif choice == '2':
            self.network_takeover_combo()
        elif choice == '3':
            self.bandwidth_exhaustion_combo()
        elif choice == '4':
            self.dns_infrastructure_combo()
        elif choice == '5':
            self.custom_multi_attack()
        elif choice == '6':
            return
    
    def deauth_attack_config(self):
        """Configure deauth attack"""
        print("\n[💥 ADVANCED DEAUTH ATTACK CONFIG]")
        
        bssid = input("[?] Target BSSID (MAC address): ").strip()
        if not bssid:
            print("[!] BSSID required!")
            return
        
        threads = input("[?] Number of threads (default 10): ").strip()
        threads = int(threads) if threads else 10
        
        count = input("[?] Packet count (0 for unlimited): ").strip()
        count = int(count) if count else 0
        
        print(f"\n[*] Starting advanced deauth attack...")
        print(f"[*] Target: {bssid}")
        print(f"[*] Threads: {threads}")
        print(f"[*] Press Ctrl+C to stop")
        
        try:
            self.tester.running = True
            self.tester.advanced_deauth_attack(self.interface, bssid, threads, count)
        except KeyboardInterrupt:
            print("\n[*] Attack stopped by user")
        
        input("Press Enter to continue...")
    
    def udp_flood_config(self):
        """Configure UDP flood attack"""
        print("\n[🌊 UDP FLOOD ATTACK CONFIG]")
        
        target = input("[?] Target IP address: ").strip()
        if not target:
            print("[!] Target IP required!")
            return
        
        port = input("[?] Target port (default 80): ").strip()
        port = int(port) if port else 80
        
        threads = input("[?] Number of threads (default 50): ").strip()
        threads = int(threads) if threads else 50
        
        size = input("[?] Packet size in bytes (default 1024): ").strip()
        size = int(size) if size else 1024
        
        print(f"\n[*] Starting UDP flood attack...")
        print(f"[*] Target: {target}:{port}")
        print(f"[*] Threads: {threads}")
        print(f"[*] Packet size: {size} bytes")
        print(f"[*] Press Ctrl+C to stop")
        
        try:
            self.tester.running = True
            self.tester.udp_flood_attack(target, port, threads, size)
            
            while self.tester.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[*] Attack stopped by user")
        
        input("Press Enter to continue...")
    
    def wifi_disruption_combo(self):
        """Full WiFi disruption combination attack"""
        print("\n[🎯 FULL WiFi DISRUPTION COMBO]")
        
        bssid = input("[?] Target BSSID: ").strip()
        if not bssid:
            print("[!] BSSID required!")
            return
        
        print(f"\n[*] Starting WiFi disruption combo attack...")
        print(f"[*] Phase 1: Advanced Deauth Attack")
        print(f"[*] Phase 2: Beacon Flooding")
        print(f"[*] Press Ctrl+C to stop")
        
        try:
            self.tester.running = True
            
            # Start deauth attack in background
            deauth_thread = threading.Thread(
                target=self.tester.advanced_deauth_attack,
                args=(self.interface, bssid, 5, 0)
            )
            deauth_thread.daemon = True
            deauth_thread.start()
            
            # Start beacon flooding
            beacon_thread = threading.Thread(
                target=self.tester.advanced_beacon_flood,
                args=(self.interface, 10, 0)
            )
            beacon_thread.daemon = True
            beacon_thread.start()
            
            while self.tester.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n[*] Combo attack stopped by user")
        
        input("Press Enter to continue...")
    
    def statistics_menu(self):
        """Show attack statistics"""
        self.clear_screen()
        print("[📊 ATTACK STATISTICS & MONITORING]")
        print("=" * 50)
        
        if hasattr(self.tester, 'packet_count'):
            print(f"Total packets sent: {self.tester.packet_count}")
            
            if hasattr(self.tester, 'start_time') and self.tester.start_time:
                elapsed = time.time() - self.tester.start_time
                pps = self.tester.packet_count / elapsed if elapsed > 0 else 0
                print(f"Packets per second: {pps:.2f}")
                print(f"Attack duration: {elapsed:.1f} seconds")
        
        print(f"Active threads: {len(self.tester.threads)}")
        print(f"Interface: {self.interface or 'Not set'}")
        print(f"Target IP: {self.target_ip or 'Not set'}")
        print(f"Gateway IP: {self.gateway_ip or 'Not set'}")
        print(f"Targets found: {len(self.targets)}")
        
        input("\nPress Enter to continue...")
    
    def settings_menu(self):
        """Advanced settings menu"""
        self.clear_screen()
        print("[⚙️ ADVANCED SETTINGS]")
        print("=" * 50)
        print(f"1. Thread Count: {self.tester.thread_count}")
        print(f"2. Interface: {self.interface or 'Not set'}")
        print(f"3. Target IP: {self.target_ip or 'Not set'}")
        print("4. Reset All Settings")
        print("5. Back to Main Menu")
        
        choice = input("\n[?] Select option (1-5): ").strip()
        
        if choice == '1':
            threads = input(f"[?] New thread count (current: {self.tester.thread_count}): ").strip()
            if threads:
                self.tester.thread_count = int(threads)
                print(f"[+] Thread count set to {threads}")
        
        elif choice == '4':
            self.interface = None
            self.target_ip = None
            self.target_bssid = None
            self.gateway_ip = None
            self.targets = []
            print("[+] All settings reset")
        
        elif choice == '5':
            return
        
        input("Press Enter to continue...")
    
    def exit_program(self):
        """Exit program with cleanup"""
        print("\n[*] Stopping all attacks and cleaning up...")
        self.tester.stop_all_attacks()
        print("[+] Goodbye!")
        sys.exit(0)

def main():
    # Check root privileges
    if os.geteuid() != 0:
        print("[!] This tool requires root privileges!")
        print("[!] Please run with sudo")
        sys.exit(1)
    
    try:
        gui = AdvancedWiFiGUI()
        gui.main_menu()
    except KeyboardInterrupt:
        print("\n[*] Interrupted by user")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        print("[*] Cleaning up...")

if __name__ == "__main__":
    main()