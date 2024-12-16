import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3
from main_ledger import open_main_ledger
from sub_ledger import open_sub_ledger
from main_product import open_main_product
from sub_product import open_sub_product
from opening_balance import opening_balance
from opening_stock import opening_stock
from party_balance import party_balance
from party_ledger import party_ledger
from receipt_issue import recepit_issue
from day_book import day_book


# Database connection
conn = sqlite3.connect('stock.db')
cursor = conn.cursor()

# Function to handle exit menu action
def exit_program():
    root.quit()

#### fetch main_ledger value for main_product
def fetch_main_ledger():
    try:
        cursor.execute("SELECT UPPER(name) FROM main_ledger")
        return [row[0] for row in cursor.fetchall()]
    except sqlite3.OperationalError as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
        return []


#### fetch sub_ledger value for sub_product
def fetch_sub_ledger(selected_main_product):
    try:
        cursor.execute("SELECT UPPER(name) FROM sub_ledger WHERE UPPER(main_product) = ?", (selected_main_product.upper(),))

        return [row[0] for row in cursor.fetchall()]
    except sqlite3.OperationalError as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
        return []

def update_sub_products(event):
    selected_main_product = main_product_combo.get()
    print(f"Selected Main Product: {selected_main_product}")
    if selected_main_product:
        sub_products = fetch_sub_ledger(selected_main_product)
        print(f"Sub Products: {sub_products}")
        sub_product_combo['values'] = sub_products
        sub_product_combo.set("")  # Clear the current selection
    else:
        sub_product_combo['values'] = []
        sub_product_combo.set("")

# Transactions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saved_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        name TEXT,
        "transaction" TEXT,
        main_product TEXT NOT NULL,
        sub_product TEXT NOT NULL,
        gross_wt REAL NOT NULL,
        stones INTEGER,
        touch REAL,
        net_wt REAL NOT NULL,
        mc_at REAL,
        mc REAL,
        rate REAL NOT NULL,
        amount REAL NOT NULL,
        narration TEXT
    )
    """)


# Functionality for buttons
def add_item():
    sl_no = len(tree.get_children()) + 1
    date = date_entry.get()
    name = party_entry.get()
    transaction = transaction_combo.get()
    main_product = main_product_combo.get()
    sub_product = sub_product_combo.get()
    gross_wt = gross_wt_entry.get()
    stones = stones_entry.get()
    touch = touch_entry.get()
    net_wt = net_wt_entry.get()
    mc_at = mc_at_entry.get()
    mc = mc_entry.get()
    rate = rate_entry.get()
    amount = amount_entry.get()
    narration = narration_entry.get()

    if name and transaction and gross_wt:
        tree.insert("", "end", values=(sl_no, date, name,main_product,sub_product, transaction, gross_wt, stones, touch, net_wt, mc_at, mc, rate, amount, narration))
        clear_fields()

    else:
        messagebox.showerror("Input Error", "Please fill all required fields.")

    try:
        amount = float(amount)
        cursor.execute("""
        INSERT INTO saved_data (date, "transaction", name, main_product, sub_product, gross_wt, stones, touch, net_wt, mc_at, mc, rate, amount, narration)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (date,transaction,name, main_product, sub_product, gross_wt, stones, touch, net_wt, mc_at, mc, rate, amount,narration))
        conn.commit()
        messagebox.showinfo("Success", 
                            f"Date : {date},\nTransaction : {transaction}, \nCustomer Name : {name}, \nMain Product : {main_product}, \nSub Product : {sub_product}, \nGross Wt : {gross_wt}, \nStones : {stones}, \nTouch : {touch}, \nNetWt : {net_wt}, \nMC@ : {mc_at}, \nMC : {mc}, \nRate : {rate}, \nAmount : {amount}, \nNarration : {narration}\n"
                            "Receipt saved successfully!")
        
        
        # Clear input fields
        date_entry.delete(0, tk.END)
        name.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        main_product_combo.set("")
        sub_product_combo.set("")
    except ValueError:
        messagebox.showerror("Input Error", "Amount must be a number!")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

def delete_item():
    selected_item = tree.selection()
    if selected_item:
        tree.delete(selected_item)
    else:
        messagebox.showerror("Selection Error", "Please select an item to delete.")

def clear_fields():
    party_entry.delete(0, tk.END)
    gross_wt_entry.delete(0, tk.END)
    stones_entry.delete(0, tk.END)
    touch_entry.delete(0, tk.END)
    net_wt_entry.delete(0, tk.END)
    mc_at_entry.delete(0, tk.END)
    mc_entry.delete(0, tk.END)
    rate_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    narration_entry.delete(0, tk.END)


