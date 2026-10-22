# tlsage

**How many days until this TLS cert dies?**

One command for ops, monitors, and “why is prod angry” moments.

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Install

```bash
pip install .
# or run directly
python tlsage.py github.com
```

## Usage

```bash
tlsage github.com
tlsage example.com -w 14          # warn if ≤ 14 days
tlsage api.myapp.com -p 8443
```

### Sample

```text
github.com:443
  expires  2026-03-15 12:00 UTC
  days     144.2
  status   OK
```

Exit `1` when expired or inside the warn window — CI / cron friendly.

## License

MIT © [kianPk](https://github.com/kianPk)
