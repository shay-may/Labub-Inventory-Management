import tkinter as tk
from tkinter import ttk, messagebox

inventory = {}

PASTEL_PINK = "#FCE7F3"
PASTEL_YELLOW = "#FEF9C3"
PASTEL_SKY = "#DDEBFF"
CARD_BG = "#FFFFFF"
BORDER = "#E6E6E6"
TEXT = "#1F2937"


def normalize_name(s):
    return s.strip()


def safe_float(s):
    s = s.strip()
    if s == "":
        raise ValueError("Price is required.")
    val = float(s)
    if val < 0:
        raise ValueError("Price must be non-negative.")
    return val


def safe_int(s):
    s = s.strip()
    if not s.isdigit():
        raise ValueError("Quantity must be a whole number (0 or more).")
    return int(s)


def safe_generation(s):
    g = s.strip()
    if g == "":
        raise ValueError("Generation is required.")
    return g


def safe_text(s, field_name):
    v = s.strip()
    if v == "":
        raise ValueError(field_name + " is required.")
    return v


def upsert_item(name, series, generation, color, price, quantity, special):
    inventory[name] = {
        "series": series,
        "generation": generation,
        "color": color,
        "price": price,
        "quantity": quantity,
        "special": special
    }


def refresh_table():
    for row in tree.get_children():
        tree.delete(row)

    rows = []
    for name, item in inventory.items():
        rows.append((
            name,
            item["series"],
            item["generation"],
            item["color"],
            f"{item['price']:.2f}",
            str(item["quantity"]),
            "Yes" if item["special"] else "No"
        ))

    sort_key = sort_var.get()
    if sort_key == "Name":
        rows.sort(key=lambda r: r[0].lower())
    elif sort_key == "Series":
        rows.sort(key=lambda r: r[1].lower())
    elif sort_key == "Generation":
        rows.sort(key=lambda r: r[2].lower())
    elif sort_key == "Color":
        rows.sort(key=lambda r: r[3].lower())
    elif sort_key == "Price":
        rows.sort(key=lambda r: float(r[4]))
    elif sort_key == "Quantity":
        rows.sort(key=lambda r: int(r[5]))
    elif sort_key == "Special":
        rows.sort(key=lambda r: r[6])

    query = filter_var.get().strip().lower()
    if query:
        filtered = []
        for r in rows:
            hay = " ".join(r).lower()
            if query in hay:
                filtered.append(r)
        rows = filtered

    only_special = special_only_var.get()
    if only_special:
        rows = [r for r in rows if r[6] == "Yes"]

    for r in rows:
        tree.insert("", "end", values=r)

    update_status()


def update_status():
    total_items = len(inventory)
    total_qty = sum(item["quantity"] for item in inventory.values()) if inventory else 0
    special_count = sum(1 for item in inventory.values() if item["special"]) if inventory else 0
    status_label.config(text=f"Items: {total_items}   Total quantity: {total_qty}   Special: {special_count}")


def clear_form():
    name_var.set("")
    series_var.set("")
    generation_var.set("")
    color_var.set("")
    price_var.set("")
    qty_var.set("")
    special_var.set(False)


def load_selected_into_form():
    sel = tree.selection()
    if not sel:
        messagebox.showinfo("Select an item", "Click a row in the table first.")
        return

    vals = tree.item(sel[0], "values")
    name_var.set(vals[0])
    series_var.set(vals[1])
    generation_var.set(vals[2])
    color_var.set(vals[3])
    price_var.set(vals[4])
    qty_var.set(vals[5])
    special_var.set(vals[6] == "Yes")


def add_item():
    try:
        name = safe_text(name_var.get(), "Name")
        name = normalize_name(name)

        if name in inventory:
            messagebox.showerror("Already exists", "That Labubu name already exists. Use Update.")
            return

        series = safe_text(series_var.get(), "Series")
        generation = safe_generation(generation_var.get())
        color = safe_text(color_var.get(), "Color")
        price = safe_float(price_var.get())
        quantity = safe_int(qty_var.get())
        special = bool(special_var.get())

        upsert_item(name, series, generation, color, price, quantity, special)
        refresh_table()
        clear_form()
        messagebox.showinfo("Added", "Labubu added successfully.")
    except Exception as e:
        messagebox.showerror("Input error", str(e))


def update_item():
    try:
        name = safe_text(name_var.get(), "Name")
        name = normalize_name(name)

        if name not in inventory:
            messagebox.showerror("Not found", "That Labubu name does not exist. Use Add.")
            return

        series = safe_text(series_var.get(), "Series")
        generation = safe_generation(generation_var.get())
        color = safe_text(color_var.get(), "Color")
        price = safe_float(price_var.get())
        quantity = safe_int(qty_var.get())
        special = bool(special_var.get())

        upsert_item(name, series, generation, color, price, quantity, special)
        refresh_table()
        messagebox.showinfo("Updated", "Labubu updated successfully.")
    except Exception as e:
        messagebox.showerror("Input error", str(e))


