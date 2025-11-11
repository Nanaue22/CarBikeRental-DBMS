from db_config import get_connection

def add_rental(cust_id, vehicle_id, staff_id, start_date, end_date, role=None):
    conn = get_connection(role)
    cursor = conn.cursor()

    try:
        # 1️⃣ Check if customer exists
        cursor.execute("SELECT COUNT(*) FROM Customer WHERE Cust_ID = %s", (cust_id,))
        if cursor.fetchone()[0] == 0:
            return f"❌ Error: Customer ID {cust_id} does not exist."

        # 2️⃣ Check if vehicle exists and is available
        cursor.execute("SELECT Availability FROM Vehicle WHERE Vehicle_ID = %s", (vehicle_id,))
        result = cursor.fetchone()
        if not result:
            return f"❌ Error: Vehicle ID {vehicle_id} does not exist."
        if result[0] == 0:
            return f"⚠️ Vehicle ID {vehicle_id} is currently unavailable."

        # 3️⃣ Check if staff exists
        cursor.execute("SELECT COUNT(*) FROM Staff WHERE Staff_ID = %s", (staff_id,))
        if cursor.fetchone()[0] == 0:
            return f"❌ Error: Staff ID {staff_id} does not exist."

        # 4️⃣ Insert rental
        query = """
        INSERT INTO Rental (Cust_ID, Vehicle_ID, Staff_ID, Start_Date, End_Date, Status)
        VALUES (%s, %s, %s, %s, %s, 'Booked')
        """
        cursor.execute(query, (cust_id, vehicle_id, staff_id, start_date, end_date))
        conn.commit()
        return "✅ Rental added successfully!"

    except Exception as e:
        conn.rollback()
        return f"⚠️ Database Error: {e}"

    finally:
        cursor.close()
        conn.close()

# 🔹 Return vehicle safely
def return_vehicle(rental_id, role=None):
    conn = get_connection(role)
    cursor = conn.cursor()
    try:
        # 1️⃣ Check if rental exists
        cursor.execute("SELECT Status FROM Rental WHERE Rental_ID = %s", (rental_id,))
        result = cursor.fetchone()

        if not result:
            return f"❌ Error: Rental ID {rental_id} does not exist."

        # 2️⃣ Prevent duplicate returns
        if result[0] == "Returned":
            return f"⚠️ Rental ID {rental_id} is already marked as Returned."

        # 3️⃣ Perform update
        query = """
            UPDATE Rental
            SET Status = 'Returned', Return_Date = CURDATE()
            WHERE Rental_ID = %s
        """
        cursor.execute(query, (rental_id,))
        conn.commit()

        return f"✅ Vehicle successfully marked as returned for Rental ID {rental_id}."

    except Exception as e:
        conn.rollback()
        return f"⚠️ Database Error: {e}"

    finally:
        cursor.close()
        conn.close()


# 🔹 Safely calculate rental cost (via stored procedure)
def calculate_rental_cost(rental_id, role=None):
    conn = get_connection(role)
    cursor = conn.cursor()
    try:
        # 1️⃣ Check if rental exists
        cursor.execute("SELECT COUNT(*) FROM Rental WHERE Rental_ID = %s", (rental_id,))
        if cursor.fetchone()[0] == 0:
            return f"❌ Error: Rental ID {rental_id} does not exist."

        # 2️⃣ Call stored procedure
        cursor.callproc("Calculate_Rental_Cost", [rental_id])
        conn.commit()

        # 3️⃣ Fetch updated total cost
        cursor.execute("SELECT Total_Cost FROM Rental WHERE Rental_ID = %s", (rental_id,))
        total = cursor.fetchone()[0]

        return f"✅ Total cost for Rental ID {rental_id} calculated: ₹{total:.2f}"

    except Exception as e:
        conn.rollback()
        return f"⚠️ Database Error: {e}"

    finally:
        cursor.close()
        conn.close()
