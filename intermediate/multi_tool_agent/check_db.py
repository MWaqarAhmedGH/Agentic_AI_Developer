import sqlite3

def show_data():
import os
    # Direct connection to the SQLite database file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, "agent_database.db")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Query to select all data from the searchrecord table
        cursor.execute("SELECT * FROM searchrecord")
        rows = cursor.fetchall()
        
        print("\n--- [ DATABASE CONTENT ] ---")
        if not rows:
            print("Database is empty.")
        else:
            for row in rows:
                # row[0] is ID, row[1] is Query, row[2] is Summary
                print(f"ID: {row[0]} | Query: {row[1]} | Summary: {row[2]}")
        print("----------------------------\n")
        
        conn.close()
    except Exception as e:
        print(f"Error reading database: {e}")

if __name__ == "__main__":
    show_data()
