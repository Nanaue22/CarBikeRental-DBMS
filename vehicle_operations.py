from db_config import get_connection

def view_available_vehicles():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Vehicle_ID, Brand, Model, Rent_Price, Availability FROM Vehicle")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def add_vehicle(reg_no, vtype, brand, model, rent_price, branch_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO Vehicle (Reg_No, Type, Brand, Model, Rent_Price, Availability, Branch_ID)
        VALUES (%s, %s, %s, %s, %s, TRUE, %s)
    """
    cursor.execute(query, (reg_no, vtype, brand, model, rent_price, branch_id))
    conn.commit()
    cursor.close()
    conn.close()
    return "Vehicle added successfully!"
