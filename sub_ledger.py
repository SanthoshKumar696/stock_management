import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database connection
conn = sqlite3.connect('stock.db')
cursor = conn.cursor()

# Create sub_ledger table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sub_ledger(
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    main_product TEXT,
    code TEXT,
    name TEXT,
    credit_period_days INTEGER,
    FOREIGN KEY (main_product) REFERENCES main_ledger(name))
""")
conn.commit()


# Fetch main products from the main_ledger table
def fetch_main_products():
    cursor.execute("SELECT name FROM main_ledger")
    return [row[0] for row in cursor.fetchall()]

def open_sub_ledger(root):  # Start the Sub Ledger page

    # Create a new window for Sub Ledger
    sub_ledger_window = tk.Toplevel(root)
    sub_ledger_window.title("Sub Ledger")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    sub_ledger_window.geometry(f"{screen_width}x{screen_height}")
    sub_ledger_window.configure(bg="lightblue")

    # Variables for input fields
    operation_var = tk.StringVar(value="Addition")  # Default radio button selection
    main_ledger_var = tk.StringVar()  # Dropdown selection
    code_var = tk.StringVar()
    name_var = tk.StringVar()
    credit_period_var = tk.StringVar()
    last_name_var = tk.StringVar()

    # First Line: Radio Buttons for Operations
    tk.Label(
        sub_ledger_window,
        text="Select Operation:",
        font=("Arial", 12, "bold"),
        bg="lightblue"
    ).grid(row=0, column=0, sticky="w", padx=10, pady=10)

    operations = ["Addition", "Correction", "Deletion", "View"]
    for i, operation in enumerate(operations):
        tk.Radiobutton(
            sub_ledger_window,
            text=operation,
            variable=operation_var,
            value=operation,
            font=("Arial", 10),
            bg="lightblue"
        ).grid(row=0, column=i + 1, padx=10)

    # Second Line: Main Ledger Dropdown
    tk.Label(
        sub_ledger_window,
        text="Main Ledger:",
        font=("Arial", 12),
        bg="lightblue"
    ).grid(row=1, column=0, sticky="w", padx=10, pady=10)

    main_ledger_dropdown = ttk.Combobox(
        sub_ledger_window,
        textvariable=main_ledger_var,
        values=fetch_main_products(),
        state="readonly",
        width=30
    )
    main_ledger_dropdown.grid(row=1, column=1, columnspan=3, padx=10, pady=10)

    # Third Line: Code
    tk.Label(
        sub_ledger_window,
        text="Code:",
        font=("Arial", 12),
        bg="lightblue"
    ).grid(row=2, column=0, sticky="w", padx=10, pady=10)

    code_entry = tk.Entry(
        sub_ledger_window,
        textvariable=code_var,
        font=("Arial", 12),
        width=30
    )
    code_entry.grid(row=2, column=1, columnspan=3, padx=10, pady=10)

    # Fourth Line: Name
    tk.Label(
        sub_ledger_window,
        text="Name:",
        font=("Arial", 12),
        bg="lightblue"
    ).grid(row=3, column=0, sticky="w", padx=10, pady=10)

    name_entry = tk.Entry(
        sub_ledger_window,
        textvariable=name_var,
        font=("Arial", 12),
        width=30
    )
    name_entry.grid(row=3, column=1, columnspan=3, padx=10, pady=10)

    # Fifth Line: Credit Period
    tk.Label(
        sub_ledger_window,
        text="Credit Period (Days):",
        font=("Arial", 12),
        bg="lightblue"
    ).grid(row=4, column=0, sticky="w", padx=10, pady=10)

    credit_period_entry = tk.Entry(
        sub_ledger_window,
        textvariable=credit_period_var,
        font=("Arial", 12),
        width=30
    )
    credit_period_entry.grid(row=4, column=1, columnspan=3, padx=10, pady=10)

    # Sixth Line: Last Name
    tk.Label(
        sub_ledger_window,
        text="Last Name:",
        font=("Arial", 12),
        bg="lightblue"
    ).grid(row=5, column=0, sticky="w", padx=10, pady=10)

    last_name_entry = tk.Entry(
        sub_ledger_window,
        textvariable=last_name_var,
        font=("Arial", 12),
        width=30
    )
    last_name_entry.grid(row=5, column=1, columnspan=3, padx=10, pady=10)

    # Right-side Frame to Show Entered Details
    details_frame = tk.Frame(sub_ledger_window, bg="lightgray", width=400, height=300)
    details_frame.grid(row=0, column=4, rowspan=7, padx=20, pady=10)

    # Function to update and display entered details in the right-side box
    def display_entered_details():
        # Get the entered values
        operation = operation_var.get()
        main_ledger = main_ledger_var.get()
        code = code_var.get()
        name = name_var.get()
        credit_period = credit_period_var.get()
        last_name = last_name_var.get()

        # Clear previous details
        for widget in details_frame.winfo_children():
            widget.destroy()

        # Display the new details in a label
        details_label = tk.Label(
            details_frame,
            text=f"Operation: {operation}\n"
                 f"Main Ledger: {main_ledger}\n"
                 f"Code: {code}\n"
                 f"Name: {name}\n"
                 f"Credit Period: {credit_period} days\n"
                 f"Last Name: {last_name}",
            font=("Arial", 12),
            bg="lightgray",
            justify="left"
        )
        details_label.pack(padx=10, pady=10)

    # Save Entry Function
    def save_entry():
        # Extract values from StringVar objects
        operation = operation_var.get()
        main_ledger = main_ledger_var.get()
        code = code_var.get()
        name = name_var.get()
        credit_period = credit_period_var.get()
        last_name = last_name_var.get()

        # Validate that all fields are filled
        if operation and main_ledger and code and name and credit_period and last_name:
            try:
                # Convert credit_period to an integer (if applicable)
                credit_period = int(credit_period)

                # Execute SQL insert
                cursor.execute(
                    "INSERT INTO sub_ledger (main_product, code, name, credit_period_days) VALUES (?, ?, ?, ?)",
                    (main_ledger, code, name, credit_period)
                )
                conn.commit()

                # Display success message
                messagebox.showinfo("Success", f"Sub-product '{name}' added under '{main_ledger}'!")

                # Clear entry fields after saving
                code_entry.delete(0, tk.END)
                name_entry.delete(0, tk.END)
                credit_period_entry.delete(0, tk.END)
                main_ledger_dropdown.set("")
                last_name_entry.delete(0, tk.END)

            except sqlite3.IntegrityError as e:
                # Handle database-specific errors, such as duplicate codes
                messagebox.showerror("Database Error", f"Error: {e}")
            except ValueError:
                # Handle invalid credit_period input
                messagebox.showerror("Invalid Input", "Credit Period must be an integer.")
        else:
            # Show warning if any fields are empty
            messagebox.showwarning("Missing Fields", "Please fill all the fields!")

    # Cancel Entry Function
    def cancel_entry():
        # Clear all fields
        operation_var.set("Addition")
        main_ledger_var.set("")
        code_var.set("")
        name_var.set("")
        credit_period_var.set("")
        last_name_var.set("")

    # Buttons
    tk.Button(
        sub_ledger_window,
        text="Save",
        font=("Arial", 12),
        bg="green",
        fg="white",
        width=10,
        command=save_entry
    ).grid(row=6, column=0, pady=20)

    tk.Button(
        sub_ledger_window,
        text="Cancel",
        font=("Arial", 12),
        bg="orange",
        fg="white",
        width=10,
        command=cancel_entry
    ).grid(row=6, column=1, pady=20)

    tk.Button(
        sub_ledger_window,
        text="Exit",
        font=("Arial", 12),
        bg="red",
        fg="white",
        width=10,
        command=sub_ledger_window.destroy
    ).grid(row=6, column=2, pady=20)

    tk.Button(
        sub_ledger_window,
        text="Name List",
        font=("Arial", 12),
        bg="blue",
        fg="white",
        width=10,
        command=lambda: messagebox.showinfo("Name List", "Display the name list logic here.")
    ).grid(row=6, column=3, pady=20)

    
     

    # Function to display names in the sub_ledger table
    def display_name_list():
        try:
            cursor.execute("SELECT name FROM sub_ledger")
            names = cursor.fetchall()
            if names:
                name_list = "\n".join(name[0] for name in names)
                messagebox.showinfo("Name List", f"Names in Sub Ledger:\n{name_list}")
            else:
                messagebox.showinfo("Name List", "No names found in Sub Ledger.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")

    # Update Name List button command
    tk.Button(
        sub_ledger_window,
        text="Name List",
        font=("Arial", 12),
        bg="blue",
        fg="white",
        width=10,
        command=display_name_list
    ).grid(row=6, column=3, pady=20)

