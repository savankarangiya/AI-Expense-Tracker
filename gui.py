import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os
import matplotlib.pyplot as plt
import csv
from tkinter import messagebox
import pickle


DATA_FILE = "expenses.json"

all_expenses = []

# ================= WINDOW =================

root = tk.Tk()

with open("model.pkl", "rb") as file:
    model = pickle.load(file)

with open("vectorizer.pkl", "rb") as file:
    vectorizer = pickle.load(file)

root.title("AI Expense Tracker")

window_width = 1200
window_height = 750

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

center_x = int((screen_width / 2) - (window_width / 2))
center_y = int((screen_height / 2) - (window_height / 2)) - 40

root.geometry(
    f"{window_width}x{window_height}+{center_x}+{center_y}"
)

root.resizable(False, False)

# ================= COLORS =================

BG_COLOR = "#0F172A"

CARD_COLOR = "#1E293B"

ACCENT_COLOR = "#3B82F6"

TEXT_COLOR = "#F8FAFC"

BORDER_COLOR = "#334155"

BUTTON_TEXT = "#FFFFFF"

selected_item = None

root.configure(
    bg=BG_COLOR
)

# ================= HEADER =================

header_frame = tk.Frame(
    root,
    bg=BG_COLOR
)
header_frame.pack(fill="x", pady=10)

title_label = tk.Label(
    header_frame,
    text="💰 AI Expense Tracker",
    font=("Segoe UI", 24, "bold"),
    bg=BG_COLOR,
    fg=ACCENT_COLOR
)

title_label.pack()

# ================= INPUT FRAME =================

input_frame = tk.LabelFrame(
    root,
    text="Add Expense",
    padx=15,
    pady=15,
    bg=CARD_COLOR,
    fg=ACCENT_COLOR,
    font=("Segoe UI", 11, "bold")
)

input_frame.pack(
    fill="x",
    padx=20,
    pady=10
)

description_label = tk.Label(
    input_frame,
    text="Description",
    font=("Segoe UI", 11),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)

description_label.grid(
    row=0,
    column=0,
    padx=10,
    pady=10
)

description_entry = tk.Entry(
    input_frame,
    width=35,
    font=("Segoe UI", 11),
    bg="#FFFFFF",
    fg="black",
    insertbackground="black",
    relief="flat"
)

description_entry.grid(
    row=0,
    column=1,
    padx=10,
    pady=10
)

amount_label = tk.Label(
    input_frame,
    text="Amount",
    font=("Segoe UI", 11),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)

amount_label.grid(
    row=0,
    column=2,
    padx=10,
    pady=10
)

amount_entry = tk.Entry(
    input_frame,
    width=20,
    font=("Segoe UI", 11),
    bg="#FFFFFF",
    fg="black",
    insertbackground="black",
    relief="flat"
)

amount_entry.grid(
    row=0,
    column=3,
    padx=10,
    pady=10
)

category_label = tk.Label(
    input_frame,
    text="Category",
    font=("Segoe UI", 11),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)

category_label.grid(
    row=0,
    column=4,
    padx=10,
    pady=10
)

categories = [
    "Food",
    "Travel",
    "Health",
    "Shopping",
    "Education",
    "Entertainment",
    "Other"
]

category_var = tk.StringVar()

category_var.set(categories[0])

category_menu = ttk.Combobox(
    input_frame,
    textvariable=category_var,
    values=categories,
    width=20,
    state="readonly",
    cursor="hand2"
)

category_menu.grid(
    row=0,
    column=5,
    padx=10,
    pady=10
)

search_frame = tk.Frame(root)

search_frame.pack(
    fill="x",
    padx=20,
    pady=5
)

search_label = tk.Label(
    search_frame,
    text="Search Expense:",
    font=("Segoe UI", 11)
)

search_label.pack(
    side="left",
    padx=5
)

search_entry = tk.Entry(
    search_frame,
    width=40,
    font=("Segoe UI", 11)
)

search_entry.pack(
    side="left",
    padx=5
)




# ================= TABLE FRAME =================

table_frame = tk.LabelFrame(
    root,
    text="Expense Records"
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)

# ================= TABLE STYLE =================

style = ttk.Style()

style.theme_use("default")

style.configure(
    "Treeview",
    background="#1E1E1E",
    foreground="white",
    rowheight=30,
    fieldbackground="#1E1E1E",
    borderwidth=0,
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    background="#FF8C00",
    foreground="white",
    font=("Segoe UI", 11, "bold")
)

style.map(
    "Treeview",
    background=[
        ("selected", "#FF8C00")
    ]
)


expense_table = ttk.Treeview(
    table_frame,
    columns=(
        "Description",
        "Amount",
        "Category",
        "Date"
    ),
    show="headings",
    height=8
)

