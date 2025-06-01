import sqlite3
import bcrypt
from datetime import datetime
import random

DATABASE = 'rakshsim_users.db'

def hash_password(plain_text):
    return bcrypt.hashpw(plain_text.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def seed_data():
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()

        # Seed Users
        users = [
            ('Raj Singh', 'raj.singh@chandigarhpolice.in'),
            ('Neha Kaur', 'neha.kaur@chandigarhpolice.in'),
            ('Aman Sharma', 'aman.sharma@chandigarhpolice.in')
        ]

        for name, email in users:
            first_name = name.split()[0]
            password = hash_password(f"{first_name}123")
            completed_modules = random.randint(3, 10)
            cur.execute("INSERT OR IGNORE INTO users (name, email, password, completed_modules) VALUES (?, ?, ?, ?)",
                        (name, email, password, completed_modules))

        # Seed Simulations
        simulations = [('active', 0), ('active', 0), ('inactive', 1), ('inactive', 1)]
        for status, resolved in simulations:
            cur.execute("INSERT INTO simulations (status, resolved) VALUES (?, ?)", (status, resolved))

        # Seed Alerts
        alerts = [
            "New ransomware detected in Sector 17 node.",
            "Backup systems restored successfully.",
            "Unauthorized access attempt blocked.",
            "Simulated phishing attack triggered.",
            "Firewall policy updated for node 12."
        ]
        for msg in alerts:
            cur.execute("INSERT INTO alerts (message) VALUES (?)", (msg,))

        # Seed Incidents
        incidents = [
            (1, "Node 12", "Encryption detected", "Isolated node", "resolved", "malware", "high", datetime.now().isoformat()),
            (2, "Node 3", "Suspicious file activity", "Monitored traffic", "investigating", "suspicious", "medium", datetime.now().isoformat())
        ]
        for inc in incidents:
            cur.execute("""INSERT INTO incidents (user_id, node, summary, actions, status, category, severity, timestamp)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", inc)

        conn.commit()
        print("✅ Seed data inserted successfully using bcrypt.")

if __name__ == '__main__':
    seed_data()