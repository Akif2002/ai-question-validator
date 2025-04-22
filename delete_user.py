import sqlite3

def delete_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM professors WHERE username = ?", (username,))
    conn.commit()
    conn.close()
    print(f"✅ User '{username}' deleted successfully.")

# Change the username below if needed
delete_user("ZIYATH")
