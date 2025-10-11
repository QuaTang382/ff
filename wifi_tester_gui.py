#!/usr/bin/env python3
"""
WiFi Security Tester - Interactive Menu Interface
================================================

Simple interactive menu interface for the WiFi Security Testing Tool
"""

import os
import sys
import subprocess
from wifi_security_tester import WiFiSecurityTester

class WiFiTesterGUI:
    def __init__(self):
        self.tester = WiFiSecurityTester()
        self.interface = None
        self.target_bssid = None
        self.target_ssid = None
        self.networks = {}
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def main_menu(self):
        """Display main menu"""
        while True:
            self.clear_screen()
            self.tester.banner()
            
            print("\n[MAIN MENU]")
            print("1. Setup Interface")
            print("2. Scan Networks")
            print("3. Deauthentication Attack")
            print("4. Beacon Flooding")
            print("5. Authentication Flooding")
            print("6. Probe Request Flooding")
            print("7. View Current Settings")
            print("8. Exit")
            
            choice = input("\n[?] Select option (1-8): ").strip()
            
            if choice == '1':
                self.setup_interface()
            elif choice == '2':
                self.scan_networks()
            elif choice == '3':
                self.deauth_attack_menu()
            elif choice == '4':
                self.beacon_flood_menu()
            elif choice == '5':
                self.auth_flood_menu()
            elif choice == '6':
                self.probe_flood_menu()
            elif choice == '7':
                self.show_settings()
            elif choice == '8':
                self.exit_program()
            else:
                input("[!] Invalid option! Press Enter to continue...")
    
    def setup_interface(self):
        """Setup wireless interface"""
        self.clear_screen()
        print("[INTERFACE SETUP]")
        
        # Get available interfaces
        interfaces = self.tester.get_interfaces()
        if not interfaces:
            print("[!] No wireless interfaces found!")
            input("Press Enter to continue...")
            return
        
        print("\n[+] Available wireless interfaces:")
        for i, iface in enumerate(interfaces):
            print(f"  {i+1}. {iface}")
        
        try:
            choice = int(input("\n[?] Select interface (number): ")) - 1
            selected_interface = interfaces[choice]
        except (ValueError, IndexError):
            print("[!] Invalid selection!")
            input("Press Enter to continue...")
            return
        
        print(f"\n[*] Setting up {selected_interface}...")
        monitor_interface = self.tester.set_monitor_mode(selected_interface)
        
        if monitor_interface:
            self.interface = monitor_interface
            print(f"[+] Monitor mode enabled on {monitor_interface}")
        else:
            print("[!] Failed to set monitor mode!")
        
        input("Press Enter to continue...")
    
    def scan_networks(self):
        """Scan for networks"""
        if not self.interface:
            print("[!] Please setup interface first!")
            input("Press Enter to continue...")
            return
        
        self.clear_screen()
        print("[NETWORK SCANNING]")
        
        duration = input("[?] Scan duration in seconds (default 10): ").strip()
        if not duration:
            duration = 10
        else:
            try:
                duration = int(duration)
            except ValueError:
                duration = 10
        
        print(f"\n[*] Scanning for {duration} seconds...")
        self.networks = self.tester.scan_networks(self.interface, duration)
        
        if self.networks:
            self.tester.display_networks(self.networks)
            
            choice = input("\n[?] Select target network (number, or Enter to skip): ").strip()
            if choice:
                try:
                    target_index = int(choice) - 1
                    target_bssid = list(self.networks.keys())[target_index]
                    target_info = self.networks[target_bssid]
                    
                    self.target_bssid = target_bssid
                    self.target_ssid = target_info['ssid']
                    
                    print(f"[+] Target set: {self.target_ssid} ({self.target_bssid})")
                except (ValueError, IndexError):
                    print("[!] Invalid selection!")
        else:
            print("[!] No networks found!")
        
        input("Press Enter to continue...")
    
    def deauth_attack_menu(self):
        """Deauthentication attack menu"""
        if not self.interface:
            print("[!] Please setup interface first!")
            input("Press Enter to continue...")
            return
        
        if not self.target_bssid:
            print("[!] Please scan and select a target first!")
            input("Press Enter to continue...")
            return
        
        self.clear_screen()
        print("[DEAUTHENTICATION ATTACK]")
        print(f"Target: {self.target_ssid} ({self.target_bssid})")
        
        client = input("\n[?] Target client MAC (Enter for broadcast): ").strip()
        if not client:
            client = None
        
        count = input("[?] Number of packets (Enter for unlimited): ").strip()
        if not count:
            count = 0
        else:
            try:
                count = int(count)
            except ValueError:
                count = 0
        
        print(f"\n[*] Starting deauth attack...")
        print("[*] Press Ctrl+C to stop")
        
        try:
            self.tester.running = True
            self.tester.deauth_attack(self.interface, self.target_bssid, client, count)
        except KeyboardInterrupt:
            print("\n[*] Attack stopped by user")
        
        input("Press Enter to continue...")
    
    def beacon_flood_menu(self):
        """Beacon flooding menu"""
        if not self.interface:
            print("[!] Please setup interface first!")
            input("Press Enter to continue...")
            return
        
        self.clear_screen()
        print("[BEACON FLOODING]")
        
        count = input("[?] Number of fake APs (default 1000): ").strip()
        if not count:
            count = 1000
        else:
            try:
                count = int(count)
            except ValueError:
                count = 1000
        
        print(f"\n[*] Starting beacon flood with {count} fake APs...")
        print("[*] Press Ctrl+C to stop")
        
        try:
            self.tester.running = True
            self.tester.beacon_flood(self.interface, count)
        except KeyboardInterrupt:
            print("\n[*] Attack stopped by user")
        
        input("Press Enter to continue...")
    
    def auth_flood_menu(self):
        """Authentication flooding menu"""
        if not self.interface:
            print("[!] Please setup interface first!")
            input("Press Enter to continue...")
            return
        
        if not self.target_bssid:
            print("[!] Please scan and select a target first!")
            input("Press Enter to continue...")
            return
        
        self.clear_screen()
        print("[AUTHENTICATION FLOODING]")
        print(f"Target: {self.target_ssid} ({self.target_bssid})")
        
        count = input("\n[?] Number of auth requests (default 1000): ").strip()
        if not count:
            count = 1000
        else:
            try:
                count = int(count)
            except ValueError:
                count = 1000
        
        print(f"\n[*] Starting auth flood with {count} requests...")
        print("[*] Press Ctrl+C to stop")
        
        try:
            self.tester.running = True
            self.tester.auth_flood(self.interface, self.target_bssid, count)
        except KeyboardInterrupt:
            print("\n[*] Attack stopped by user")
        
        input("Press Enter to continue...")
    
    def probe_flood_menu(self):
        """Probe request flooding menu"""
        if not self.interface:
            print("[!] Please setup interface first!")
            input("Press Enter to continue...")
            return
        
        self.clear_screen()
        print("[PROBE REQUEST FLOODING]")
        
        ssid = input("[?] Target SSID: ").strip()
        if not ssid:
            if self.target_ssid:
                ssid = self.target_ssid
                print(f"[*] Using current target: {ssid}")
            else:
                print("[!] SSID required!")
                input("Press Enter to continue...")
                return
        
        count = input("[?] Number of probe requests (default 1000): ").strip()
        if not count:
            count = 1000
        else:
            try:
                count = int(count)
            except ValueError:
                count = 1000
        
        print(f"\n[*] Starting probe flood for '{ssid}' with {count} requests...")
        print("[*] Press Ctrl+C to stop")
        
        try:
            self.tester.running = True
            self.tester.probe_flood(self.interface, ssid, count)
        except KeyboardInterrupt:
            print("\n[*] Attack stopped by user")
        
        input("Press Enter to continue...")
    
    def show_settings(self):
        """Show current settings"""
        self.clear_screen()
        print("[CURRENT SETTINGS]")
        print(f"Interface: {self.interface or 'Not set'}")
        print(f"Target BSSID: {self.target_bssid or 'Not set'}")
        print(f"Target SSID: {self.target_ssid or 'Not set'}")
        print(f"Networks found: {len(self.networks)}")
        
        input("\nPress Enter to continue...")
    
    def exit_program(self):
        """Exit program with cleanup"""
        print("\n[*] Cleaning up...")
        self.tester.cleanup()
        print("[+] Goodbye!")
        sys.exit(0)

def main():
    # Check root privileges
    if os.geteuid() != 0:
        print("[!] This tool requires root privileges!")
        print("[!] Please run with sudo")
        sys.exit(1)
    
    try:
        gui = WiFiTesterGUI()
        gui.tester.check_dependencies()
        gui.main_menu()
    except KeyboardInterrupt:
        print("\n[*] Interrupted by user")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        print("[*] Cleaning up...")

if __name__ == "__main__":
    main()