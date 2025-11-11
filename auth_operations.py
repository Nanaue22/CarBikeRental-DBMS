# auth_operations.py
# ------------------
from db_config import get_connection
from tkinter import messagebox

# 🔹 Sign Up New Staff
def signup_staff(name, role, email, password, branch_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Check if email already exists
        cursor.execute("SELECT COUNT(*) FROM Staff WHERE Email = %s", (email,))
        if cursor.fetchone()[0] > 0:
            return "⚠️ Account with this email already exists."

        # Insert new staff record
        cursor.execute("""
            INSERT INTO Staff (Name, Role, Email, Password, Branch_ID)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, role, email, password, branch_id))
        conn.commit()
        return "✅ Account created successfully!"
    except Exception as e:
        conn.rollback()
        return f"⚠️ Database Error: {e}"
    finally:
        cursor.close()
        conn.close()


# 🔹 Login Verification
def login_staff(staff_id, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT Staff_ID, Name, Role 
            FROM Staff
            WHERE Staff_ID = %s AND Password = %s
        """, (staff_id, password))
        user = cursor.fetchone()
        if user:
            return user  # (Staff_ID, Name, Role)
        else:
            return None
    except Exception as e:
        return f"⚠️ Database Error: {e}"
    finally:
        cursor.close()
        conn.close()
