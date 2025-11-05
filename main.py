import tkinter as tk
from tkinter import ttk, messagebox
from rental_operations import add_rental, return_vehicle, calculate_rental_cost
from vehicle_operations import view_available_vehicles, add_vehicle
from common_operations import get_table_data, get_customer_total_spent
from analytics import vehicle_type_distribution, top_customers_by_spent

root = tk.Tk()
root.title("Car/Bike Rental Management System")
root.geometry("1100x650")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# -------------------------------------------------
# TAB 1: View Tables
# -------------------------------------------------
tab_view = ttk.Frame(notebook)
notebook.add(tab_view, text="📋 View Tables")

tables = ["Customer", "Staff", "Vehicle", "Rental", "Payment", "Branch"]

frame_table = tk.Frame(tab_view)
frame_table.pack(fill="x", pady=10)

tk.Label(frame_table, text="Select Table:").pack(side="left", padx=10)
selected_table = tk.StringVar(value="Customer")
table_menu = ttk.Combobox(frame_table, textvariable=selected_table, values=tables, state="readonly")
table_menu.pack(side="left", padx=10)

tree = ttk.Treeview(tab_view)
tree.pack(fill="both", expand=True, pady=10)

def load_table_data(table_name):
    cols, rows = get_table_data(table_name)
    for i in tree.get_children():
        tree.delete(i)
    tree["columns"] = cols
    tree["show"] = "headings"
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    for row in rows:
        tree.insert("", "end", values=row)

tk.Button(frame_table, text="Show Data", command=lambda: load_table_data(selected_table.get()), bg="blue", fg="white").pack(side="left", padx=10)

# -------------------------------------------------
# TAB 2: Vehicle Management
# -------------------------------------------------
tab_vehicle = ttk.Frame(notebook)
notebook.add(tab_vehicle, text="🚗 Vehicle Management")

tk.Label(tab_vehicle, text="Add New Vehicle", font=("Arial", 14, "bold")).pack(pady=10)
frame_add_vehicle = tk.Frame(tab_vehicle)
frame_add_vehicle.pack(pady=10)

labels = ["Reg No", "Type (Car/Bike)", "Brand", "Model", "Rent Price", "Branch ID"]
entries = []

for i, lbl in enumerate(labels):
    tk.Label(frame_add_vehicle, text=lbl).grid(row=i, column=0, sticky="e", pady=5)
    ent = tk.Entry(frame_add_vehicle)
    ent.grid(row=i, column=1, padx=10)
    entries.append(ent)

def handle_add_vehicle():
    vals = [e.get() for e in entries]
    msg = add_vehicle(*vals)
    messagebox.showinfo("Success", msg)
    for e in entries:
        e.delete(0, tk.END)

tk.Button(tab_vehicle, text="Add Vehicle", command=handle_add_vehicle, bg="green", fg="white").pack(pady=10)

# -------------------------------------------------
# TAB 3: Rental Operations
# -------------------------------------------------
tab_rental = ttk.Frame(notebook)
notebook.add(tab_rental, text="📄 Rental Operations")

# Add Rental
tk.Label(tab_rental, text="Add New Rental", font=("Arial", 14, "bold")).pack(pady=10)
frame_rent = tk.Frame(tab_rental)
frame_rent.pack(pady=5)

lbls = ["Customer ID", "Vehicle ID", "Staff ID", "Start Date (YYYY-MM-DD)", "End Date (YYYY-MM-DD)"]
entries_r = []
for i, lbl in enumerate(lbls):
    tk.Label(frame_rent, text=lbl).grid(row=i, column=0, sticky="e", pady=5)
    ent = tk.Entry(frame_rent)
    ent.grid(row=i, column=1, padx=10)
    entries_r.append(ent)

tk.Button(frame_rent, text="Add Rental", command=lambda: messagebox.showinfo("Result", add_rental(*[e.get() for e in entries_r])), bg="green", fg="white").grid(row=6, column=0, columnspan=2, pady=10)

# Return Rental
tk.Label(tab_rental, text="Return Vehicle", font=("Arial", 14, "bold")).pack(pady=10)
frm_return = tk.Frame(tab_rental)
frm_return.pack(pady=5)

tk.Label(frm_return, text="Rental ID").grid(row=0, column=0)
rental_id = tk.Entry(frm_return)
rental_id.grid(row=0, column=1)

tk.Button(frm_return, text="Mark Returned", command=lambda: messagebox.showinfo("Returned", return_vehicle(rental_id.get())), bg="blue", fg="white").grid(row=1, column=0, columnspan=2, pady=10)

# Calculate Cost (Stored Procedure)
tk.Label(frm_return, text="Calculate Total Cost").grid(row=2, column=0, pady=5)
cost_rental_id = tk.Entry(frm_return)
cost_rental_id.grid(row=2, column=1)
tk.Button(frm_return, text="Calculate", command=lambda: messagebox.showinfo("Cost", calculate_rental_cost(cost_rental_id.get())), bg="orange", fg="white").grid(row=3, column=0, columnspan=2, pady=10)

# -------------------------------------------------
# TAB 4: Insights & Analytics
# -------------------------------------------------
tab_insight = ttk.Frame(notebook)
notebook.add(tab_insight, text="📊 Insights & Analytics")

# View Customer Total Spent
tk.Label(tab_insight, text="View Customer Total Spent", font=("Arial", 14, "bold")).pack(pady=10)
frm_insight = tk.Frame(tab_insight)
frm_insight.pack(pady=5)

tk.Label(frm_insight, text="Customer ID").grid(row=0, column=0)
cust_total_entry = tk.Entry(frm_insight)
cust_total_entry.grid(row=0, column=1)

def show_customer_total():
    cid = cust_total_entry.get()
    total = get_customer_total_spent(cid)
    messagebox.showinfo("Total Spent", f"Customer {cid} has spent ₹{total:.2f}")

tk.Button(frm_insight, text="Show Total Spent", command=show_customer_total, bg="green", fg="white").grid(row=1, column=0, columnspan=2, pady=10)

# Charts
tk.Label(tab_insight, text="Analytics Charts", font=("Arial", 14, "bold")).pack(pady=10)
tk.Button(tab_insight, text="Vehicle Type Distribution", command=vehicle_type_distribution, bg="purple", fg="white").pack(pady=5)
tk.Button(tab_insight, text="Top Customers by Spending", command=top_customers_by_spent, bg="brown", fg="white").pack(pady=5)

root.mainloop()