def save_items():
    items = tree.get_children()
    if items:
        with open("jewelry_data.csv", "w") as file:
            file.write("SLNo,Name,Transaction,Gross,Stones,Touch,Net Weight,MC@,MC,Rate,Amount,Narration\n")
            for item in items:
                values = tree.item(item, "values")
                file.write(",".join(values) + "\n")
        messagebox.showinfo("Save Success", "Data saved to jewelry_data.csv")
    else:
        messagebox.showerror("Save Error", "No data to save.")



root = tk.Tk()
root.title("Jewelry Management System")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(f"{screen_width}x{screen_height}")
root.configure(bg="lightpink")

# Create menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

master_menu = tk.Menu(menu_bar, tearoff=0)
transaction_menu = tk.Menu(menu_bar, tearoff=0)
report_menu = tk.Menu(menu_bar, tearoff=0)
utility_menu = tk.Menu(menu_bar, tearoff=0)
exit_menu = tk.Menu(menu_bar, tearoff=0)

menu_bar.add_cascade(label="Master", menu=master_menu)
menu_bar.add_cascade(label="Transaction", menu=transaction_menu)
menu_bar.add_cascade(label="Report", menu=report_menu)
menu_bar.add_cascade(label="Utility", menu=utility_menu)
menu_bar.add_cascade(label="Exit", menu=exit_menu)

#Master #### Adding submenu of master menu
master_menu.add_command(label="Main Ledger", command=lambda:open_main_ledger(root))
master_menu.add_command(label="Sub Ledger", command=lambda:open_sub_ledger(root))
master_menu.add_command(label="Main Product", command=lambda:open_main_product(root))
master_menu.add_command(label="Sub Product", command=lambda:open_sub_product(root))
master_menu.add_command(label="Opening Stock", command=lambda:opening_stock(root)) #######
master_menu.add_command(label="Party Opening Balance", command=lambda:opening_balance(root)) #####

#Transaction
# Adding submenu items to the Trasaction menu
transaction_menu.add_command(label="Recepit & Issue", command=lambda:recepit_issue(root))

#Report
# Adding submenu items to the Report menu
report_menu.add_command(label="DayBook", command=lambda:day_book(root))
report_menu.add_command(label="PartyLedger", command=lambda:party_ledger(root))
report_menu.add_command(label="Party Balance", command=lambda:party_balance(root))

#Exit
exit_menu.add_command(label="Exit", command=exit_program)

cash_receipt_label = tk.Label(root, text="Cash Receipt", font=("Arial", 14, "bold"), bg="lightpink", fg="red")
cash_receipt_label.pack(pady=10)

# Top Frame - Row 1: Basic Details
top_frame = tk.Frame(root, bg="lightpink")
top_frame.pack(pady=5)

tk.Label(top_frame, text="Date (DD-MM-YYYY):", bg="lightpink", font=("Arial", 10)).grid(row=0, column=0, padx=5)
date_entry = tk.Entry(top_frame, width=15)
date_entry.insert(0,datetime.now().strftime("%d-%m-%Y"))
date_entry.grid(row=0, column=1, padx=5)

tk.Label(top_frame, text="Transaction:", bg="lightpink", font=("Arial", 10)).grid(row=0, column=2, padx=5)
transaction_combo = ttk.Combobox(top_frame, values=["Cash Receipt", "Invoice", "Payment"], width=15)
transaction_combo.grid(row=0, column=3, padx=5)

tk.Label(top_frame, text="Party Name:", bg="lightpink", font=("Arial", 10)).grid(row=0, column=4, padx=5)
party_entry = tk.Entry(top_frame, width=20)
party_entry.grid(row=0, column=5, padx=5)

# Middle Frame - Row 2: Product Details
middle_frame = tk.Frame(root, bg="lightpink")
middle_frame.pack(pady=5)

tk.Label(middle_frame, text="Main Product:", bg="lightpink", font=("Arial", 10)).grid(row=0, column=0, padx=5)
main_product_combo = ttk.Combobox(middle_frame, values=fetch_main_ledger(), state="readonly",width=20)
main_product_combo.grid(row=0, column=1, padx=5)
main_product_combo.bind("<<ComboboxSelected>>",update_sub_products)

tk.Label(middle_frame, text="Sub Product:", bg="lightpink", font=("Arial", 10)).grid(row=0, column=2, padx=5)
sub_product_combo = ttk.Combobox(middle_frame, state="readonly", width=20)
sub_product_combo.grid(row=0, column=3, padx=5)

tk.Label(middle_frame, text="Gross Wt:", bg="lightpink", font=("Arial", 10)).grid(row=0, column=4, padx=5)
gross_wt_entry = tk.Entry(middle_frame, width=10)
gross_wt_entry.grid(row=0, column=5, padx=5)

