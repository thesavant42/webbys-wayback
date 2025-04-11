```markdown
# 🦆 Webby's Wayback v1.0 — The Shadow Fetcher

**Webby’s Wayback** is a stealthy retrieval tool for downloading real, archived `.doc`, `.pdf`, `.xls`, and `.ppt` files from the Internet Archive’s Wayback Machine — with fallback logic, logging, and full modularity.

## 💼 Features

- ✅ Wildcard URL support (`*.disney.*/*`)
- ✅ Filters only `200 OK` snapshots
- ✅ Filetype filtering
- ✅ Wayback-first downloading
- ✅ Optional live fallback
- ✅ `--opsec` mode to block accidental live hits
- ✅ Per-pattern flags via `queue.txt`
- ✅ JSON + HTML report generation
- ✅ Modular Python structure
- ✅ DW-style terminal output
- ✅ High-verbosity logging
- ✅ Daily log rotation (30-day retention)

## 🧰 Installation

```bash
pip install requests
```

## 🚀 Usage

```bash
python3 wayback_fetcher.py "*.disney.*/*"
```

### With options:

```bash
python3 wayback_fetcher.py "*.disney.*/*" --opsec --export-json disney.json --export-html disney.html
```

## 📋 Queue Mode

Edit `queue.txt`:

```
*.disney.*/* | --opsec --export-json=disney.json
*.pixar.*/*.doc | --ext=.doc,.pdf
```

Then run:

```bash
python3 fetch_queue.py
```

## 📦 Output

- Files downloaded to `downloads/`
- Logs stored in `logs/`
- JSON and HTML reports if requested

## 🔐 License

Apache 2.0 — see [LICENSE](LICENSE)

---
🧠 Built by savant42, part of the Darkwing Dox toolkit.
```
