from db_config import get_connection

def get_table_data(table_name, role=None):
    conn = get_connection(role)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    cursor.close()
    conn.close()
    return columns, data

# 🔹 NEW: Call MySQL FUNCTION GetCustomerTotal
def get_customer_total_spent(cust_id, role=None):
    conn = get_connection(role)
    cursor = conn.cursor()
    cursor.execute("SELECT GetCustomerTotal(%s)", (cust_id,))
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return result if result else 0.0
