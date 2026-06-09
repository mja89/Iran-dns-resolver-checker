"""
checker.py - IP Reachability Checker
ماژول بررسی دسترسی‌پذیری IP
"""

import socket
import time
import concurrent.futures
from typing import Dict, List

LATENCY_GOOD = 100
LATENCY_SLOW = 400
DEFAULT_PORTS = [80, 443]
TIMEOUT = 3


def check_ip(ip: str, port: int = 443, timeout: float = TIMEOUT) -> Dict:
    start = time.perf_counter()
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            latency_ms = (time.perf_counter() - start) * 1000
            return {
                "ip": ip, "port": port, "reachable": True,
                "latency_ms": round(latency_ms, 1),
                "status": _classify_latency(latency_ms),
            }
    except (socket.timeout, TimeoutError):
        return {"ip": ip, "port": port, "reachable": False, "latency_ms": None, "status": "timeout"}
    except (ConnectionRefusedError, OSError):
        return {"ip": ip, "port": port, "reachable": False, "latency_ms": None, "status": "refused"}
    except Exception:
        return {"ip": ip, "port": port, "reachable": False, "latency_ms": None, "status": "error"}


def check_ip_multi_port(ip: str, ports: List[int] = None) -> Dict:
    if ports is None:
        ports = DEFAULT_PORTS
    best = None
    for port in ports:
        result = check_ip(ip, port)
        if result["reachable"]:
            if best is None or result["latency_ms"] < best["latency_ms"]:
                best = result
    return best if best else check_ip(ip, ports[0])


def check_all_ips(ip_list: List[Dict], ports: List[int] = None, max_workers: int = 10) -> List[Dict]:
    if ports is None:
        ports = DEFAULT_PORTS

    def _check(entry: Dict) -> Dict:
        result = check_ip_multi_port(entry["ip"], ports)
        return {**entry, **result}

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(_check, entry): entry for entry in ip_list}
        results = []
        for future in concurrent.futures.as_completed(futures):
            try:
                results.append(future.result())
            except Exception:
                pass

    results.sort(key=lambda r: (not r.get("reachable", False), r.get("latency_ms") or float("inf")))
    return results


def _classify_latency(ms: float) -> str:
    if ms < LATENCY_GOOD:
        return "fast"
    elif ms < LATENCY_SLOW:
        return "slow"
    else:
        return "very_slow"
