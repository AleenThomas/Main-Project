import tkinter as tk
from tkinter import ttk
import requests

def convert_currency():
    try:
        amount = float(entry_amount.get())
        from_currency = entry_from_currency.get()
        to_currency = entry_to_currency.get()

        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url)
        data = response.json()
        exchange_rate = data['rates'][to_currency]
        result.set(f"{amount} {from_currency} = {round(amount * exchange_rate, 2)} {to_currency}")
    except ValueError:
        result.set("Invalid Input")

root = tk.Tk()
root.title("Currency Converter")

# Adding a custom style
style = ttk.Style()
style.configure('TButton', font=('calibri', 12, 'bold'), foreground='white', background='blue')
style.configure('TLabel', font=('calibri', 12))
style.configure('TEntry', font=('calibri', 12))

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0)

entry_amount = ttk.Entry(frame)
entry_from_currency = ttk.Entry(frame)
entry_to_currency = ttk.Entry(frame)
result = tk.StringVar()

convert_button = ttk.Button(frame, text="Convert", command=convert_currency, style='TButton')
result_label = ttk.Label(frame, textvariable=result, style='TLabel')

# Adding labels
ttk.Label(frame, text="Amount:", style='TLabel').grid(row=0, column=0, padx=5, pady=5)
ttk.Label(frame, text="From Currency:", style='TLabel').grid(row=1, column=0, padx=5, pady=5)
ttk.Label(frame, text="To Currency:", style='TLabel').grid(row=2, column=0, padx=5, pady=5)

entry_amount.grid(row=0, column=1, padx=5, pady=5)
entry_from_currency.grid(row=1, column=1, padx=5, pady=5)
entry_to_currency.grid(row=2, column=1, padx=5, pady=5)
convert_button.grid(row=3, column=1, padx=5, pady=5)
result_label.grid(row=4, column=1, padx=5, pady=5)

root.mainloop()
