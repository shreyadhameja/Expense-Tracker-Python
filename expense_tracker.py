import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox, ttk
import os

# Initialize CSV
def initialize_csv():
    if not os.path.exists('expenses.csv'):
        df = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])
        df.to_csv('expenses.csv', index=False)

# Add new expense
def add_expense():
    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()
    description = desc_entry.get()

    if not date or not category or not amount:
        messagebox.showerror("Missing Data", "Please fill all fields.")
        return

    try:
        datetime.strptime(date, "%Y-%m-%d")
        amount = float(amount)
    except:
        messagebox.showerror("Invalid Input", "Date format: YYYY-MM-DD. Amount: Numeric.")
        return

    df = pd.read_csv('expenses.csv')
    new_expense = pd.DataFrame([[date, category, amount, description]],
                               columns=['Date', 'Category', 'Amount', 'Description'])
    df = pd.concat([df, new_expense], ignore_index=True)
    df.to_csv('expenses.csv', index=False)

    messagebox.showinfo("Success", "Expense added.")
    clear_entries()

# View all expenses
def view_expenses():
    df = pd.read_csv('expenses.csv')
    text.delete(1.0, tk.END)
    if df.empty:
        text.insert(tk.END, "No expenses recorded.")
    else:
        text.insert(tk.END, df.to_string(index=False))

# Clear input fields
def clear_entries():
    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)

# Show Pie Chart
def pie_chart():
    df = pd.read_csv('expenses.csv')
    if df.empty:
        messagebox.showinfo("No Data", "No expenses to visualize.")
        return

    category_sum = df.groupby('Category')['Amount'].sum()

    fig, ax = plt.subplots()
    category_sum.plot.pie(autopct='%1.1f%%', ax=ax)
    ax.set_ylabel('')
    ax.set_title('Expenses by Category')

    show_plot(fig)

# Show Line Chart
def line_chart():
    df = pd.read_csv('expenses.csv')
    if df.empty:
        messagebox.showinfo("No Data", "No expenses to visualize.")
        return

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df.dropna(subset=['Date'], inplace=True)

    daily_total = df.groupby('Date')['Amount'].sum()

    fig, ax = plt.subplots()
    daily_total.plot(marker='o', ax=ax)
    ax.set_title('Daily Expense Trend')
    ax.set_xlabel('Date')
    ax.set_ylabel('Amount')
    plt.xticks(rotation=45)
    plt.tight_layout()

    show_plot(fig)

# Show Bar Chart
def bar_chart():
    df = pd.read_csv('expenses.csv')
    if df.empty:
        messagebox.showinfo("No Data", "No expenses to visualize.")
        return

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df.dropna(subset=['Date'], inplace=True)
    df['Month'] = df['Date'].dt.to_period('M')

    month_total = df.groupby('Month')['Amount'].sum()

    fig, ax = plt.subplots()
    month_total.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title('Monthly Expenses')
    ax.set_xlabel('Month')
    ax.set_ylabel('Amount')
    plt.tight_layout()

    show_plot(fig)

# Embed matplotlib figure inside a new Tkinter window
def show_plot(fig):
    win = tk.Toplevel(root)
    win.title("Chart")
    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.draw()
    canvas.get_tk_widget().pack()
    toolbar = ttk.Frame(win)
    toolbar.pack()
    plt.close(fig)

# Initialize GUI window
initialize_csv()
root = tk.Tk()
root.title("📊 Expense Tracker GUI")
root.geometry("650x700")
root.resizable(False, False)

# Labels and Entries
tk.Label(root, text="Date (YYYY-MM-DD):").place(x=20, y=20)
date_entry = tk.Entry(root, width=20)
date_entry.place(x=170, y=20)

tk.Label(root, text="Category:").place(x=20, y=60)
category_entry = tk.Entry(root, width=20)
category_entry.place(x=170, y=60)

tk.Label(root, text="Amount:").place(x=20, y=100)
amount_entry = tk.Entry(root, width=20)
amount_entry.place(x=170, y=100)

tk.Label(root, text="Description:").place(x=20, y=140)
desc_entry = tk.Entry(root, width=40)
desc_entry.place(x=170, y=140)

# Buttons
tk.Button(root, text="Add Expense", command=add_expense, width=20, bg="#4CAF50", fg="white").place(x=400, y=20)
tk.Button(root, text="View All Expenses", command=view_expenses, width=20, bg="#2196F3", fg="white").place(x=400, y=60)
tk.Button(root, text="Pie Chart (Categories)", command=pie_chart, width=20, bg="#FF9800", fg="white").place(x=400, y=100)
tk.Button(root, text="Line Chart (Over Time)", command=line_chart, width=20, bg="#9C27B0", fg="white").place(x=400, y=140)
tk.Button(root, text="Bar Chart (Monthly)", command=bar_chart, width=20, bg="#F44336", fg="white").place(x=400, y=180)

# Text area to display expenses
text = tk.Text(root, height=20, width=80)
text.place(x=20, y=230)

root.mainloop()
