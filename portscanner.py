#!/usr/bin/env python3
import socket
import argparse
import concurrent.futures
import json
import signal
import sys
import time
from datetime import datetime

# Global stop flag for Ctrl+C
stop_flag = False
results = []

# -----------------------------
# Ctrl+C handler
# -----------------------------
def handle_interrupt(signum, frame):
    global stop_flag
    stop_flag = True
    print("\n[!] CTRL+C detected! Finishing current tasks...\n")

signal.signal(signal.SIGINT, handle_interrupt)

# -----------------------------
# Banner grabbing
# -----------------------------
def banner_grab(ip, port):
    probes = [
        b"\r\n",
        b"HEAD / HTTP/1.0\r\n\r\n",
        b"OPTIONS / HTTP/1.0\r\n\r\n",
        b"HELLO\r\n",
        b"QUIT\r\n",
    ]

    try:
        s = socket.socket()
        s.settimeout(0.6)
        s.connect((ip, port))

        for p in probes:
            try:
                s.sendall(p)
                data = s.recv(1024)
                if data:
                    return data.decode("utf-8", errors="ignore").strip()
            except:
                continue
        return ""
    except:
        return ""

# -----------------------------
# Service identification
# -----------------------------
SERVICE_MAP = {
    21: "ftp",
    22: "ssh",
    23: "telnet",
    25: "smtp",
    53: "dns",
    80: "http",
    110: "pop3",
    143: "imap",
    443: "https",
    3306: "mysql",
    6379: "redis",
    8080: "http-proxy"
}

def guess_service(port, banner):
    banner_l = banner.lower()

    if port in SERVICE_MAP:
        return SERVICE_MAP[port]

    keywords = ["ssh", "http", "smtp", "ftp", "mysql", "imap", "pop3", "redis"]
    for k in keywords:
        if k in banner_l:
            return k

    return "unknown"

# -----------------------------
# TCP scanning
# -----------------------------
def scan_tcp(ip, port, do_banner):
    if stop_flag:
        return None

    try:
        s = socket.socket()
        s.settimeout(0.5)
        result = s.connect_ex((ip, port))

        if result == 0:
            banner = banner_grab(ip, port) if do_banner else ""
            service = guess_service(port, banner)

            return {
                "port": port,
                "protocol": "tcp",
                "service": service,
                "banner": banner
            }
    except:
        pass

    return None

# -----------------------------
# UDP scanning
# -----------------------------
def scan_udp(ip, port):
    if stop_flag:
        return None

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)
        s.sendto(b"\x00", (ip, port))

        try:
            data, addr = s.recvfrom(1024)
            banner = data.decode("utf-8", errors="ignore")
            service = guess_service(port, banner)
            return {
                "port": port,
                "protocol": "udp",
                "service": service,
                "banner": banner
            }
        except socket.timeout:
            return None  # UDP non-response

    except:
        return None

# -----------------------------
# Main scan
# -----------------------------
def run_scan(ip, port_range, threads, do_banner, udp_enabled):
    global results

    print(f"\n[+] Scanning {ip}")
    print(f"[+] Ports: {port_range.start}-{port_range.stop - 1}")
    print(f"[+] Threads: {threads}")
    print(f"[+] UDP enabled: {'yes' if udp_enabled else 'no'}")
    print(f"[+] Banner grabbing: {'yes' if do_banner else 'no'}\n")

    tasks = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        for p in port_range:
            tasks.append(executor.submit(scan_tcp, ip, p, do_banner))
            if udp_enabled:
                tasks.append(executor.submit(scan_udp, ip, p))

        total = len(tasks)
        done_count = 0

        for future in concurrent.futures.as_completed(tasks):
            done_count += 1
            if done_count % 200 == 0:
                pct = (done_count / total) * 100
                print(f"[{done_count}/{total}] ~ {pct:.1f}% complete")

            result = future.result()
            if result:
                results.append(result)

# -----------------------------
# Save JSON
# -----------------------------
def save_json(ip, duration):
    data = {
        "target": ip,
        "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "duration_seconds": round(duration, 2),
        "open_ports": sorted(results, key=lambda x: (x["protocol"], x["port"]))
    }

    with open("scan_results.json", "w") as f:
        json.dump(data, f, indent=4)

    print("\n[✔] Results saved to scan_results.json")

# -----------------------------
# CLI
# -----------------------------
def main():
    parser = argparse.ArgumentParser(description="Stable Nmap-style Python Port Scanner")
    parser.add_argument("-t", "--target", required=True)
    parser.add_argument("-p", "--ports", default="1-1024")
    parser.add_argument("--threads", type=int, default=300)
    parser.add_argument("--banner", action="store_true")
    parser.add_argument("--udp", action="store_true")

    args = parser.parse_args()

    ip = args.target
    start, end = map(int, args.ports.split("-"))
    ports = range(start, end + 1)

    start_time = time.time()
    run_scan(ip, ports, args.threads, args.banner, args.udp)
    duration = time.time() - start_time

    save_json(ip, duration)
    print("[✔] Scan complete!")

if __name__ == "__main__":
    main()
