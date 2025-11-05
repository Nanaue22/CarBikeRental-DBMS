from db_config import get_connection

def add_rental(cust_id, vehicle_id, staff_id, start_date, end_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Customer WHERE Cust_ID = %s", (cust_id,))
    if cursor.fetchone()[0] == 0:
        cursor.close()
        conn.close()
        return f"Error: Customer ID {cust_id} does not exist."

    query = """
        INSERT INTO Rental (Cust_ID, Vehicle_ID, Staff_ID, Start_Date, End_Date, Status)
        VALUES (%s, %s, %s, %s, %s, 'Booked')
    """
    cursor.execute(query, (cust_id, vehicle_id, staff_id, start_date, end_date))
    conn.commit()
    cursor.close()
    conn.close()
    return "Rental added successfully!"

def return_vehicle(rental_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "UPDATE Rental SET Status = 'Returned', Return_Date = CURDATE() WHERE Rental_ID = %s"
    cursor.execute(query, (rental_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return "Vehicle returned successfully!"

# 🔹 NEW: Call stored procedure to calculate rental cost
def calculate_rental_cost(rental_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.callproc("Calculate_Rental_Cost", [rental_id])
    conn.commit()
    cursor.close()
    conn.close()
    return f"Total cost calculated for Rental ID {rental_id}"
