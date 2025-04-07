# Load Tester Pro

Professional HTTP load testing tool for security professionals and developers.

## Features
- Multi-threaded architecture
- Precise RPS (requests per second) control
- Detailed statistics reporting
- Randomized User-Agent rotation
- Legal compliance warnings

## Technical Specifications
| Parameter          | Value                      |
|--------------------|---------------------------|
| Max Threads        | 500+ (depends on hardware)|
| Max RPS            | 50,000+ (server-grade)    |
| Supported Protocols| HTTP/HTTPS                |
| Connection Pooling | Yes (keep-alive)          |
| Timeout Handling   | 5s default                |

## Usage
```bash
python load_tester_pro.py <url> [threads] [duration] [rps]
