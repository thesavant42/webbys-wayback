# core/fetcher.py
import os, requests, time
from urllib.parse import urlparse
from core.exporter import Exporter
from core.logger import log_event

CDX_API = "http://web.archive.org/cdx/search/cdx"
WAYBACK = "https://web.archive.org/web"
DEFAULT_EXTENSIONS = [".doc", ".pdf", ".xls", ".ppt"]
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; WebbyFetcher/1.0)",
    "Referer": "https://web.archive.org/"
}

def is_target_file(url, extensions):
    return any(url.lower().endswith(ext) for ext in extensions)

def sanitize_filename(url):
    parsed = urlparse(url)
    name = parsed.path.replace("/", "_").strip("_")
    return f"{parsed.netloc}_{name or 'index'}"

def query_cdx(pattern, offset, limit=1000):
    params = {
        "url": pattern,
        "output": "json",
        "filter": "statuscode:200",
        "fl": "timestamp,original",
        "collapse": "urlkey",
        "limit": limit,
        "offset": offset
    }
    try:
        r = requests.get(CDX_API, params=params, headers=HEADERS, timeout=15)
        r.raise_for_status()
        data = r.json()
        return data[1:] if len(data) > 1 else []
    except:
        return []

def confirm(prompt):
    try:
        return input(f"{prompt} (Y/n) ").lower().strip() in ["y", "yes", ""]
    except KeyboardInterrupt:
        return False

def download(url, path):
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        with open(path, "wb") as f:
            f.write(r.content)
        return True
    except:
        return False

def run_fetch_job(pattern, extensions, output_dir, allow_live, opsec_mode, json_path, html_path):
    os.makedirs(output_dir, exist_ok=True)
    seen = set()
    results = []
    offset = 0
    page = 0
    max_pages = 10000

    extensions = extensions or DEFAULT_EXTENSIONS

    while page < max_pages:
        records = query_cdx(pattern, offset)
        if not records:
            break

        for timestamp, original in records:
            if original in seen or not is_target_file(original, extensions):
                continue
            seen.add(original)
            filename = sanitize_filename(original)
            filepath = os.path.join(output_dir, filename)
            wb_url = f"{WAYBACK}/{timestamp}/{original}"

            if download(wb_url, filepath):
                print(f"🗂️  Recovered from shadow archives: {filename}")
                log_event(f"ARCHIVE: {original} -> {filepath}")
                results.append({"source": "archive", "original_url": original, "wayback_url": wb_url, "saved_as": filepath})
            elif allow_live:
                if opsec_mode:
                    if not confirm(f"❗ Archive miss for {original}. Access live version?"):
                        print("🚫 Skipping live request.")
                        continue
                live_path = f"{filepath}_live"
                if download(original, live_path):
                    print(f"🛰️  Fallback from live server: {filename}")
                    log_event(f"LIVE: {original} -> {live_path}")
                    results.append({"source": "live", "original_url": original, "saved_as": live_path})
                else:
                    print(f"💥  Retrieval failed: {original}")
                log_event(f"FAIL: {original}")
            else:
                print(f"💀  Not in archive, and live fallback disabled: {original}")
                log_event(f"SKIP_NO_LIVE: {original}")

        offset += 1000
        page += 1
        time.sleep(1)

    print(f"📚 Done. {len(results)} files secured from the shadows.")
    log_event(f"SUMMARY: {len(results)} files archived for pattern '{pattern}'")
    exporter = Exporter()
    if json_path:
        exporter.write_json(json_path, pattern, results)
    if html_path:
        exporter.write_html(html_path, pattern, results)
