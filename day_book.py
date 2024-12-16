import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# Database connection
conn = sqlite3.connect('stock.db')
cursor = conn.cursor()


def fetch_transactions(from_date, to_date):
    try:
        # Validate date format
        from_date_obj = datetime.strptime(from_date, "%d-%m-%Y")
        to_date_obj = datetime.strptime(to_date, "%d-%m-%Y")

        cursor.execute("SELECT * FROM saved_data WHERE date BETWEEN ? AND ? order by date", (from_date, to_date))
                        
        rows = cursor.fetchall()
        return rows
    except ValueError:
        messagebox.showerror("Date Error", "Invalid date format! Use YYYY-MM-DD.")
        return []
# Function to display the Day Book window
def day_book(root):
    # Create a new window for Day Book
    day_book_window = tk.Toplevel()
    day_book_window.title("Day Book")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    day_book_window.geometry(f"{screen_width}x{screen_height}")
    day_book_window.configure(bg="lightblue")


    # Function to fetch transactions from the database
    

    def show_report():
        from_date = from_date_entry.get()
        to_date = to_date_entry.get()

        if not from_date or not to_date:
            messagebox.showerror("Input Error", "Both dates are required!")
            return

        transactions = fetch_transactions(from_date, to_date)
        
        if transactions:
            report_window = tk.Toplevel(root)
            report_window.title("Transaction Report")

            columns = ("ID", "Date", "Transaction", "Party Name", "Main Product", "Sub Product", "Gross Wt", "Stones", "Touch", "Net Wt", "MC@", "MC", "Rate", "Amount", "Narration")
            tree = ttk.Treeview(report_window, columns=columns, show="headings")
            tree.heading("ID", text="ID")
            tree.heading("Date", text="Date")
            tree.heading("Party Name", text="Party Name")
            tree.heading("Main Product", text="Main Product")
            tree.heading("Sub Product", text="Sub Product")
            tree.heading("Gross Wt", text="Gross Wt")
            tree.heading("Stones", text="Stones")
            tree.heading("Touch", text="Touch")
            tree.heading("Net Wt", text="Net Wt")
            tree.heading("MC@", text="MC@")
            tree.heading("MC", text="MC")
            tree.heading("Rate", text="Rate")
            tree.heading("Amount", text="Amount")
            tree.heading("Narration", text="Narration")
            
            for row in transactions:
                tree.insert("", tk.END, values=row)

            tree.pack(fill=tk.BOTH, expand=True)
        else:
            messagebox.showinfo("No Data", "No transactions found for the given date range.")

    # Add a big and bold heading for Day Book
    tk.Label(
        day_book_window,
        text="Day Book",
        font=("Arial", 24, "bold"),
        bg="lightblue",
        fg="darkblue"
    ).pack(pady=10)

    # From Date input
    from_date_frame = tk.Frame(day_book_window, bg="lightblue")
    from_date_frame.pack(pady=10)

    tk.Label(
        from_date_frame,
        text="From Date:",
        font=("Arial", 14),
        bg="lightblue"
    ).grid(row=0, column=0, padx=5, pady=5, sticky="w")

    from_date_entry = tk.Entry(from_date_frame, font=("Arial", 14), width=20)
    from_date_entry.grid(row=0, column=1, padx=5, pady=5)

    # To Date input
    to_date_frame = tk.Frame(day_book_window, bg="lightblue")
    to_date_frame.pack(pady=10)

    tk.Label(
        to_date_frame,
        text="To Date:",
        font=("Arial", 14),
        bg="lightblue"
    ).grid(row=0, column=0, padx=5, pady=5, sticky="w")

    to_date_entry = tk.Entry(to_date_frame, font=("Arial", 14), width=20)
    to_date_entry.grid(row=0, column=1, padx=5, pady=5)

    # Buttons
    button_frame = tk.Frame(day_book_window, bg="lightblue")
    button_frame.pack(pady=20)

    # Report Button
    tk.Button(
        button_frame,
        text="Report",
        font=("Arial", 12),
        bg="green",
        fg="white",
        width=10,
        command=show_report()
    ).grid(row=0, column=0, padx=10)

    # Clear Button
    tk.Button(
        button_frame,
        text="Clear",
        font=("Arial", 12),
        bg="orange",
        fg="white",
        width=10,
        command=lambda: [from_date_entry.delete(0, tk.END), to_date_entry.delete(0, tk.END)]
    ).grid(row=0, column=1, padx=10)

    # Exit Button
    tk.Button(
        button_frame,
        text="Exit",
        font=("Arial", 12),
        bg="red",
        fg="white",
        width=10,
        command=day_book_window.destroy
    ).grid(row=0, column=2, padx=10)



    root.mainloop()
