"""
display.py - Terminal Output Formatter
ماژول نمایش خروجی در ترمینال
"""

from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich import box
from typing import List, Dict

console = Console()

STATUS_STYLE = {
    "fast":      ("✅", "green"),
    "slow":      ("⚠️ ", "yellow"),
    "very_slow": ("🐢", "dark_orange"),
    "timeout":   ("❌", "red"),
    "refused":   ("🚫", "red"),
    "error":     ("💥", "red"),
}


def print_banner():
    banner = Panel.fit(
        "[bold cyan]dns-resolver-checker[/bold cyan]\n"
        "[dim]Resolve domains & check IP reachability[/dim]\n"
        "[dim]حل دامنه و بررسی دسترسی‌پذیری IP از شبکه شما[/dim]",
        border_style="cyan",
    )
    console.print(banner)
    console.print()


def print_resolving(domain: str):
    console.print(f"[bold]🔍 Resolving:[/bold] [cyan]{domain}[/cyan]")


def print_checking(count: int):
    console.print(f"[bold]🌐 Checking[/bold] [yellow]{count}[/yellow] IP(s)...\n")


def print_results(results: List[Dict], domain: str):
    if not results:
        console.print("[red]❌ No IPs found.[/red]")
        return

    table = Table(
        title=f"Results for [bold cyan]{domain}[/bold cyan]",
        box=box.ROUNDED, border_style="cyan",
        header_style="bold magenta", show_lines=True,
    )
    table.add_column("IP Address", style="white", min_width=16)
    table.add_column("Latency", justify="right", min_width=10)
    table.add_column("Status", justify="center", min_width=12)
    table.add_column("Port", justify="center", min_width=7)
    table.add_column("DNS Source", style="dim", min_width=12)

    reachable_count = 0
    for r in results:
        icon, color = STATUS_STYLE.get(r.get("status", "error"), ("❓", "white"))
        latency = r.get("latency_ms")
        latency_str = f"[{color}]{latency:.0f} ms[/{color}]" if latency else "[red]timeout[/red]"
        status_text = Text(f"{icon} {r.get('status','error').replace('_',' ')}")
        status_text.stylize(color)
        table.add_row(
            f"[bold]{r['ip']}[/bold]",
            latency_str, status_text,
            str(r.get("port", "-")),
            r.get("source", "unknown"),
        )
        if r.get("reachable"):
            reachable_count += 1

    console.print(table)
    console.print()
    total = len(results)
    console.print(
        f"[bold]Summary:[/bold] [green]{reachable_count} reachable[/green] | "
        f"[red]{total - reachable_count} unreachable[/red] | [cyan]{total} total[/cyan]"
    )
    if reachable_count > 0:
        best = next(r for r in results if r.get("reachable"))
        console.print(f"\n[bold green]🏆 Best IP:[/bold green] [bold cyan]{best['ip']}[/bold cyan] [dim]({best['latency_ms']:.0f} ms)[/dim]")
    console.print()


def print_no_results(domain: str):
    console.print(Panel(
        f"[red]Could not resolve [bold]{domain}[/bold][/red]\n"
        f"[red]نمی‌توان دامنه [bold]{domain}[/bold] را حل کرد[/red]",
        border_style="red", title="Error / خطا",
    ))
