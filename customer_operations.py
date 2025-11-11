from db_config import get_connection

# =====================================
# 🔹 1. ADD NEW CUSTOMER
# =====================================
def add_customer(name, email, phone, license_no):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Check if customer already exists by license or email
        cursor.execute("SELECT COUNT(*) FROM Customer WHERE License_No = %s OR Email = %s", (license_no, email))
        if cursor.fetchone()[0] > 0:
            return f"⚠️ Customer with License '{license_no}' or Email '{email}' already exists."

        query = """
            INSERT INTO Customer (Name, Email, Phone, License_No)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (name, email, phone, license_no))
        conn.commit()
        return f"✅ Customer '{name}' added successfully!"

    except Exception as e:
        if conn: conn.rollback()
        return f"❌ Database Error: {e}"

    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# =====================================
# 🔹 2. UPDATE CUSTOMER DETAILS
# =====================================
def update_customer(cust_id, name=None, email=None, phone=None, license_no=None):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Check if customer exists
        cursor.execute("SELECT COUNT(*) FROM Customer WHERE Cust_ID = %s", (cust_id,))
        if cursor.fetchone()[0] == 0:
            return f"⚠️ No customer found with ID {cust_id}."

        # Build dynamic update query
        fields = []
        values = []

        if name:
            fields.append("Name = %s")
            values.append(name)
        if email:
            fields.append("Email = %s")
            values.append(email)
        if phone:
            fields.append("Phone = %s")
            values.append(phone)
        if license_no:
            fields.append("License_No = %s")
            values.append(license_no)

        if not fields:
            return "⚠️ No fields provided for update."

        values.append(cust_id)
        query = f"UPDATE Customer SET {', '.join(fields)} WHERE Cust_ID = %s"
        cursor.execute(query, tuple(values))
        conn.commit()
        return f"✅ Customer ID {cust_id} updated successfully!"

    except Exception as e:
        if conn: conn.rollback()
        return f"❌ Database Error: {e}"

    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# =====================================
# 🔹 3. DELETE CUSTOMER
# =====================================
def delete_customer(cust_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Check if customer exists
        cursor.execute("SELECT COUNT(*) FROM Customer WHERE Cust_ID = %s", (cust_id,))
        if cursor.fetchone()[0] == 0:
            return f"⚠️ No customer found with ID {cust_id}."

        # Delete the customer
        cursor.execute("DELETE FROM Customer WHERE Cust_ID = %s", (cust_id,))
        conn.commit()
        return f"🗑️ Customer ID {cust_id} deleted successfully!"

    except Exception as e:
        if conn: conn.rollback()
        return f"❌ Database Error: {e}"

    finally:
        if cursor: cursor.close()
        if conn: conn.close()
