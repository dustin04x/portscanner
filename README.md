# 🔍 Python Port Scanner

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macOS%20%7C%20windows-lightgrey.svg)

**A fast, multithreaded network port scanner with banner grabbing and service detection capabilities**

</div>

---

## ✨ Features

- 🚀 **High-Speed Scanning** - Multithreaded architecture with configurable thread count (default: 300)
- 🎯 **TCP & UDP Support** - Scan both TCP and UDP ports
- 🏷️ **Banner Grabbing** - Extract service banners for detailed reconnaissance
- 🔎 **Service Detection** - Automatically identify common services (HTTP, SSH, FTP, MySQL, etc.)
- 💾 **JSON Export** - Save scan results in structured JSON format
- ⚡ **Real-time Progress** - Track scanning progress with live updates
- 🛑 **Graceful Interruption** - Ctrl+C handling to finish current tasks safely
- 📊 **Detailed Reports** - Timestamp, duration, and comprehensive port information

---

## 📋 Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

---

## 🚀 Installation

1. **Clone or download the script:**
   ```bash
   git clone https://github.com/dustin04x/portscanner.git
   cd portscanner
   ```

2. **Make it executable (Linux/macOS):**
   ```bash
   chmod +x portscanner.py
   ```

3. **Run it:**
   ```bash
   python3 portscanner.py -t <target>
   ```

---

## 💻 Usage

### Basic Syntax

```bash
python3 portscanner.py -t <target> [options]
```

### Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--target` | `-t` | Target IP address or hostname (required) | - |
| `--ports` | `-p` | Port range in format `start-end` | `1-1024` |
| `--threads` | - | Number of concurrent threads | `300` |
| `--banner` | - | Enable banner grabbing | `False` |
| `--udp` | - | Enable UDP scanning | `False` |

---

## 📚 Examples

### 1. **Basic TCP Scan** (Default ports 1-1024)
```bash
python3 portscanner.py -t 192.168.1.1
```

### 2. **Custom Port Range**
```bash
python3 portscanner.py -t 192.168.1.1 -p 1-65535
```

### 3. **Fast Scan with More Threads**
```bash
python3 portscanner.py -t scanme.nmap.org -p 1-1000 --threads 500
```

### 4. **Scan with Banner Grabbing**
```bash
python3 portscanner.py -t 192.168.1.1 -p 20-100 --banner
```

### 5. **Full Scan (TCP + UDP + Banner)**
```bash
python3 portscanner.py -t 192.168.1.1 -p 1-1024 --banner --udp
```

### 6. **Scan Specific Service Ports**
```bash
python3 portscanner.py -t example.com -p 80-443
```

---

## 📊 Sample Output

### Terminal Output:
```bash
[+] Scanning 192.168.1.1
[+] Ports: 1-1024
[+] Threads: 300
[+] UDP enabled: no
[+] Banner grabbing: yes

[200/1024] ~ 19.5% complete
[400/1024] ~ 39.1% complete
[600/1024] ~ 58.6% complete
[800/1024] ~ 78.1% complete
[1000/1024] ~ 97.7% complete

[✔] Results saved to scan_results.json
[✔] Scan complete!
```

### JSON Output (`scan_results.json`):
```json
{
    "target": "192.168.1.1",
    "scan_time": "2025-11-18 10:30:45",
    "duration_seconds": 12.34,
    "open_ports": [
        {
            "port": 22,
            "protocol": "tcp",
            "service": "ssh",
            "banner": "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5"
        },
        {
            "port": 80,
            "protocol": "tcp",
            "service": "http",
            "banner": "HTTP/1.1 200 OK\r\nServer: nginx/1.18.0"
        },
        {
            "port": 443,
            "protocol": "tcp",
            "service": "https",
            "banner": ""
        }
    ]
}
```

---

## 🔧 How It Works

1. **Multi-threading** - Creates a thread pool to scan multiple ports concurrently
2. **Socket Connection** - Attempts TCP/UDP connections to each port
3. **Banner Grabbing** - Sends multiple probes (HTTP, generic) to extract service banners
4. **Service Identification** - Matches ports and banner keywords to identify services
5. **Result Aggregation** - Collects all open ports with their details
6. **JSON Export** - Saves structured results with metadata

### Supported Services

The scanner can identify these common services:

| Port | Service | Port | Service |
|------|---------|------|---------|
| 21 | FTP | 143 | IMAP |
| 22 | SSH | 443 | HTTPS |
| 23 | Telnet | 3306 | MySQL |
| 25 | SMTP | 6379 | Redis |
| 53 | DNS | 8080 | HTTP-Proxy |
| 80 | HTTP | 110 | POP3 |

Additional services can be detected through banner analysis.

---

## ⚙️ Customization

### Adjust Timeout Values

For more accurate or faster scans, modify timeouts in the code:

```python
# TCP connection timeout (line 94)
s.settimeout(0.5)  # Default: 0.5 seconds

# Banner grab timeout (line 39)
s.settimeout(0.6)  # Default: 0.6 seconds

# UDP timeout (line 121)
s.settimeout(1)    # Default: 1 second
```

### Add More Services

Extend the `SERVICE_MAP` dictionary (line 57):

```python
SERVICE_MAP = {
    21: "ftp",
    22: "ssh",
    # Add your custom services here
    5432: "postgresql",
    27017: "mongodb",
}
```

---

## 🛡️ Performance Tips

- **Faster Scans**: Increase threads (`--threads 500-1000`) for faster networks
- **Accuracy**: Lower threads (`--threads 50-100`) for unstable connections
- **Stealth**: Use lower thread counts to avoid detection/rate limiting
- **UDP Scanning**: UDP is slower; consider scanning only specific UDP ports

---

## ⚠️ Important Notes

- **Graceful Exit**: Press `Ctrl+C` to stop scanning - the script will finish current tasks and save results
- **Network Stability**: Very high thread counts may cause network congestion
- **UDP Scanning**: UDP responses are unreliable; lack of response doesn't always mean the port is closed
- **Firewall Detection**: Some ports may appear closed due to firewalls filtering traffic

---

## 🔒 Legal Disclaimer

This tool is intended for **educational purposes** and **authorized security testing only**.

⚠️ **WARNING**: Unauthorized port scanning may be illegal in your jurisdiction. Always ensure you have:
- Explicit written permission from the network owner
- Authorization to perform security testing
- Compliance with local laws and regulations

**The authors are not responsible for misuse or damage caused by this tool. Use ethically and responsibly.**

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Suggestions for Enhancements:
- Add SYN scan support
- Implement OS detection
- Add XML output format
- Create stealth scan modes
- Add IPv6 support

---

## 📝 Changelog

### Version 2.0 (Current)
- ✅ Added UDP scanning support
- ✅ Implemented banner grabbing
- ✅ Added service detection
- ✅ JSON output format
- ✅ Progress tracking
- ✅ Graceful Ctrl+C handling
- ✅ Configurable threading
- ✅ Enhanced CLI with argparse

### Version 1.0
- Basic TCP port scanning
- Simple multithreading

---

## 🙏 Acknowledgments

- Inspired by Nmap and other network scanning tools
- Built with Python's powerful standard library
- Thanks to the security research community

---

<div align="center">

**Made with ❤️ for the cybersecurity community**

[Report Bug](https://github.com/dustin04x/portscanner/issues) · [Request Feature](https://github.com/dustin04x/portscanner/issues)

</div>
