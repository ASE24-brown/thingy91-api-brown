import sqlite3
from datetime import datetime


def list_tables():
    conn = sqlite3.connect('thingy91.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in the database:", tables)
    conn.close()


def update_device_table():
    conn = sqlite3.connect('thingy91.db')
    cursor = conn.cursor()

    # Check if the status column already exists
    cursor.execute("PRAGMA table_info(device)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'status' not in columns:
        # Add the status column to the device table
        cursor.execute('ALTER TABLE device ADD COLUMN status INTEGER NOT NULL DEFAULT 0')
        print("Status column added to device table.")
    else:
        print("Status column already exists in device table.")

    # Check if the last_updated column already exists
    if 'last_updated' not in columns:
        # Add the last_updated column to the device table
        cursor.execute('ALTER TABLE device ADD COLUMN last_updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP')
        print("Last_updated column added to device table.")
    else:
        print("Last_updated column already exists in device table.")

    conn.commit()
    conn.close()

def add_password_column():
    conn = sqlite3.connect('thingy91.db')
    cursor = conn.cursor()

    # Check if the password column already exists
    cursor.execute("PRAGMA table_info(user)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'password' not in columns:
        # Add the password column to the user table
        cursor.execute('ALTER TABLE user ADD COLUMN password TEXT')
        print("Password column added to user table.")
    else:
        print("Password column already exists in user table.")

    conn.commit()
    conn.close()


def add_device_id_column():
    conn = sqlite3.connect('thingy91.db')  # Replace with your actual database file
    cursor = conn.cursor()

    # Check if the device_id column already exists
    cursor.execute("PRAGMA table_info(sensordata)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'device_id' not in columns:
        # Add the device_id column to the sensordata table
        cursor.execute('ALTER TABLE sensordata ADD COLUMN device_id INTEGER')
        print("device_id column added to sensordata table.")
    else:
        print("device_id column already exists in sensordata table.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    #add_password_column()
    #add_device_id_column()
    update_device_table()
    