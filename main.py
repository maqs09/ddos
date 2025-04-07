#!/usr/bin/env python3
"""
Load Tester Pro - Professional-grade load testing tool
Version: 2.1
License: MIT
"""

import sys
import time
import requests
import threading
import random
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

class LoadTester:
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Apache-HttpClient/4.5.13",
        "Python-requests/2.28.1"
    ]

    def __init__(self, url, threads=50, duration=30, rps=100):
        self.url = self._validate_url(url)
        self.threads = threads
        self.duration = duration
        self.target_rps = rps
        self.results = {
            'total': 0,
            'success': 0,
            'errors': 0,
            'status_codes': {},
            'start_time': time.time()
        }
        self.running = False
        self.lock = threading.Lock()

    def _validate_url(self, url):
        parsed = urlparse(url)
        if not all([parsed.scheme, parsed.netloc]):
            raise ValueError("Invalid URL format")
        return url

    def _send_request(self):
        headers = {'User-Agent': random.choice(self.USER_AGENTS)}
        try:
            response = requests.get(
                self.url,
                headers=headers,
                timeout=5,
                allow_redirects=False
            )
            with self.lock:
                self.results['total'] += 1
                self.results['success'] += 1
                code = response.status_code
                self.results['status_codes'][code] = self.results['status_codes'].get(code, 0) + 1
            return True
        except Exception as e:
            with self.lock:
                self.results['total'] += 1
                self.results['errors'] += 1
            return False

    def _worker(self):
        delay = 1.0 / self.target_rps if self.target_rps > 0 else 0
        while self.running:
            self._send_request()
            time.sleep(delay)

    def run(self):
        print(f"\n[Load Tester Pro] Starting test for {self.duration}s")
        print(f"• Target: {self.url}")
        print(f"• Threads: {self.threads}")
        print(f"• Target RPS: {self.target_rps}")
        print("="*50)

        self.running = True
        self.results['start_time'] = time.time()

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            for _ in range(self.threads):
                executor.submit(self._worker)
            
            while time.time() - self.results['start_time'] < self.duration:
                time.sleep(1)
                self._print_stats()
        
        self.running = False
        self._print_final_report()

    def _print_stats(self):
        elapsed = time.time() - self.results['start_time']
        with self.lock:
            print(f"\r[Status] Reqs: {self.results['total']} | "
                  f"OK: {self.results['success']} | "
                  f"ERR: {self.results['errors']} | "
                  f"RPS: {self.results['total']/elapsed:.1f} | "
                  f"Time: {elapsed:.1f}s", end="")

    def _print_final_report(self):
        print("\n\n" + "="*50)
        print("[TEST COMPLETE]")
        print(f"Total duration: {time.time() - self.results['start_time']:.2f}s")
        print(f"Requests sent: {self.results['total']}")
        print(f"Successful: {self.results['success']}")
        print(f"Failed: {self.results['errors']}")
        print("\nStatus codes:")
        for code, count in sorted(self.results['status_codes'].items()):
            print(f"  {code}: {count}")
        print("="*50)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python load_tester_pro.py <url> [threads] [duration] [rps]")
        print("Example: python load_tester_pro.py https://example.com 50 30 100")
        sys.exit(1)

    try:
        url = sys.argv[1]
        threads = int(sys.argv[2]) if len(sys.argv) > 2 else 50
        duration = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        rps = int(sys.argv[4]) if len(sys.argv) > 4 else 100

        print("[!] LEGAL NOTICE: Use only against systems you own or have permission to test!")
        tester = LoadTester(url, threads, duration, rps)
        tester.run()
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
