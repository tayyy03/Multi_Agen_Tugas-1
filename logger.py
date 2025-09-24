import csv
import json
from datetime import datetime
from pathlib import Path

CSV_FILE = Path("conversation_log.csv")
JSON_FILE = Path("conversation_log.json")

def log_message(sender, receiver, performative, conversation_id, content):
    timestamp = datetime.utcnow().isoformat()

    entry = {
        "timestamp": timestamp,
        "sender": str(sender),
        "receiver": str(receiver),
        "performative": performative,
        "conversation_id": conversation_id,
        "content": content,
    }

    # --- Simpan ke CSV ---
    file_exists = CSV_FILE.exists()
    with CSV_FILE.open(mode="a", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["timestamp", "sender", "receiver", "performative", "conversation_id", "content"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        row = entry.copy()
        row["content"] = json.dumps(content, ensure_ascii=False)
        writer.writerow(row)

    # --- Simpan ke JSON ---
    if JSON_FILE.exists():
        try:
            with JSON_FILE.open("r", encoding="utf-8") as jf:
                data = json.load(jf)
        except (json.JSONDecodeError, OSError):
            data = []
    else:
        data = []

    data.append(entry)

    with JSON_FILE.open("w", encoding="utf-8") as jf:
        json.dump(data, jf, indent=2, ensure_ascii=False)

    # --- Debug print ---
    print(f"[LOG] {timestamp} | {sender} -> {receiver} | "
          f"{performative} | {conversation_id} | content={content}")