def remove_item():
    sel = tree.selection()
    if not sel:
        messagebox.showinfo("Select an item", "Click a row in the table first.")
        return

    vals = tree.item(sel[0], "values")
    name = vals[0]

    if messagebox.askyesno("Remove item", f"Remove '{name}' from inventory?"):
        if name in inventory:
            del inventory[name]
        refresh_table()
        clear_form()


def check_low_stock():
    if not inventory:
        messagebox.showinfo("Low stock", "Inventory is empty.")
        return

    s = threshold_var.get().strip()
    if not s.isdigit():
        messagebox.showerror("Input error", "Threshold must be a whole number.")
        return
    threshold = int(s)

    low = []
    for name, item in inventory.items():
        if item["quantity"] < threshold:
            low.append(f"{name} (qty: {item['quantity']})")

    if not low:
        messagebox.showinfo("Low stock", f"No Labubus below {threshold}.")
        return

    messagebox.showinfo("Low stock", "Below threshold:\n\n" + "\n".join(low))


def on_filter_change(*args):
    refresh_table()


def on_sort_change(*args):
    refresh_table()


root = tk.Tk()
root.title("Labubu Inventory")
root.geometry("1100x680")
root.configure(bg=PASTEL_PINK)

style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview",
                background="white",
                fieldbackground="white",
                foreground=TEXT,
                rowheight=28,
                bordercolor=BORDER,
                lightcolor=BORDER,
                darkcolor=BORDER)

style.configure("Treeview.Heading",
                background=PASTEL_SKY,
                foreground=TEXT,
                relief="flat",
                font=("Segoe UI", 10, "bold"))

style.map("Treeview",
          background=[("selected", PASTEL_YELLOW)],
          foreground=[("selected", TEXT)])

style.configure("TCombobox", fieldbackground="white", background="white")
style.configure("TCheckbutton", background=CARD_BG, foreground=TEXT)

outer = tk.Frame(root, bg=PASTEL_PINK)
outer.pack(fill="both", expand=True, padx=18, pady=18)

left_card = tk.Frame(outer, bg=CARD_BG, highlightthickness=1, highlightbackground=BORDER)
left_card.pack(side="left", fill="y", padx=(0, 14))

right_card = tk.Frame(outer, bg=CARD_BG, highlightthickness=1, highlightbackground=BORDER)
right_card.pack(side="right", fill="both", expand=True)

title = tk.Label(left_card, text="Labubu Inventory", bg=CARD_BG, fg=TEXT, font=("Segoe UI", 18, "bold"))
title.pack(anchor="w", padx=16, pady=(14, 2))

subtitle = tk.Label(left_card, text="Add, update, filter, and check stock",
                    bg=CARD_BG, fg=TEXT, font=("Segoe UI", 10))
subtitle.pack(anchor="w", padx=16, pady=(0, 10))

form = tk.Frame(left_card, bg=CARD_BG)
form.pack(fill="x", padx=16)

def make_label(txt, r):
    tk.Label(form, text=txt, bg=CARD_BG, fg=TEXT, font=("Segoe UI", 10)).grid(row=r, column=0, sticky="w", pady=6)

def make_entry(var, r):
    e = tk.Entry(form, textvariable=var, bd=0, relief="flat",
                 highlightthickness=1, highlightbackground=BORDER, highlightcolor=BORDER,
                 font=("Segoe UI", 11), fg=TEXT, bg="white", insertbackground=TEXT, width=22)
    e.grid(row=r, column=1, sticky="w", pady=6, padx=(10, 0))
    return e

name_var = tk.StringVar()
series_var = tk.StringVar()
generation_var = tk.StringVar()
color_var = tk.StringVar()
price_var = tk.StringVar()
qty_var = tk.StringVar()
special_var = tk.BooleanVar(value=False)

make_label("Name", 0); make_entry(name_var, 0)
make_label("Series", 1); make_entry(series_var, 1)
make_label("Generation", 2); make_entry(generation_var, 2)
make_label("Color", 3); make_entry(color_var, 3)
make_label("Price", 4); make_entry(price_var, 4)
make_label("Quantity", 5); make_entry(qty_var, 5)

tk.Label(form, text="Special", bg=CARD_BG, fg=TEXT, font=("Segoe UI", 10)).grid(row=6, column=0, sticky="w", pady=6)
special_chk = ttk.Checkbutton(form, text="Yes, special edition", variable=special_var)
special_chk.grid(row=6, column=1, sticky="w", pady=6, padx=(10, 0))

buttons = tk.Frame(left_card, bg=CARD_BG)
buttons.pack(fill="x", padx=16, pady=(12, 6))

def pastel_button(parent, text, bg, command):
    return tk.Button(parent, text=text, command=command,
                     bg=bg, fg=TEXT, activebackground=bg, activeforeground=TEXT,
                     bd=0, highlightthickness=1, highlightbackground=BORDER,
                     font=("Segoe UI", 10, "bold"), padx=12, pady=10, cursor="hand2")