tk.Label(middle_frame, text="Stones:", bg="lightpink", font=("Arial", 10)).grid(row=0, column=6, padx=5)
stones_entry = tk.Entry(middle_frame, width=10)
stones_entry.grid(row=0, column=7, padx=5)

# Bottom Frame - Row 3: Additional Details
bottom_frame = tk.Frame(root, bg="lightpink")
bottom_frame.pack(pady=5)

tk.Label(bottom_frame, text="Touch:", bg="lightpink", font=("Arial", 10)).grid(row=0, column=0, padx=5)
touch_entry = tk.Entry(bottom_frame, width=10)
touch_entry.grid(row=0, column=1, padx=5)

tk.Label(bottom_frame, text="Net Wt:", bg="lightpink", font=("Arial", 10)).grid(row=0, column=2, padx=5)
net_wt_entry = tk.Entry(bottom_frame, width=10)
net_wt_entry.grid(row=0, column=3, padx=5)

tk.Label(bottom_frame, text="MC@:", bg="lightpink", font=("Arial", 10)).grid(row=0, column=4, padx=5)
mc_at_entry = tk.Entry(bottom_frame, width=10)
mc_at_entry.grid(row=0, column=5, padx=5)

tk.Label(bottom_frame, text="MC:", bg="lightpink", font=("Arial", 10)).grid(row=0, column=6, padx=5)
mc_entry = tk.Entry(bottom_frame, width=10)
mc_entry.grid(row=0, column=7, padx=5)

tk.Label(bottom_frame, text="Rate:", bg="lightpink", font=("Arial", 10)).grid(row=1, column=0, padx=5)
rate_entry = tk.Entry(bottom_frame, width=10)
rate_entry.grid(row=1, column=1, padx=5)

tk.Label(bottom_frame, text="Amount:", bg="lightpink", font=("Arial", 10)).grid(row=1, column=2, padx=5)
amount_entry = tk.Entry(bottom_frame, width=10)
amount_entry.grid(row=1, column=3, padx=5)

tk.Label(bottom_frame, text="Narration:", bg="lightpink", font=("Arial", 10)).grid(row=1, column=4, padx=5)
narration_entry = tk.Entry(bottom_frame, width=30)
narration_entry.grid(row=1, column=5, padx=5, columnspan=3)

# Treeview Frame for Displaying Items
tree_frame = tk.Frame(root, bg="lightpink")
tree_frame.pack(pady=10, fill="both", expand=True)

columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9", "#10", "#11", "#12", "#13", "#14", "#15")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)

tree.heading("#1", text="SLNo")
tree.heading("#2", text="Date")
tree.heading("#3", text="Name")
tree.heading("#4", text="Main Product")
tree.heading("#5", text="Design")
tree.heading("#6", text="Transaction")
tree.heading("#7", text="Gross")
tree.heading("#8", text="Stones")
tree.heading("#9", text="Touch")
tree.heading("#10", text="Net Wt")
tree.heading("#11", text="MC@")
tree.heading("#12", text="MC")
tree.heading("#13", text="Rate")
tree.heading("#14", text="Amount")
tree.heading("#15", text="Narration")


tree.column("#1", width=30, anchor=tk.CENTER)
tree.column("#2", width=50, anchor=tk.CENTER)
tree.column("#3", width=150, anchor=tk.W)
tree.column("#4", width=150, anchor=tk.W)
tree.column("#5", width=100, anchor=tk.W)
tree.column("#6", width=120, anchor=tk.W)
tree.column("#7", width=40, anchor=tk.CENTER)
tree.column("#8", width=40, anchor=tk.CENTER)
tree.column("#9", width=40, anchor=tk.CENTER)
tree.column("#10", width=80, anchor=tk.CENTER)
tree.column("#11", width=50, anchor=tk.CENTER)
tree.column("#12", width=40, anchor=tk.CENTER)
tree.column("#13", width=80, anchor=tk.CENTER)
tree.column("#14", width=100, anchor=tk.CENTER)
tree.column("#15", width=200, anchor=tk.W)

tree.pack(fill="both", expand=True)

# Footer Frame - Buttons
footer_frame = tk.Frame(root, bg="lightpink")
footer_frame.pack(pady=10)

tk.Button(footer_frame, text="Add", width=12, bg="green", fg="white", command=add_item).grid(row=0, column=0, padx=10)
tk.Button(footer_frame, text="Delete", width=12, bg="red", fg="white", command=delete_item).grid(row=0, column=1, padx=10)
tk.Button(footer_frame, text="Save", width=12, bg="blue", fg="white", command=save_items).grid(row=0, column=2, padx=10)

# Run the application
root.mainloop()
