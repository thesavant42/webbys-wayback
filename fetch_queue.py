# fetch_queue.py
from core.fetcher import run_fetch_job
from core.banner import print_banner
import time
import shlex

QUEUE_FILE = "queue.txt"
SLEEP_BETWEEN_JOBS = 5  # seconds

def parse_line(line):
    parts = [p.strip() for p in line.split("|")]
    pattern = parts[0]
    args = shlex.split(" ".join(parts[1:])) if len(parts) > 1 else []
    return pattern, args

def load_queue():
    try:
        with open(QUEUE_FILE, "r") as f:
            return [parse_line(line.strip()) for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        print(f"❌ Queue file not found: {QUEUE_FILE}")
        return []

def parse_args(arglist):
    # Manually parse supported args since we're bypassing argparse
    opts = {
        "extensions": None,
        "output_dir": "downloads",
        "allow_live": True,
        "opsec_mode": False,
        "json_path": None,
        "html_path": None
    }
    i = 0
    while i < len(arglist):
        arg = arglist[i]
        if arg == "--ext" and i + 1 < len(arglist):
            opts["extensions"] = arglist[i+1].split(",")
            i += 2
        elif arg == "--output" and i + 1 < len(arglist):
            opts["output_dir"] = arglist[i+1]
            i += 2
        elif arg == "--no-live":
            opts["allow_live"] = False
            i += 1
        elif arg == "--opsec":
            opts["opsec_mode"] = True
            i += 1
        elif arg == "--export-json" and i + 1 < len(arglist):
            opts["json_path"] = arglist[i+1]
            i += 2
        elif arg == "--export-html" and i + 1 < len(arglist):
            opts["html_path"] = arglist[i+1]
            i += 2
        else:
            i += 1
    return opts

def main():
    print_banner()
    entries = load_queue()
    for pattern, args in entries:
        print(f"🚀 Running pattern: {pattern}")
        opts = parse_args(args)
        run_fetch_job(
            pattern=pattern,
            extensions=opts["extensions"],
            output_dir=opts["output_dir"],
            allow_live=opts["allow_live"],
            opsec_mode=opts["opsec_mode"],
            json_path=opts["json_path"],
            html_path=opts["html_path"]
        )
        time.sleep(SLEEP_BETWEEN_JOBS)

if __name__ == "__main__":
    main()