btn_add = pastel_button(buttons, "Add", PASTEL_YELLOW, add_item)
btn_add.grid(row=0, column=0, sticky="ew", padx=(0, 8))
btn_update = pastel_button(buttons, "Update", PASTEL_SKY, update_item)
btn_update.grid(row=0, column=1, sticky="ew", padx=(0, 8))
btn_remove = pastel_button(buttons, "Remove", "#FFE4E6", remove_item)
btn_remove.grid(row=0, column=2, sticky="ew")

buttons.grid_columnconfigure(0, weight=1)
buttons.grid_columnconfigure(1, weight=1)
buttons.grid_columnconfigure(2, weight=1)

more = tk.Frame(left_card, bg=CARD_BG)
more.pack(fill="x", padx=16, pady=(4, 12))

btn_load = pastel_button(more, "Load selected into form", PASTEL_PINK, load_selected_into_form)
btn_load.pack(fill="x", pady=(0, 8))

btn_clear = pastel_button(more, "Clear form", "#F3F4F6", clear_form)
btn_clear.pack(fill="x")

divider = tk.Frame(left_card, bg=BORDER, height=1)
divider.pack(fill="x", padx=16, pady=10)

tools = tk.Frame(left_card, bg=CARD_BG)
tools.pack(fill="x", padx=16, pady=(0, 12))

tk.Label(tools, text="Low stock threshold", bg=CARD_BG, fg=TEXT, font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", pady=6)
threshold_var = tk.StringVar(value="3")
threshold_entry = tk.Entry(tools, textvariable=threshold_var, bd=0, relief="flat",
                           highlightthickness=1, highlightbackground=BORDER, highlightcolor=BORDER,
                           font=("Segoe UI", 11), fg=TEXT, bg="white", insertbackground=TEXT, width=10)
threshold_entry.grid(row=0, column=1, sticky="w", padx=(10, 0), pady=6)

btn_low = pastel_button(tools, "Check low stock", PASTEL_YELLOW, check_low_stock)
btn_low.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))

tools.grid_columnconfigure(0, weight=1)

topbar = tk.Frame(right_card, bg=CARD_BG)
topbar.pack(fill="x", padx=12, pady=12)

tk.Label(topbar, text="Inventory Table", bg=CARD_BG, fg=TEXT, font=("Segoe UI", 14, "bold")).pack(side="left")

filter_var = tk.StringVar()
filter_var.trace_add("write", on_filter_change)

special_only_var = tk.BooleanVar(value=False)
special_only_var.trace_add("write", on_filter_change)

sort_var = tk.StringVar(value="Name")
sort_var.trace_add("write", on_sort_change)

controls = tk.Frame(right_card, bg=CARD_BG)
controls.pack(fill="x", padx=12)

tk.Label(controls, text="Filter", bg=CARD_BG, fg=TEXT, font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", padx=(0, 6))
filter_entry = tk.Entry(controls, textvariable=filter_var, bd=0, relief="flat",
                        highlightthickness=1, highlightbackground=BORDER, highlightcolor=BORDER,
                        font=("Segoe UI", 11), fg=TEXT, bg="white", insertbackground=TEXT, width=28)
filter_entry.grid(row=0, column=1, sticky="w", padx=(0, 12))

special_only_chk = ttk.Checkbutton(controls, text="Special only", variable=special_only_var)
special_only_chk.grid(row=0, column=2, sticky="w", padx=(0, 12))

tk.Label(controls, text="Sort by", bg=CARD_BG, fg=TEXT, font=("Segoe UI", 10)).grid(row=0, column=3, sticky="w", padx=(0, 6))
sort_box = ttk.Combobox(controls, textvariable=sort_var, state="readonly",
                        values=["Name", "Series", "Generation", "Color", "Price", "Quantity", "Special"], width=14)
sort_box.grid(row=0, column=4, sticky="w")

controls.grid_columnconfigure(5, weight=1)

table_frame = tk.Frame(right_card, bg=CARD_BG)
table_frame.pack(fill="both", expand=True, padx=12, pady=12)

columns = ("Name", "Series", "Generation", "Color", "Price", "Quantity", "Special")
tree = ttk.Treeview(table_frame, columns=columns, show="headings")
tree.pack(side="left", fill="both", expand=True)

for col in columns:
    tree.heading(col, text=col)

tree.column("Name", width=160, anchor="w")
tree.column("Series", width=160, anchor="w")
tree.column("Generation", width=110, anchor="w")
tree.column("Color", width=120, anchor="w")
tree.column("Price", width=90, anchor="e")
tree.column("Quantity", width=90, anchor="e")
tree.column("Special", width=90, anchor="center")

scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
scroll.pack(side="right", fill="y")
tree.configure(yscrollcommand=scroll.set)

status_label = tk.Label(right_card, text="", bg=CARD_BG, fg=TEXT, font=("Segoe UI", 10))
status_label.pack(fill="x", padx=12, pady=(0, 12))

refresh_table()
root.mainloop()