expense_table.tag_configure(
    "oddrow",
    background="#252525"
)

expense_table.tag_configure(
    "evenrow",
    background="#1E1E1E"
)

expense_table.heading(
    "Description",
    text="Description"
)

expense_table.heading(
    "Amount",
    text="Amount"
)

expense_table.heading(
    "Category",
    text="Category"
)

expense_table.heading(
    "Date",
    text="Date"
)

expense_table.column(
    "Description",
    width=500
)

expense_table.column(
    "Amount",
    width=150,
    anchor="center"
)

expense_table.column(
    "Category",
    width=250,
    anchor="center"
)

expense_table.column(
    "Date",
    width=150,
    anchor="center"
)

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=expense_table.yview
)

expense_table.configure(
    yscrollcommand=scrollbar.set
)

expense_table.pack(
    side="left",
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

scrollbar.pack(
    side="right",
    fill="y"
)


#================= FUNCTION ===================

def show_insights():

    category_totals = {}

    total_expense = 0

    for expense in all_expenses:

        category = expense["category"]

        amount = float(
            expense["amount"]
        )

        total_expense += amount

        if category in category_totals:

            category_totals[category] += amount

        else:

            category_totals[category] = amount

    if len(category_totals) == 0:

        messagebox.showinfo(
            "AI Insights",
            "No expense data available"
        )

        return

    highest_category = max(
        category_totals,
        key=category_totals.get
    )

    highest_amount = category_totals[
        highest_category
    ]

    percentage = (
        highest_amount
        / total_expense
    ) * 100

    message = (
        f"Total Expense: ₹{total_expense:.2f}\n\n"
        f"Highest Category: {highest_category}\n"
        f"Amount: ₹{highest_amount:.2f}\n\n"
        f"{highest_category} accounts for "
        f"{percentage:.1f}% of your spending."
    )

    messagebox.showinfo(
        "AI Insights",
        message
    )

def predict_category(event=None):

    description = description_entry.get().strip()

    if description == "":
        return

    text_vector = vectorizer.transform(
        [description]
    )

    prediction = model.predict(
        text_vector
    )[0]

    category_var.set(
        prediction
    )

def export_csv():

    with open(
        "expenses.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                "Description",
                "Amount",
                "Category",
                "Date"
            ]
        )

        for row in expense_table.get_children():

            writer.writerow(
                expense_table.item(
                    row,
                    "values"
                )
            )

    messagebox.showinfo(
    "Success",
    "CSV File Exported Successfully"
)

description_entry.bind(
    "<KeyRelease>",
    predict_category
)


def save_data():

    expenses = []

    for row in expense_table.get_children():

        values = expense_table.item(
            row,
            "values"
        )

        expenses.append({
            "description": values[0],
            "amount": values[1],
            "category": values[2],
            "date": values[3]
        })

    with open(
        DATA_FILE,
        "w"
    ) as file:

        json.dump(
            expenses,
            file,
            indent=4
        )

        global all_expenses

        all_expenses = expenses.copy()


def load_data():

    if not os.path.exists(DATA_FILE):
        return

    with open(
        DATA_FILE,
        "r"
    ) as file:

        expenses = json.load(file)

        global all_expenses

        all_expenses = expenses.copy()

    for expense in expenses:

        row_count = len(
            expense_table.get_children()
        )

        if row_count % 2 == 0:

            row_tag = "evenrow"

        else:

            row_tag = "oddrow"

        expense_table.insert(
            "",
            "end",
            values=(
                expense["description"],
                expense["amount"],
                expense["category"],
                expense["date"]
            ),
            tags=(row_tag,)
        )

    update_total()

def search_expense():

    keyword = search_entry.get().strip().lower()

    expense_table.delete(
        *expense_table.get_children()
    )

    for expense in all_expenses:

        if (
        keyword in expense["description"].lower()
        or
        keyword in expense["category"].lower()
        ):

            expense_table.insert(
                "",
                "end",
                values=(
                    expense["description"],
                    expense["amount"],
                    expense["category"],
                    expense["date"]
                )
            )


def show_graph():

    category_totals = {}

    for row in expense_table.get_children():

        values = expense_table.item(
            row,
            "values"
        )

        category = values[2]
        amount = float(values[1])

        if category in category_totals:

            category_totals[category] += amount

        else:

            category_totals[category] = amount

    plt.figure(
        figsize=(8, 4)
    )

    bars = plt.bar(
    category_totals.keys(),
    category_totals.values(),
    width=0.4
)

    for bar in bars:

        height = bar.get_height()

        plt.text(
            bar.get_x() + bar.get_width()/2,
            height,
            f"₹{height:.0f}",
            ha="center",
            va="bottom"
        )

    plt.title(
    "Expense Analysis By Category",
    fontsize=14,
    fontweight="bold"
)

    plt.xlabel(
        "Category"
    )

    plt.ylabel(
        "Amount"
    )

    plt.xticks(
    rotation=20
)

    plt.tight_layout()

    plt.show()


