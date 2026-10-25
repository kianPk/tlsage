# Contributing to tlsage

## Setup

```bash
git clone https://github.com/kianPk/tlsage.git
cd tlsage
pip install -e .
```

## Checks

```bash
tlsage github.com
tlsage example.com --warn-days 14 --json
```

CI runs on `.github/workflows/ci.yml`.

## PRs

Update `CHANGELOG.md`, keep stdlib-only dependencies, and ensure network smoke tests remain reasonable for CI (we use `github.com` with a high `--warn-days` threshold).
