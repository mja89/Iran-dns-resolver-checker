import socket
from typing import List, Dict

DNS_SERVERS = {
    "Google":     ["8.8.8.8", "8.8.4.4"],
    "Cloudflare": ["1.1.1.1", "1.0.0.1"],
    "Quad9":      ["9.9.9.9", "149.112.112.112"],
    "OpenDNS":    ["208.67.222.222", "208.67.220.220"],
    "System":     None,
}

def resolve_domain(domain: str, use_all_resolvers: bool = False) -> List[Dict]:
    results = []
    seen_ips = set()
    try:
        infos = socket.getaddrinfo(domain, None)
        for info in infos:
            ip = info[4][0]
            if ip not in seen_ips and ":" not in ip:
                seen_ips.add(ip)
                results.append({"ip": ip, "source": "System", "domain": domain})
    except Exception:
        pass
    return results

def get_hostname(ip: str) -> str:
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return ""
