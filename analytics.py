from db_config import get_connection
import matplotlib.pyplot as plt

def vehicle_type_distribution():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Type, COUNT(*) FROM Vehicle GROUP BY Type")
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    types = [row[0] for row in data]
    counts = [row[1] for row in data]

    plt.figure(figsize=(5, 5))
    plt.pie(counts, labels=types, autopct='%1.1f%%', startangle=140)
    plt.title("Vehicle Type Distribution")
    plt.show()

def top_customers_by_spent():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.Name, GetCustomerTotal(c.Cust_ID)
        FROM Customer c
        ORDER BY GetCustomerTotal(c.Cust_ID) DESC
        LIMIT 5;
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    names = [row[0] for row in data]
    totals = [row[1] for row in data]

    plt.figure(figsize=(6, 4))
    plt.bar(names, totals)
    plt.xlabel("Customer")
    plt.ylabel("Total Spent (₹)")
    plt.title("Top 5 Customers by Spending")
    plt.show()
