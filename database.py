import sqlite3
from pathlib import Path


DATABASE_PATH = Path("data/legal_intake.db")


def get_connection():
    DATABASE_PATH.parent.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS intakes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            matter_type TEXT NOT NULL,
            opposing_party TEXT,
            incident_date TEXT,
            description TEXT NOT NULL,
            desired_outcome TEXT,
            intake_status TEXT NOT NULL,
            conflict_check_status TEXT NOT NULL,
            decision_status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_intake(intake_data, intake_analysis, ai_summary):
    connection = get_connection()

    cursor = connection.execute("""
        INSERT INTO intakes (
            full_name,
            email,
            phone,
            matter_type,
            opposing_party,
            incident_date,
            description,
            desired_outcome,
            intake_status,
            conflict_check_status,
            decision_status,
            ai_summary
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        intake_data.get("full_name"),
        intake_data.get("email"),
        intake_data.get("phone"),
        intake_data.get("matter_type"),
        intake_data.get("opposing_party"),
        intake_data.get("incident_date"),
        intake_data.get("description"),
        intake_data.get("desired_outcome"),
        intake_analysis.get("intake_status"),
        intake_analysis.get("conflict_check_status"),
        intake_analysis.get("decision_status"),
        ai_summary,
    ))

    intake_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return intake_id

def get_all_intakes():
    connection = get_connection()

    intakes = connection.execute("""
        SELECT
            id,
            full_name,
            email,
            phone,
            matter_type,
            opposing_party,
            incident_date,
            intake_status,
            conflict_check_status,
            decision_status,
            created_at
        FROM intakes
        ORDER BY created_at DESC
    """).fetchall()

    connection.close()

    return intakes
    
def get_intake_by_id(intake_id):
    connection = get_connection()

    intake = connection.execute("""
        SELECT
            id,
            full_name,
            email,
            phone,
            matter_type,
            opposing_party,
            incident_date,
            description,
            desired_outcome,
            intake_status,
            conflict_check_status,
            decision_status,
            ai_summary,
            created_at
        FROM intakes
        WHERE id = ?
    """, (intake_id,)).fetchone()

    connection.close()

    return intake