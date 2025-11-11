import tkinter as tk
from tkinter import ttk, messagebox
from rental_operations import add_rental, return_vehicle, calculate_rental_cost
from vehicle_operations import view_available_vehicles, add_vehicle, delete_vehicle
from common_operations import get_table_data, get_customer_total_spent
from analytics import vehicle_type_distribution, top_customers_by_spent
import login_screen

def start_main_window(user):
    root = tk.Tk()
    root.title(f"Car/Bike Rental Management System - Logged in as {user[1]} ({user[2]})")
    root.geometry("1100x650")

    # ==========================
    # 🔹 TOP CONTROL BAR
    # ==========================
    top_frame = tk.Frame(root, bg="#f5f5f5")
    top_frame.pack(fill="x")

    # App title (left)
    tk.Label(top_frame, text="🚗 Car/Bike Rental Management System",
             font=("Arial", 12, "bold"), bg="#f5f5f5").pack(side="left", padx=10, pady=8)

    # 🔹 Logout button
    def logout():
        root.destroy()
        login_screen.open_login_window()  # Reopen login window

    # 🔹 Exit button
    def exit_app():
        root.destroy()
        messagebox.showinfo("Goodbye!", "Application closed successfully.")
        root.quit()

    # Buttons (right)
    btn_logout = tk.Button(top_frame, text="Logout", bg="orange", fg="white",
                           command=logout, width=10)
    btn_logout.pack(side="right", padx=10, pady=8)

    btn_exit = tk.Button(top_frame, text="Exit", bg="red", fg="white",
                         command=exit_app, width=10)
    btn_exit.pack(side="right", pady=8)

    # ==========================
    # 🔹 TAB CONTROL
    # ==========================
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

    tk.Button(frame_table, text="Show Data", command=lambda: load_table_data(selected_table.get()), bg="blue", fg="white", relief="flat", cursor="hand2", font=("Arial", 10, "bold")
).pack(side="left", padx=10)

    # -------------------------------------------------
    # TAB 2: Vehicle Management
    # -------------------------------------------------
    # -------------------------------------------------
    # ADD VEHICLE SECTION
    # -------------------------------------------------
    tab_vehicle = ttk.Frame(notebook)
    notebook.add(tab_vehicle, text="🚗 Vehicle Management")

    tk.Label(tab_vehicle, text="Add New Vehicle", font=("Arial", 14, "bold")).pack(pady=10)
    frame_add_vehicle = tk.Frame(tab_vehicle)
    frame_add_vehicle.pack(pady=10)

    labels = ["Reg No", "Type (Car/Bike)", "Brand", "Model", "Rent Price", "Branch ID"]
    entries = []
    type_var = tk.StringVar()

    for i, lbl in enumerate(labels):
        tk.Label(frame_add_vehicle, text=lbl).grid(row=i, column=0, sticky="e", pady=5)

        if lbl == "Type (Car/Bike)":
            dropdown = ttk.Combobox(frame_add_vehicle, textvariable=type_var, values=["Car", "Bike"], state="readonly")
            dropdown.grid(row=i, column=1, padx=10)
            dropdown.current(0)
            entries.append(dropdown)
        else:
            ent = tk.Entry(frame_add_vehicle)
            ent.grid(row=i, column=1, padx=10)
            entries.append(ent)

    def handle_add_vehicle():
        vals = [e.get() for e in entries]
        msg = add_vehicle(*vals)
        messagebox.showinfo("Result", msg)
        for e in entries:
            e.delete(0, tk.END)
        entries[1].set("")  # reset dropdown

    tk.Button(tab_vehicle, text="Add Vehicle", command=handle_add_vehicle, bg="green", fg="white").pack(pady=10)

    # -------------------------------------------------
    # DELETE VEHICLE SECTION
    # -------------------------------------------------
    tk.Label(tab_vehicle, text="Delete Vehicle", font=("Arial", 14, "bold")).pack(pady=10)

    frame_delete_vehicle = tk.Frame(tab_vehicle)
    frame_delete_vehicle.pack(pady=5)

    tk.Label(frame_delete_vehicle, text="Enter Vehicle ID:").grid(row=0, column=0, padx=10, pady=5)
    delete_entry = tk.Entry(frame_delete_vehicle)
    delete_entry.grid(row=0, column=1, padx=10, pady=5)

    def handle_delete_vehicle():
        vid = delete_entry.get()
        if not vid.strip():
            messagebox.showwarning("Input Error", "Please enter a Vehicle ID.")
            return

        result = delete_vehicle(vid)
        messagebox.showinfo("Delete Vehicle", result)
        delete_entry.delete(0, tk.END)

        load_table_data("Vehicle")

    tk.Button(frame_delete_vehicle, text="Delete", command=handle_delete_vehicle,
            bg="red", fg="white").grid(row=1, column=0, columnspan=2, pady=10)

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
