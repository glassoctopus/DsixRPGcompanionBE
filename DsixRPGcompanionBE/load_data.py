#!/usr/bin/env python3
import os
import json
import sqlite3
from datetime import datetime

# Configuration
DB_PATH = 'db.sqlite3'  # Update if using different database
SKILLS_FILE = 'fixtures/skills.json'

def create_connection():
    """Create a database connection"""
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.Error as e:
        print(f"Database connection failed: {e}")
        return None

def load_skills():
    """Load skills directly into database"""
    if not os.path.exists(SKILLS_FILE):
        print(f"Error: File not found - {SKILLS_FILE}")
        return

    with open(SKILLS_FILE) as f:
        skills = json.load(f)

    conn = create_connection()
    if not conn:
        return

    cursor = conn.cursor()
    count = 0

    try:
        for skill in skills:
            # Prepare the SQL (adjust columns to match your model)
            sql = """
            INSERT INTO DsixRPGcompanionBE_skill 
            (uid, skill_name, skill_description, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
            """
            
            # Current timestamp
            now = datetime.now().isoformat()
            
            # Execute with parameters
            cursor.execute(sql, (
                skill.get('uid'),
                skill.get('skill_name'),
                skill.get('skill_description'),
                now,
                now
            ))
            count += 1
        
        conn.commit()
        print(f"Successfully loaded {count} skills")
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    print("Starting direct database load...")
    load_skills()
    print("Operation complete")