import json
import os
import pandas as pd

DATA_FILE = "interventions.json"

COLUMNS = [
    "student_id",
    "student_name",
    "faculty_name",
    "intervention_type",
    "notes",
    "status",
    "created_at",
]


def load_interventions():
    """Load all saved faculty intervention records."""
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def add_intervention(
    student_id,
    student_name="",
    faculty_name="",
    intervention_type="General",
    notes="",
    status="Pending",
    **kwargs,
):
    """Add a new faculty intervention."""
    from datetime import datetime

    record = {
        "student_id": str(student_id),
        "student_name": student_name,
        "faculty_name": faculty_name,
        "intervention_type": intervention_type,
        "notes": notes,
        "status": status,
        "created_at": datetime.now().isoformat(),
    }

    record.update(kwargs)

    records = load_interventions()
    records.append(record)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=2, ensure_ascii=False)

    return record


def update_intervention_status(intervention_id, status):
    """Update an intervention's status."""
    records = load_interventions()
    updated = False

    for index, record in enumerate(records):
        record_id = record.get(
            "intervention_id",
            record.get("id", index),
        )

        if str(record_id) == str(intervention_id):
            record["status"] = status
            updated = True
            break

    if updated:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(records, file, indent=2, ensure_ascii=False)

    return updated


def interventions_dataframe():
    """Return intervention records as a Pandas DataFrame."""
    records = load_interventions()
    return pd.DataFrame(records, columns=COLUMNS)
