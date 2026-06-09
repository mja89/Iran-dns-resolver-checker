#!/usr/bin/env python3
"""
main.py - DNS Resolver Checker
"""

import argparse
import json
import sys

from dns_resolver_checker.resolver import resolve_domain
from dns_resolver_checker.checker import check_all_ips
from dns_resolver_checker import display


def parse_args():
    parser = argparse.ArgumentParser(
        prog="dns-resolver-checker",
        description="Resolve a domain and check which IPs are reachable.\nدامنه را حل کرده و بررسی می‌کند کدام IP ها قابل دسترس هستند.",
    )
    parser.add_argument("domain", help="Domain name / نام دامنه")
    parser.add_argument("--all-resolvers", "-a", action="store_true",
                        help="Query multiple DNS servers / استفاده از چند DNS سرور")
    parser.add_argument("--ports", "-p", nargs="+", type=int, default=[443, 80], metavar="PORT",
                        help="TCP ports to test (default: 443 80)")
    parser.add_argument("--workers", "-w", type=int, default=10, metavar="N",
                        help="Concurrent threads (default: 10)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--version", "-v", action="version", version="1.0.0")
    return parser.parse_args()


def main():
    args = parse_args()
    domain = args.domain.strip().lower()
    for prefix in ("https://", "http://", "www."):
        if domain.startswith(prefix):
            domain = domain[len(prefix):]

    if not args.json:
        display.print_banner()
        display.print_resolving(domain)

    ip_entries = resolve_domain(domain, use_all_resolvers=args.all_resolvers)

    if not ip_entries:
        if args.json:
            print(json.dumps({"error": f"Could not resolve {domain}", "results": []}))
        else:
            display.print_no_results(domain)
        sys.exit(1)

    if not args.json:
        display.print_checking(len(ip_entries))

    results = check_all_ips(ip_entries, ports=args.ports, max_workers=args.workers)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        display.print_results(results, domain)


if __name__ == "__main__":
    main()