def update_total():

    total = 0

    for item in expense_table.get_children():

        values = expense_table.item(
            item,
            "values"
        )

        total += float(values[1])

    total_label.config(
        text=f"Total Expense : ₹{total:.2f}"
    )

def update_records():

    total_records = len(
        expense_table.get_children()
    )

    records_label.config(
        text=f"📄 Total Records : {total_records}"
    )

def add_expense():

    description = description_entry.get().strip().title()

    amount = amount_entry.get().strip()

    category = category_var.get()

    # Empty Validation
    if description == "":
        messagebox.showerror(
    "Error",
    "Description cannot be empty"
)   
        return

    if amount == "":
        messagebox.showerror(
    "Error",
    "Amount cannot be empty"
)
        return

    # Number Validation
    try:
        amount = float(amount)

    except ValueError:
        messagebox.showerror(
        "Error",
        "Amount must be a number"
        )
        return
    
    if amount <= 0:
        messagebox.showerror(
            "Error",
            "Amount must be greater than 0"
        )
        return

    current_date = datetime.now().strftime(
        "%d-%m-%Y"
    )

    expense_table.insert(
        "",
        "end",
        values=(
            description,
            amount,
            category,
            current_date
        )
    )

    messagebox.showinfo(
    "Success",
    "Expense Added Successfully"
)

    update_total()

    update_records()

    save_data()


    description_entry.delete(0, tk.END)

    amount_entry.delete(0, tk.END)

    category_var.set("Food")

    description_entry.focus()


def delete_expense():

    selected_item = expense_table.selection()

    if not selected_item:
        messagebox.showwarning(
    "Warning",
    "Please select an expense first"
)
        return


    if not messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this expense?"
    ):
        return

    
    expense_table.delete(
        selected_item[0]
    )

    messagebox.showinfo(
    "Success",
    "Expense Deleted Successfully"
)

    update_total()

    update_records()

    save_data()


def load_expense():

    global selected_item

    selected = expense_table.selection()

    if not selected:
        messagebox.showwarning(
        "Warning",
        "Please select an expense first"
        )
        return

    selected_item = selected[0]

    values = expense_table.item(
        selected_item,
        "values"
    )

    description_entry.delete(0, tk.END)

    amount_entry.delete(0, tk.END)

    description_entry.insert(
        0,
        values[0]
    )

    amount_entry.insert(
        0,
        values[1]
    )

    category_var.set(
        values[2]
    )

def update_expense():

    global selected_item

    if selected_item is None:

        messagebox.showwarning(
            "Warning",
            "Please load an expense first"
        )

        return

    description = description_entry.get().strip().title()

    amount = amount_entry.get().strip()

    category = category_var.get()

    if description == "":
        print("Description cannot be empty")
        return

    if amount == "":
        print("Amount cannot be empty")
        return

    try:
        amount = float(amount)

    except ValueError:
        print("Amount must be a number")
        return

    old_values = expense_table.item(
        selected_item,
        "values"
    )

    expense_table.item(
        selected_item,
        values=(
            description,
            amount,
            category,
            old_values[3]
        )
    )

    messagebox.showinfo(
    "Success",
    "Expense Updated Successfully"
)

    update_total()

    save_data()


    description_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

    category_var.set("Food")

    selected_item = None

    description_entry.focus()

def show_summary():

    category_totals = {}

    for expense in all_expenses:

        category = expense["category"]

        amount = float(
            expense["amount"]
        )

        if category in category_totals:

            category_totals[category] += amount

        else:

            category_totals[category] = amount

    print("\nCATEGORY SUMMARY\n")

    for category, total in category_totals.items():

        print(
            f"{category} : ₹{total:.2f}"
        )

def reset_search():

    search_entry.delete(
        0,
        tk.END
    )

    expense_table.delete(
        *expense_table.get_children()
    )

    load_data()

def animate_hover(widget, start, end, step=1):

    r1, g1, b1 = widget.winfo_rgb(start)
    r2, g2, b2 = widget.winfo_rgb(end)

    r = r1 + (r2 - r1) // 10
    g = g1 + (g2 - g1) // 10
    b = b1 + (b2 - b1) // 10

    color = f"#{r//256:02x}{g//256:02x}{b//256:02x}"

    widget.config(bg=color)


