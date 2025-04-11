# core/exporter.py
import json
from datetime import datetime

class Exporter:
    def write_json(self, path, pattern, results):
        doc = {
            "pattern": pattern,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "results": results
        }
        with open(path, "w") as f:
            json.dump(doc, f, indent=2)
        print(f"📦 JSON export written to: {path}")

    def write_html(self, path, pattern, results):
        with open(path, "w") as f:
            f.write(f"<html><head><title>Webby’s Wayback Report</title><style>")
            f.write("body { font-family: sans-serif; } .live { color:red; } .archive { color:green; }")
            f.write("</style></head><body>")
            f.write(f"<h1>Webby’s Wayback Report</h1><p><b>Pattern:</b> {pattern}</p><ul>")
            for entry in results:
                if entry["source"] == "archive":
                    f.write(f"<li class='archive'>🗂️ <a href='{entry['wayback_url']}'>{entry['original_url']}</a></li>")
                else:
                    f.write(f"<li class='live'>🛰️ <a href='{entry['original_url']}'>{entry['original_url']}</a></li>")
            f.write("</ul></body></html>")
        print(f"🌐 HTML report written to: {path}")
