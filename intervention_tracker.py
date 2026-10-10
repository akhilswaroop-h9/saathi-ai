import json
import os
from datetime import datetime

DATA_FILE = "interventions.json"


def load_interventions():
    """Load saved faculty intervention records."""
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_intervention(record):
    """Save a faculty intervention record."""
    records = load_interventions()

    record["created_at"] = datetime.now().isoformat()
    records.append(record)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=2, ensure_ascii=False)

    return True


def get_student_interventions(student_id):
    """Get intervention records for one student."""
    records = load_interventions()

    return [
        record
        for record in records
        if str(record.get("student_id")) == str(student_id)
    ]


def delete_intervention(student_id, created_at):
    """Delete a specific intervention record."""
    records = load_interventions()

    updated_records = [
        record
        for record in records
        if not (
            str(record.get("student_id")) == str(student_id)
            and record.get("created_at") == created_at
        )
    ]

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(updated_records, file, indent=2, ensure_ascii=False)

    return len(updated_records) != len(records)
