import tkinter as tk
from tkinter import ttk, messagebox
from vehicle_operations import view_available_vehicles, add_vehicle
from rental_operations import add_rental, return_vehicle, calculate_rental_cost
from customer_operations import add_customer, update_customer, delete_customer
from common_operations import get_table_data, get_customer_total_spent
from analytics import vehicle_type_distribution, top_customers_by_spent
import sys
import login_screen  # for logout

def start_main_window(user, login_screen=None):
    staff_id, name, role = user[0], user[1], user[2]

    root = tk.Toplevel(login_screen)
    root.title(f"Car/Bike Rental Management System - Logged in as {name} ({role})")
    root.geometry("1100x650")

    # =======================================
    # 🔹 TOP CONTROL BAR
    # =======================================
    top_frame = tk.Frame(root, bg="#f5f5f5")
    top_frame.pack(fill="x")

    tk.Label(top_frame, text="🚗 Car/Bike Rental Management System",
             font=("Arial", 12, "bold"), bg="#f5f5f5").pack(side="left", padx=10, pady=8)

    tk.Label(top_frame, text=f"Role: {role}", bg="#f5f5f5",
             fg="blue", font=("Arial", 10, "bold")).pack(side="left", padx=10)

    # Logout and Exit buttons
    def logout():
        root.destroy()
        if login_screen:
            login_screen.deiconify()  # bring login back to front


    def exit_app():
        root.destroy()
        messagebox.showinfo("Goodbye!", "Application closed successfully.")
        if login_screen:
            login_screen.destroy()
        sys.exit()

    tk.Button(top_frame, text="Logout", bg="orange", fg="white",
              command=logout, width=10).pack(side="right", padx=10, pady=8)

    tk.Button(top_frame, text="Exit", bg="red", fg="white",
              command=exit_app, width=10).pack(side="right", pady=8)

    # =======================================
    # 🔹 MAIN NOTEBOOK (TABS)
    # =======================================
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # Define access control
    role_access = {
        "Manager": ["View", "Vehicle", "Rental", "Customer", "Analytics"],
        "Supervisor": ["View", "Rental", "Customer", "Analytics"],
        "Receptionist": ["View", "Rental", "Customer"],
        "Agent": ["View", "Customer"],
        "Clerk": ["View"]
    }

    # Tabs creation
    allowed_tabs = role_access.get(role, ["View"])  # default to minimal view

    # -------------------------------------------------
    # TAB 1: View Tables
    # -------------------------------------------------
    tab_view = ttk.Frame(notebook)
    if "View" in allowed_tabs:
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
        cols, rows = get_table_data(table_name, role=role)
        for i in tree.get_children():
            tree.delete(i)
        tree["columns"] = cols
        tree["show"] = "headings"
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        for row in rows:
            tree.insert("", "end", values=row)

    tk.Button(frame_table, text="Show Data",
              command=lambda: load_table_data(selected_table.get()), bg="blue", fg="white").pack(side="left", padx=10)

    # -------------------------------------------------
    # TAB 2: Vehicle Management
    # -------------------------------------------------
    tab_vehicle = ttk.Frame(notebook)
    if "Vehicle" in allowed_tabs:
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
        msg = add_vehicle(*vals, role=role)
        messagebox.showinfo("Vehicle", msg)
        for e in entries:
            e.delete(0, tk.END)

    tk.Button(tab_vehicle, text="Add Vehicle", command=handle_add_vehicle,
              bg="green", fg="white").pack(pady=10)

    # -------------------------------------------------
    # TAB 3: Rental Operations
    # -------------------------------------------------
    tab_rental = ttk.Frame(notebook)
    if "Rental" in allowed_tabs:
        notebook.add(tab_rental, text="📄 Rental Operations")

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

    tk.Button(frame_rent, text="Add Rental",
              command=lambda: messagebox.showinfo("Rental", add_rental(*[e.get() for e in entries_r], role=role)),
              bg="green", fg="white").grid(row=6, column=0, columnspan=2, pady=10)

    # Return Rental
    tk.Label(tab_rental, text="Return Vehicle", font=("Arial", 14, "bold")).pack(pady=10)
    frm_return = tk.Frame(tab_rental)
    frm_return.pack(pady=5)

    tk.Label(frm_return, text="Rental ID").grid(row=0, column=0)
    rental_id = tk.Entry(frm_return)
    rental_id.grid(row=0, column=1)

    tk.Button(frm_return, text="Mark Returned",
              command=lambda: messagebox.showinfo("Returned", return_vehicle(rental_id.get(), role=role)),
              bg="blue", fg="white").grid(row=1, column=0, columnspan=2, pady=10)

    # Calculate Cost (Stored Procedure)
    tk.Label(frm_return, text="Calculate Total Cost").grid(row=2, column=0, pady=5)
    cost_rental_id = tk.Entry(frm_return)
    cost_rental_id.grid(row=2, column=1)
    tk.Button(frm_return, text="Calculate",
              command=lambda: messagebox.showinfo("Cost", calculate_rental_cost(cost_rental_id.get(), role=role)),
              bg="orange", fg="white").grid(row=3, column=0, columnspan=2, pady=10)

    # -------------------------------------------------
    # TAB 4: Customer Management
    # -------------------------------------------------
    tab_customer = ttk.Frame(notebook)
    if "Customer" in allowed_tabs:
        notebook.add(tab_customer, text="👤 Customer Management")

    tk.Label(tab_customer, text="Manage Customers", font=("Arial", 14, "bold")).pack(pady=10)

    # Add Customer
    frame_add_cust = tk.LabelFrame(tab_customer, text="Add Customer", padx=10, pady=10)
    frame_add_cust.pack(fill="x", padx=20, pady=10)

    labels_add = ["Name", "Email", "Phone", "License No"]
    entries_add = {}
    for i, lbl in enumerate(labels_add):
        tk.Label(frame_add_cust, text=lbl + ":").grid(row=i, column=0, sticky="e", pady=5)
        ent = tk.Entry(frame_add_cust)
        ent.grid(row=i, column=1, padx=10)
        entries_add[lbl] = ent

    def handle_add_customer():
        vals = [entries_add["Name"].get(), entries_add["Email"].get(),
                entries_add["Phone"].get(), entries_add["License No"].get()]
        msg = add_customer(*vals, role=role)
        messagebox.showinfo("Customer", msg)
        for e in entries_add.values():
            e.delete(0, tk.END)

    tk.Button(frame_add_cust, text="Add Customer", command=handle_add_customer,
              bg="green", fg="white", width=15).grid(row=len(labels_add), column=0, columnspan=2, pady=10)

    # Update Customer
    frame_update_cust = tk.LabelFrame(tab_customer, text="Update Customer", padx=10, pady=10)
    frame_update_cust.pack(fill="x", padx=20, pady=10)

    labels_upd = ["Customer ID", "Name", "Email", "Phone", "License No"]
    entries_upd = {}
    for i, lbl in enumerate(labels_upd):
        tk.Label(frame_update_cust, text=lbl + ":").grid(row=i, column=0, sticky="e", pady=5)
        ent = tk.Entry(frame_update_cust)
        ent.grid(row=i, column=1, padx=10)
        entries_upd[lbl] = ent

    def handle_update_customer():
        cust_id = entries_upd["Customer ID"].get()
        vals = {
            "name": entries_upd["Name"].get(),
            "email": entries_upd["Email"].get(),
            "phone": entries_upd["Phone"].get(),
            "license_no": entries_upd["License No"].get()
        }
        msg = update_customer(cust_id, **vals, role=role)
        messagebox.showinfo("Customer", msg)
        for e in entries_upd.values():
            e.delete(0, tk.END)

    tk.Button(frame_update_cust, text="Update Customer", command=handle_update_customer,
              bg="blue", fg="white", width=15).grid(row=len(labels_upd), column=0, columnspan=2, pady=10)

    # Delete Customer
    frame_delete_cust = tk.LabelFrame(tab_customer, text="Delete Customer", padx=10, pady=10)
    frame_delete_cust.pack(fill="x", padx=20, pady=10)

    tk.Label(frame_delete_cust, text="Customer ID:").grid(row=0, column=0, sticky="e", pady=5)
    entry_del = tk.Entry(frame_delete_cust)
    entry_del.grid(row=0, column=1, padx=10)

    def handle_delete_customer():
        cust_id = entry_del.get()
        msg = delete_customer(cust_id, role=role)
        messagebox.showinfo("Customer", msg)
        entry_del.delete(0, tk.END)

    tk.Button(frame_delete_cust, text="Delete Customer", command=handle_delete_customer,
              bg="red", fg="white", width=15).grid(row=1, column=0, columnspan=2, pady=10)

    # -------------------------------------------------
    # TAB 5: Insights & Analytics
    # -------------------------------------------------
    tab_insight = ttk.Frame(notebook)
    if "Analytics" in allowed_tabs:
        notebook.add(tab_insight, text="📊 Insights & Analytics")

    tk.Label(tab_insight, text="View Customer Total Spent", font=("Arial", 14, "bold")).pack(pady=10)
    frm_insight = tk.Frame(tab_insight)
    frm_insight.pack(pady=5)

    tk.Label(frm_insight, text="Customer ID").grid(row=0, column=0)
    cust_total_entry = tk.Entry(frm_insight)
    cust_total_entry.grid(row=0, column=1)

    def show_customer_total():
        cid = cust_total_entry.get()
        total = get_customer_total_spent(cid, role=role)
        messagebox.showinfo("Total Spent", f"Customer {cid} has spent ₹{total:.2f}")

    tk.Button(frm_insight, text="Show Total Spent", command=show_customer_total,
              bg="green", fg="white").grid(row=1, column=0, columnspan=2, pady=10)

    # Charts
    tk.Label(tab_insight, text="Analytics Charts", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Button(tab_insight, text="Vehicle Type Distribution", command=vehicle_type_distribution,
              bg="purple", fg="white").pack(pady=5)
    tk.Button(tab_insight, text="Top Customers by Spending", command=top_customers_by_spent,
              bg="brown", fg="white").pack(pady=5)

    root.mainloop()
