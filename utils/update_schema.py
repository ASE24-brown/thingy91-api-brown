import sqlite3

def add_password_column():
    conn = sqlite3.connect('thingy91.db')  # Replace with your actual database file
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

if __name__ == "__main__":
    add_password_column()