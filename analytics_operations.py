# analytics_operations.py
from db_config import get_connection


# -------------------------------------------
# Nested Query – Customer with most expensive rental
# -------------------------------------------
def get_customer_most_expensive(role=None):
    conn = get_connection(role)
    cursor = conn.cursor(buffered=True)

    query = """
        SELECT c.Name, c.Email
        FROM Customer c
        JOIN Rental r ON c.Cust_ID = r.Cust_ID
        JOIN Vehicle v ON r.Vehicle_ID = v.Vehicle_ID
        ORDER BY v.Rent_Price DESC
        LIMIT 1;
    """

    cursor.execute(query)
    result = cursor.fetchone()

    cursor.close()
    conn.close()
    return result

# -------------------------------------------
# Join Query – Full rental report
# -------------------------------------------
def get_rental_report(role=None):
    conn = get_connection(role)
    cursor = conn.cursor()

    query = """
        SELECT 
            r.Rental_ID,
            c.Name AS Customer_Name,
            v.Model AS Vehicle_Model,
            s.Name AS Staff_Name,
            r.Start_Date,
            r.End_Date,
            r.Total_Cost
        FROM Rental r
        LEFT JOIN Customer c ON r.Cust_ID = c.Cust_ID
        LEFT JOIN Vehicle v ON r.Vehicle_ID = v.Vehicle_ID
        LEFT JOIN Staff s ON r.Staff_ID = s.Staff_ID;
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


# -------------------------------------------
# Branch-wise vehicle count
# -------------------------------------------
def get_branch_vehicle_count(role=None):
    conn = get_connection(role)
    cursor = conn.cursor()

    query = """
        SELECT 
            b.Name AS Branch_Name,
            v.Type AS Vehicle_Type,
            COUNT(v.Vehicle_ID) AS Number_Of_Vehicles
        FROM Vehicle v
        JOIN Branch b ON v.Branch_ID = b.Branch_ID
        GROUP BY b.Name, v.Type
        ORDER BY b.Name, v.Type;
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows
