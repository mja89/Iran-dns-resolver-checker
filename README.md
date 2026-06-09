# Iran DNS Resolver Checker 🔍

**EN:** Resolve domain names and check which IP addresses are reachable from your network.

**FA:** دامنه‌ها را حل کنید و ببینید کدام IP ها از شبکه شما قابل دسترس هستند.

## Installation / نصب

```bash
git clone https://github.com/mja89/Iran-dns-resolver-checker.git
cd Iran-dns-resolver-checker
pip install -r requirements.txt
```

## Usage / استفاده

```bash
python main.py google.com
python main.py github.com --all-resolvers
python main.py example.com --ports 80 443
python main.py cloudflare.com --json
```

## Termux (Android)

```bash
pkg install python git
git clone https://github.com/mja89/Iran-dns-resolver-checker.git
cd Iran-dns-resolver-checker
pip install -r requirements.txt
python main.py google.com
```

## Status / وضعیت

| Icon | Status | Meaning |
|------|--------|---------|
| ✅ | fast | < 100 ms |
| ⚠️ | slow | 100–400 ms |
| 🐢 | very slow | > 400 ms |
| ❌ | timeout | No response |

## License / مجوز
MIT
