# wayback_fetcher.py
from core.fetcher import run_fetch_job
from core.banner import print_banner
import argparse

def main():
    print_banner()

    parser = argparse.ArgumentParser(description="Webby's Wayback — Archive Retriever with Style")
    parser.add_argument("pattern", help="CDX search pattern, e.g., '*.disney.*/*'")
    parser.add_argument("--ext", nargs="+", help="File extensions to include (default: .doc .pdf .xls .ppt)")
    parser.add_argument("--output", default="downloads", help="Directory to save downloaded files")
    parser.add_argument("--no-live", action="store_true", help="Disable live fallback entirely")
    parser.add_argument("--opsec", action="store_true", help="Prompt before accessing live server (OPSEC mode)")
    parser.add_argument("--export-json", help="Path to write JSON results")
    parser.add_argument("--export-html", help="Path to write HTML summary")

    args = parser.parse_args()

    run_fetch_job(
        pattern=args.pattern,
        extensions=args.ext,
        output_dir=args.output,
        allow_live=not args.no_live,
        opsec_mode=args.opsec,
        json_path=args.export_json,
        html_path=args.export_html
    )

if __name__ == "__main__":
    main()