def premium_hover(
    button,
    hover_color,
    normal_color
):

    def enter(e):

        button.config(
            bg=hover_color,
            fg="white",
            relief="raised",
            bd=4,
            cursor="hand2"
        )

    def leave(e):

        button.config(
            bg=normal_color,
            fg="white",
            relief="flat",
            bd=0
        )

    button.bind("<Enter>", enter)
    button.bind("<Leave>", leave)


#================== BUTTON ========================

add_button = tk.Button(
    input_frame,
    text="➕ Add Expense",
    font=("Segoe UI", 11, "bold"),
    width=15,
    command=add_expense,
    bg=ACCENT_COLOR,
    fg="white",
    relief="flat",
    cursor="hand2"
)

add_button.grid(
    row=0,
    column=6,
    padx=15,
    pady=10
)

search_button = tk.Button(
    search_frame,
    text="Search",
    font=("Segoe UI", 10, "bold"),
    command=search_expense,
    cursor="hand2"
)

search_button.pack(
    side="left",
    padx=5
)

reset_button = tk.Button(
    search_frame,
    text="❌ Reset",
    font=("Segoe UI", 10, "bold"),
    command=reset_search
)

reset_button.pack(
    side="left",
    padx=5
)


# ================= STATS FRAME =================

stats_frame = tk.LabelFrame(
    root,
    text="Statistics",
    bg=CARD_COLOR,
    fg=ACCENT_COLOR,
    font=("Segoe UI", 11, "bold"),
    padx=10,
    pady=10
)

stats_frame.pack(
    fill="x",
    padx=20,
    pady=10
)

total_label = tk.Label(
    stats_frame,
    text="💰 Total Expense : ₹0.00",
    font=("Segoe UI", 14, "bold"),
    bg=CARD_COLOR,
    fg=ACCENT_COLOR
)

records_label = tk.Label(
    stats_frame,
    text="📄 Total Records : 0",
    font=("Segoe UI", 12, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)

records_label.pack(
    pady=5
)

total_label.pack(
    pady=3
)


# ================= ACTION FRAME =================

action_frame = tk.Frame(root)

action_frame.pack(
    fill="x",
    padx=20,
    pady=10
)

export_button = tk.Button(
    action_frame,
    text="📄 Export CSV",
    font=("Segoe UI", 11, "bold"),
    width=15,
    command=export_csv,
    bg=ACCENT_COLOR,
    fg="white",
    cursor="hand2",
    bd=0
)

font=("Segoe UI", 11, "bold"),
cursor="hand2",
bd=0,
relief="flat",
activeforeground="white",
premium_hover(
    add_button,
    "#10B981",
    ACCENT_COLOR
)


load_button = tk.Button(
    action_frame,
    text="📂 Load",
    font=("Segoe UI", 11, "bold"),
    width=15,
    command=load_expense,
    bg="#2196F3",
    fg="white",
    relief="flat",
    cursor="hand2",
)

load_button.pack(
    side="left",
    padx=10
)

update_button = tk.Button(
    action_frame,
    text="✏️ Update",
    font=("Segoe UI", 11, "bold"),
    width=18,
    bg="#FF9800",
    command=update_expense,
    cursor="hand2"
)

update_button.pack(
    side="left",
    padx=10
)

delete_button = tk.Button(
    action_frame,
    text="🗑 Delete",
    font=("Segoe UI", 11, "bold"),
    width=18,
    bg="#F44336",
    command=delete_expense,
    cursor="hand2"
)

delete_button.pack(
    side="left",
    padx=10
)

graph_button = tk.Button(
    action_frame,
    text="📊 Analytics",
    font=("Segoe UI", 11, "bold"),
    width=18,
    bg="#4CAF50",
    command=show_graph,
    cursor="hand2"
)

graph_button.pack(
    side="left",
    padx=10
)

insight_button = tk.Button(
    action_frame,
    text="🤖 AI Insights",
    font=("Segoe UI", 11, "bold"),
    width=15,
    command=show_insights,
    bg=ACCENT_COLOR,
    fg="white",
    cursor="hand2",
    bd=0
)

insight_button.pack(
    side="left",
    padx=10
)

premium_hover(
    add_button,
    "#10B981",
    ACCENT_COLOR
)

premium_hover(
    load_button,
    "#3B82F6",
    ACCENT_COLOR
)

premium_hover(
    update_button,
    "#6366F1",
    ACCENT_COLOR
)

premium_hover(
    delete_button,
    "#EF4444",
    ACCENT_COLOR
)

premium_hover(
    graph_button,
    "#8B5CF6",
    ACCENT_COLOR
)

premium_hover(
    export_button,
    "#F59E0B",
    ACCENT_COLOR
)

premium_hover(
    insight_button,
    "#06B6D4",
    ACCENT_COLOR
)

# ================= RUN =================

load_data()

update_records()

root.mainloop()