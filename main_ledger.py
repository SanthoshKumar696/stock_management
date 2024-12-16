import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# database connection
conn=sqlite3.connect('stock.db')
cursor=conn.cursor()

# Create main_ledger table
cursor.execute("""
CREATE TABLE IF NOT EXISTS main_ledger (
    code TEXT PRIMARY KEY,
    name TEXT UNIQUE
)
""")
conn.commit()



def open_main_ledger(root):
    # Create a new window for Main Ledger
    ledger_window = tk.Toplevel()
    ledger_window.title("Main Ledger")
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    ledger_window.geometry(f"{screen_width}x{screen_height}")
    
    ledger_window.configure(bg="lightblue")

    # Frame for the left section (Radio Buttons and Inputs)
    left_frame = tk.Frame(ledger_window, bg="lightblue")
    left_frame.pack(side="left", fill="y", padx=10, pady=10)

    # Radio Button Options
    operation_var = tk.StringVar(value="Addition")  # Default selection
    tk.Label(
        left_frame, 
        text="Select Operation:", 
        font=("Arial", 12), 
        bg="lightblue"
    ).pack(anchor="w", padx=10, pady=5)

    for operation in ["Addition", "Correction", "Deletion", "View"]:
        tk.Radiobutton(
            left_frame, 
            text=operation, 
            variable=operation_var, 
            value=operation, 
            font=("Arial", 10), 
            bg="lightblue"
        ).pack(anchor="w", padx=20)

    # Input for Code
    tk.Label(
        left_frame, 
        text="Code:", 
        font=("Arial", 12), 
        bg="lightblue"
    ).pack(anchor="w", padx=10, pady=5)

    code_entry = tk.Entry(left_frame, width=30, font=("Arial", 12))
    code_entry.pack(padx=10, pady=5)

    # Input for Name
    tk.Label(
        left_frame, 
        text="Name:", 
        font=("Arial", 12), 
        bg="lightblue"
    ).pack(anchor="w", padx=10, pady=5)

    name_entry = tk.Entry(left_frame, width=30, font=("Arial", 12))
    name_entry.pack(padx=10, pady=5)

    # Save button functionality
    def save_entry():
        code = code_entry.get().strip()
        name = name_entry.get().strip()
        if code and name:
            stored_details_tree.insert("", "end", values=(code, name))
            code_entry.delete(0, tk.END)
            name_entry.delete(0, tk.END)

            try:
                cursor.execute("INSERT INTO main_ledger (code, name) VALUES (?, ?)", (code, name))
                conn.commit()
                messagebox.showinfo("Success", f"Product '{name}' added successfully!")
                code_entry.delete(0, tk.END)
                name_entry.delete(0, tk.END)
            except sqlite3.IntegrityError as e:
                messagebox.showerror("Database Error", f"Error: {e}")

        
        else:
            messagebox.showwarning("Input Error", "Please enter both Code and Name")

    # Buttons
    tk.Button(
        left_frame, 
        text="Save", 
        font=("Arial", 12), 
        bg="green", 
        fg="white", 
        width=10, 
        command=save_entry
    ).pack(pady=10)

    tk.Button(
        left_frame, 
        text="Cancel", 
        font=("Arial", 12), 
        bg="orange", 
        fg="white", 
        width=10, 
        command=lambda: [code_entry.delete(0, tk.END), name_entry.delete(0, tk.END)]
    ).pack(pady=5)

    tk.Button(
        left_frame, 
        text="Exit", 
        font=("Arial", 12), 
        bg="red", 
        fg="white", 
        width=10, 
        command=ledger_window.destroy
    ).pack(pady=5)

    # Frame for the right section (Stored Details Table)
    right_frame = tk.Frame(ledger_window, bg="lightblue")
    right_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    tk.Label(
        right_frame, 
        text="Stored Details", 
        font=("Arial", 12, "bold"), 
        bg="lightblue"
    ).pack(pady=10)

    # Treeview (Table) for displaying stored details
    columns = ("Code", "Name")
    stored_details_tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=20)
    stored_details_tree.heading("Code", text="Code")
    stored_details_tree.heading("Name", text="Name")
    stored_details_tree.column("Code", width=100, anchor="center")
    stored_details_tree.column("Name", width=200, anchor="center")
    stored_details_tree.pack(fill="both", expand=True, padx=10)

    # Preloaded data
    stored_data = []

    for item in stored_data:
        stored_details_tree.insert("", "end", values=item)
    # Add a button to close the ledger window 