# core/logger.py
import os
from datetime import datetime, timedelta

LOG_DIR = "logs"
RETENTION_DAYS = 30

def log_event(message):
    os.makedirs(LOG_DIR, exist_ok=True)
    rotate_logs()
    log_file = os.path.join(LOG_DIR, f"webby_{datetime.utcnow().strftime('%Y%m%d')}.log")
    timestamp = datetime.utcnow().isoformat()
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def rotate_logs():
    cutoff = datetime.utcnow() - timedelta(days=RETENTION_DAYS)
    for filename in os.listdir(LOG_DIR):
        if filename.startswith("webby_") and filename.endswith(".log"):
            try:
                date_str = filename[len("webby_"):-len(".log")]
                file_date = datetime.strptime(date_str, "%Y%m%d")
                if file_date < cutoff:
                    os.remove(os.path.join(LOG_DIR, filename))
            except Exception:
                continue
