import requests
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk


def get_exchange_rate(f):
    data = requests.get(f"https://api.exchangerate-api.com/v4/latest/{f}").json()
    return data['rates']


def convert_currency():
    try:
        a, f = float(amount_entry.get()), from_currency_var.get()
        to_currencies = [currencies[idx] for idx in to_currency_listbox.curselection()]
        if not f or not to_currencies:
            result_label.config(text="⚠ Please select currencies!", font=("Arial", 18, "bold"), fg="red")
            return

        rates = get_exchange_rate(f)
        result_text = f"✅ {a} {f} converts to:\n"
        for t in to_currencies:
            r = rates.get(t)
            if r:
                result_text += f"{round(a * r, 2)} {t}\n"
            else:
                result_text += f"⚠ Error fetching rate for {t}\n"

        result_label.config(text=result_text, font=("Arial", 18, "bold"), fg="green")
    except ValueError:
        result_label.config(text="⚠ Please enter a valid number!", font=("Arial", 18, "bold"), fg="red")


def toggle_theme():
    global is_dark_mode
    is_dark_mode = not is_dark_mode

    # Change colors for dark mode or light mode
    if is_dark_mode:
        frame.config(bg="#2E2E2E")
        bg_label.config(bg="#2E2E2E")
        result_label.config(bg="#2E2E2E", fg="white")
        amount_entry.config(bg="#555555", fg="white")
        from_currency_dropdown.config(bg="#555555", fg="white")
        to_currency_listbox.config(bg="#555555", fg="white")
        convert_button.config(bg="#444444", fg="white")
        exit_button.config(bg="#444444", fg="white")
        theme_button.config(bg="#444444", fg="white")
    else:
        frame.config(bg="#f0f0f0")
        bg_label.config(bg="#f0f0f0")
        result_label.config(bg="#f0f0f0", fg="black")
        amount_entry.config(bg="white", fg="black")
        from_currency_dropdown.config(bg="white", fg="black")
        to_currency_listbox.config(bg="white", fg="black")
        convert_button.config(bg="#007BFF", fg="white")
        exit_button.config(bg="red", fg="white")
        theme_button.config(bg="#007BFF", fg="white")


root = tk.Tk()
root.title("💰 Currency Converter 💰")
root.attributes('-fullscreen', True)

# Load and set background image
bg_image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT7yKr15ziTWHr8x93NF43O3CPFvioenaVZLA&s"
bg_image = Image.open(requests.get(bg_image_url, stream=True).raw)
bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

frame = tk.Frame(root, bg="#f0f0f0", bd=8, relief=tk.RIDGE)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

tk.Label(frame, text="Currency Converter", font=("Arial", 28, "bold"), bg="#f0f0f0").pack(pady=20)

tk.Label(frame, text="Enter Amount:", font=("Arial", 20, "bold"), bg="#f0f0f0").pack()
amount_entry = tk.Entry(frame, font=("Arial", 20), width=20, justify="center")
amount_entry.pack(pady=10)

tk.Label(frame, text="From Currency:", font=("Arial", 20, "bold"), bg="#f0f0f0").pack()
from_currency_var = tk.StringVar()
currencies = ["USD", "EUR", "CNY", "JPY", "GBP", "INR"]
from_currency_dropdown = ttk.Combobox(frame, textvariable=from_currency_var, values=currencies, font=("Arial", 18),
                                      state="readonly", width=18)
from_currency_dropdown.pack(pady=10)

tk.Label(frame, text="Select Currencies to Convert Into (You can choose multiple options for conversion):",
         font=("Arial", 20, "bold"), bg="#f0f0f0").pack()
to_currency_listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, font=("Arial", 18), height=5, width=25)
for currency in currencies:
    to_currency_listbox.insert(tk.END, currency)
to_currency_listbox.pack(pady=10)

convert_button = tk.Button(frame, text="Convert", command=convert_currency, font=("Arial", 20, "bold"), bg="#007BFF",
                           fg="white",
                           width=18)
convert_button.pack(pady=20)

result_label = tk.Label(frame, text="Result will be shown here", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="black")
result_label.pack(pady=20)

exit_button = tk.Button(root, text="Exit", command=root.quit, font=("Arial", 18, "bold"), bg="red", fg="white",
                        width=12)
exit_button.pack(pady=20)

# Toggle theme button in top-right corner with smaller size
theme_button = tk.Button(root, text="🌙", command=toggle_theme, font=("Arial", 14, "bold"), bg="#007BFF", fg="white",
                         width=4, height=1)
theme_button.place(x=root.winfo_screenwidth() - 80, y=10)

# Initialize dark mode as False (Light mode)
is_dark_mode = False

root.mainloop()