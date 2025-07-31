import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext, Toplevel, Checkbutton, IntVar
import pyttsx3
import difflib
import random

# Voice engine setup
engine = pyttsx3.init()

def speak(text):
    output.insert(tk.END, f"🤖 Champak: {text}\n")
    engine.say(text)
    engine.runAndWait()

# Menus
veg_menu = {
    "Veg Biryani": 120, "Masala Dosa": 80, "Veg Cheese Pizza": 180,
    "Gulab Jamun": 50, "Salad Bowl": 60, "Dal Makhani": 120,    
    "Chole Bhature": 150, "Aloo Gobi": 130, "Vegetable Biryani": 170,
    "Rajma": 140, "Methi Thepla": 80, "Pulao": 90,
    "Tandoori Roti": 30, "Garlic Naan": 40, "Gulab Jamun (Dessert)": 50
}
paneer_dishes = {
    "Paneer Butter Masala": 150, "Paneer Tikka": 180, "Paneer Bhurji": 330,
    "Paneer Lababdar": 190, "Paneer Do Pyaza": 170, "Kadai Paneer": 175, "Chilli Paneer": 170
}
chef_special_pool = {
    "Paneer Tikka Wrap": 140, "Veg Spring Roll": 120, "Cheese Burst Dosa": 150,
    "Mexican Salad": 130, "Veg Seekh Kebab": 160, "Stuffed Paratha": 100,
    "Schezwan Noodles": 140, "Tandoori Platter": 200, "Crispy Corn": 110,
    "Hakka Noodles": 140
}
chef_special_today = dict(random.sample(list(chef_special_pool.items()), random.randint(5, 7)))
full_menu = {**veg_menu, **paneer_dishes, **chef_special_today}
order = {}

# UI setup
root = tk.Tk()
root.title("Champak's AI Veg Restaurant")
root.geometry("700x700")

output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=85, height=30)
output.pack(pady=10)

def find_matches(user_input):
    matches = [item for item in full_menu if user_input.lower() in item.lower()]
    return matches if matches else difflib.get_close_matches(user_input, full_menu.keys(), n=5, cutoff=0.5)

def show_checkbox_selection(dish_options):
    selected_dish = []

    def submit_selection():
        for i, var in enumerate(var_list):
            if var.get() == 1:
                selected_dish.append(dish_options[i])
        top.destroy()

    top = Toplevel(root)
    top.title("Select Dish Variety")
    var_list = []

    for dish in dish_options:
        var = IntVar()
        chk = Checkbutton(top, text=f"{dish} - ₹{full_menu[dish]}", variable=var)
        chk.pack(anchor='w')
        var_list.append(var)

    tk.Button(top, text="Confirm", command=submit_selection).pack(pady=5)
    top.wait_window()
    return selected_dish[0] if selected_dish else None

def start_bot():
    speak("Welcome to Champak's AI Veg Restaurant!")
    output.insert(tk.END, "\n🌟 Today's Chef Specials (25% off) 🌟\n")
    for item, price in chef_special_today.items():
        output.insert(tk.END, f"{item:<35} ₹{price}\n")
    speak("Today's Chef Specials are " + ", ".join(chef_special_today.keys()))

    name = simpledialog.askstring("Name", "What's your name?")
    table = simpledialog.askstring("Table", "Enter your table number:")
    speak(f"Hello {name}, here's our menu.")

    output.insert(tk.END, f"\n📋 Full Menu:\n")
    for item, price in full_menu.items():
        output.insert(tk.END, f"{item:<35} ₹{price}\n")

    while True:
        dish_input = simpledialog.askstring("Order", "Enter dish name (or 'done' to finish):")
        if not dish_input:
            continue
        if dish_input.lower() == 'done':
            break

        matches = find_matches(dish_input)
        if matches:
            if len(matches) > 1:
                speak("Multiple varieties found. Please choose one.")
                dish = show_checkbox_selection(matches)
            else:
                dish = matches[0]
        else:
            speak("Dish not found.")
            continue

        qty = simpledialog.askstring("Quantity", f"How many plates of {dish}?")
        try:
            qty = int(qty)
            if qty > 0:
                order[dish] = order.get(dish, 0) + qty
            else:
                speak("Quantity must be positive.")
        except:
            speak("Invalid quantity.")

    show_bill(name, table)

def show_bill(name, table):
    speak("Preparing your bill.")
    output.insert(tk.END, "\n🧾 -------- Bill Summary --------\n")
    output.insert(tk.END, f"Customer Name: {name}\nTable Number: {table}\n\n")

    header = f"{'Dish Name':<35} {'Qty':>5} {'Price':>8} {'Subtotal':>10} {'Discount':>10} {'Total':>10}\n"
    output.insert(tk.END, header)
    output.insert(tk.END, "-" * 90 + "\n")

    grand_total = 0
    total_discount = 0

    for dish, qty in order.items():
        price = full_menu[dish]
        subtotal = qty * price
        discount = subtotal * 0.25 if dish in chef_special_today else 0
        total = subtotal - discount
        grand_total += total
        total_discount += discount
        line = f"{dish:<35} {qty:>5} ₹{price:>7} ₹{subtotal:>9} -₹{int(discount):>8} ₹{int(total):>9}\n"
        output.insert(tk.END, line)

    output.insert(tk.END, "-" * 90 + "\n")
    output.insert(tk.END, f"{'Total Discount':>70} : -₹{int(total_discount)}\n")
    output.insert(tk.END, f"{'Grand Total':>70} : ₹{int(grand_total)}\n")

    speak(f"Your total bill is {int(grand_total)} rupees after discount.")
    speak("Your order is being prepared.")
    output.insert(tk.END, "\n⏳ Cooking...\n✅ Your order is ready! Enjoy your meal!\n")
    speak("Your order is ready. Enjoy your meal!")

    ask_feedback()

def ask_feedback():
    choice = messagebox.askyesno("Feedback", "Would you like to give feedback?")
    if choice:
        rating = simpledialog.askstring("Rating", "Rate us out of 5:")
        comment = simpledialog.askstring("Comments", "Any comments?")
        output.insert(tk.END, f"\n⭐ Rating: {rating}/5\n💬 Comment: {comment}\n")
        speak("Thank you for your feedback.")
    else:
        speak("Thank you for visiting.")

    output.insert(tk.END, "\n🙏 Thank you for visiting Champak's AI Veg Restaurant!\n")
    speak("Thank you for visiting Champak's AI Veg Restaurant. Have a great day!")

start_bot()
root.mainloop()

