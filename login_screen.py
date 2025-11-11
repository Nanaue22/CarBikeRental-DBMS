# login_screen.py
# ----------------
import tkinter as tk
from tkinter import messagebox
from auth_operations import login_staff, signup_staff
import main  # to open dashboard after login

# 🔹 Login Window
def open_login_window():
    login = tk.Tk()
    login.title("Staff Login")
    login.geometry("400x350")

    tk.Label(login, text="Staff Login", font=("Arial", 16, "bold")).pack(pady=10)

    tk.Label(login, text="Staff ID:").pack()
    entry_id = tk.Entry(login)
    entry_id.pack()

    tk.Label(login, text="Password:").pack()
    entry_pw = tk.Entry(login, show="*")
    entry_pw.pack()

    def attempt_login():
        staff_id = entry_id.get()
        password = entry_pw.get()
        user = login_staff(staff_id, password)
        if isinstance(user, str):  # DB error
            messagebox.showerror("Error", user)
        elif user:
            messagebox.showinfo("Success", f"Welcome, {user[1]} ({user[2]})!")
            login.destroy()
            main.start_main_window(user)  # open main dashboard
        else:
            messagebox.showerror("Login Failed", "Invalid Staff ID or Password.")

    tk.Button(login, text="Login", command=attempt_login, bg="green", fg="white").pack(pady=10)
    tk.Button(login, text="Sign Up", command=lambda: open_signup_window(login), bg="blue", fg="white").pack()

    login.mainloop()


# 🔹 Signup Window
def open_signup_window(parent):
    parent.destroy()
    signup = tk.Tk()
    signup.title("Staff Sign Up")
    signup.geometry("400x450")

    tk.Label(signup, text="Create New Account", font=("Arial", 16, "bold")).pack(pady=10)

    fields = ["Name", "Role", "Email", "Password", "Branch ID"]
    entries = {}
    for field in fields:
        tk.Label(signup, text=field + ":").pack()
        ent = tk.Entry(signup, show="*" if field == "Password" else None)
        ent.pack()
        entries[field] = ent

    def create_account():
        data = [entries[f].get() for f in fields]
        msg = signup_staff(*data)
        messagebox.showinfo("Signup Status", msg)
        if "successfully" in msg:
            signup.destroy()
            open_login_window()

    tk.Button(signup, text="Sign Up", command=create_account, bg="green", fg="white").pack(pady=15)
    tk.Button(signup, text="Back to Login", command=lambda: [signup.destroy(), open_login_window()],
              bg="gray", fg="white").pack()

    signup.mainloop()


if __name__ == "__main__":
    open_login_window()
