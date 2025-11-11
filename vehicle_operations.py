from db_config import get_connection

# ====================================================
# 🔹 View all vehicles (with clean error handling)
# ====================================================
def view_available_vehicles():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT 
                Vehicle_ID, Reg_No, Type, Brand, Model, Rent_Price,
                CASE WHEN Availability = TRUE THEN 'Available' ELSE 'Unavailable' END AS Status,
                Branch_ID
            FROM Vehicle
            ORDER BY Vehicle_ID ASC
        """
        cursor.execute(query)
        result = cursor.fetchall()

        if not result:
            return []  # Return empty list if no data found
        return result

    except Exception as e:
        return f"⚠️ Database Error while fetching vehicles: {e}"

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# ====================================================
# 🔹 Add a new vehicle safely
# ====================================================
def add_vehicle(reg_no, vtype, brand, model, rent_price, branch_id, role=None):
    conn = None
    cursor = None

    try:
        conn = get_connection(role)
        cursor = conn.cursor()

        # 1️⃣ Validate Type (must be Car or Bike)
        valid_types = ["Car", "Bike"]
        if vtype not in valid_types:
            return f"⚠️ Invalid vehicle type '{vtype}'. Choose from {valid_types}."

        # 2️⃣ Check for duplicate registration number
        cursor.execute("SELECT COUNT(*) FROM Vehicle WHERE Reg_No = %s", (reg_no,))
        if cursor.fetchone()[0] > 0:
            return f"⚠️ Vehicle with registration number '{reg_no}' already exists."

        # 3️⃣ Check if Branch ID exists
        cursor.execute("SELECT COUNT(*) FROM Branch WHERE Branch_ID = %s", (branch_id,))
        if cursor.fetchone()[0] == 0:
            return f"❌ Error: Branch ID {branch_id} does not exist."

        # 4️⃣ Validate rent price (numeric and positive)
        try:
            rent_price = float(rent_price)
            if rent_price <= 0:
                return "⚠️ Rent price must be a positive value."
        except ValueError:
            return "⚠️ Invalid rent price entered. Please enter a numeric value."

        # 5️⃣ Insert new vehicle record
        insert_query = """
            INSERT INTO Vehicle (Reg_No, Type, Brand, Model, Rent_Price, Availability, Branch_ID)
            VALUES (%s, %s, %s, %s, %s, TRUE, %s)
        """
        cursor.execute(insert_query, (reg_no, vtype, brand, model, rent_price, branch_id))
        conn.commit()

        return f"✅ Vehicle '{brand} {model}' ({vtype}) added successfully!"

    except Exception as e:
        if conn:
            conn.rollback()
        return f"⚠️ Database Error: {e}"

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# ====================================================
# 🔹 Delete a vehicle safely
# ====================================================
def delete_vehicle(vehicle_id, role=None):
    conn = get_connection(role)
    cursor = conn.cursor()
    try:
        # 1️⃣ Check if vehicle exists
        cursor.execute("SELECT Availability FROM Vehicle WHERE Vehicle_ID = %s", (vehicle_id,))
        result = cursor.fetchone()
        if not result:
            return f"❌ Error: Vehicle ID {vehicle_id} does not exist."

        # 2️⃣ Optional: prevent deleting rented vehicles
        if result[0] == 0:
            return f"⚠️ Vehicle ID {vehicle_id} is currently unavailable (rented). Cannot delete."

        # 3️⃣ Delete vehicle
        cursor.execute("DELETE FROM Vehicle WHERE Vehicle_ID = %s", (vehicle_id,))
        conn.commit()
        return f"✅ Vehicle ID {vehicle_id} deleted successfully!"

    except Exception as e:
        conn.rollback()
        return f"⚠️ Database Error: {e}"

    finally:
        cursor.close()
        conn.close()
