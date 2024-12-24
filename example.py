import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database Setup
def setup_database():
    conn = sqlite3.connect('cash_receipt.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS receipts (
        id INTEGER PRIMARY KEY,
        name TEXT,
        amount REAL,
        date TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Add New Data to Database
def add_data(name, amount, date):
    conn = sqlite3.connect('cash_receipt.db')
    c = conn.cursor()
    c.execute('INSERT INTO receipts (name, amount, date) VALUES (?, ?, ?)', (name, amount, date))
    conn.commit()
    conn.close()

# Fetch All Data from Database
def fetch_data():
    conn = sqlite3.connect('cash_receipt.db')
    c = conn.cursor()
    c.execute('SELECT * FROM receipts')
    rows = c.fetchall()
    conn.close()
    return rows

# Update Data in Database
def update_data(record_id, name, amount, date):
    conn = sqlite3.connect('cash_receipt.db')
    c = conn.cursor()
    c.execute('UPDATE receipts SET name = ?, amount = ?, date = ? WHERE id = ?', (name, amount, date, record_id))
    conn.commit()
    conn.close()

# Refresh Treeview
def refresh_treeview():
    for item in tree.get_children():
        tree.delete(item)

    for row in fetch_data():
        tree.insert('', tk.END, values=row)

# Save or Update Data
def save_or_update():
    name = name_entry.get()
    amount = amount_entry.get()
    date = date_entry.get()

    if not name or not amount or not date:
        messagebox.showerror("Missing Information", "All fields are required.")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Invalid Input", "Amount must be a valid number.")
        return

    if save_button["text"] == "Save":
        # Save new data
        add_data(name, amount, date)
        messagebox.showinfo("Success", "Record added successfully!")
    else:
        # Update existing data
        global selected_id
        update_data(selected_id, name, amount, date)
        messagebox.showinfo("Success", "Record updated successfully!")
        save_button["text"] = "Save"

    refresh_treeview()
    clear_fields()

# Load Selected Row for Correction
def load_for_correction():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a record to modify.")
        return

    record = tree.item(selected_item[0], "values")
    global selected_id
    selected_id = record[0]

    # Populate fields with selected data
    name_entry.delete(0, tk.END)
    name_entry.insert(0, record[1])
    amount_entry.delete(0, tk.END)
    amount_entry.insert(0, record[2])
    date_entry.delete(0, tk.END)
    date_entry.insert(0, record[3])

    save_button["text"] = "Update"

# Clear Input Fields
def clear_fields():
    name_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    save_button["text"] = "Save"

# Main Application
root = tk.Tk()
root.title("Cash Receipt Manager")

setup_database()

# Form Fields
tk.Label(root, text="Name").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Amount").grid(row=1, column=0, padx=5, pady=5)
amount_entry = tk.Entry(root)
amount_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Date").grid(row=2, column=0, padx=5, pady=5)
date_entry = tk.Entry(root)
date_entry.grid(row=2, column=1, padx=5, pady=5)

# Save Button
save_button = tk.Button(root, text="Save", command=save_or_update)
save_button.grid(row=3, column=0, columnspan=2, pady=10)

# Treeview
columns = ("id", "name", "amount", "date")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("id", text="ID")
tree.heading("name", text="Name")
tree.heading("amount", text="Amount")
tree.heading("date", text="Date")
tree.grid(row=4, column=0, columnspan=2, pady=10)

# Correction Button
correction_button = tk.Button(root, text="Correction", command=load_for_correction)
correction_button.grid(row=5, column=0, columnspan=2, pady=10)

# Initialize Treeview
refresh_treeview()

root.mainloop()
