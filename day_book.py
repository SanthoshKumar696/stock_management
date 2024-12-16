import tkinter as tk
from tkinter import ttk, messagebox

def day_book(root):   #### day book page start
     # Create a new window for Day Book
    day_book_window = tk.Toplevel()
    day_book_window.title("Day Book")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    day_book_window.geometry(f"{screen_width}x{screen_height}")
    day_book_window.configure(bg="lightblue")

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
        command=lambda: print(f"Report generated for {from_date_entry.get()} to {to_date_entry.get()}")
    ).grid(row=0, column=0, padx=10)

    # Cancel Button
    tk.Button(
        button_frame,
        text="Cancel",
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
### day book page ended