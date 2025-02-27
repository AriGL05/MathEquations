import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

# 🧮 Safely evaluate user equations
def safe_eval(expr, x, y=0):
    try:
        return eval(expr, {"__builtins__": {}}, {"x": x, "y": y, "np": np})
    except Exception as e:
        messagebox.showerror("Error", f"Invalid equation: {e}")
        return None

# ✅ Euler's Method
def euler_method(equation, x0, y0, xn, h):
    x, y = x0, y0
    results = [(x, y)]
    while x < xn:
        y += h * safe_eval(equation, x, y)
        x += h
        results.append((x, y))
    return results

# ✅ Improved Euler (Heun Method)
def improved_euler(equation, x0, y0, xn, h):
    x, y = x0, y0
    results = [(x, y)]
    while x < xn:
        fxy = safe_eval(equation, x, y)
        y_predict = y + h * fxy
        y += h / 2 * (fxy + safe_eval(equation, x + h, y_predict))
        x += h
        results.append((x, y))
    return results

# ✅ Runge-Kutta (4th Order)
def runge_kutta(equation, x0, y0, xn, h):
    x, y = x0, y0
    results = [(x, y)]
    while x < xn:
        k1 = h * safe_eval(equation, x, y)
        k2 = h * safe_eval(equation, x + h / 2, y + k1 / 2)
        k3 = h * safe_eval(equation, x + h / 2, y + k2 / 2)
        k4 = h * safe_eval(equation, x + h, y + k3)
        y += (k1 + 2 * k2 + 2 * k3 + k4) / 6
        x += h
        results.append((x, y))
    return results

# ✅ Newton-Raphson Method
def newton_raphson(equation, derivative, x0, tol=1e-6, max_iter=100):
    x = x0
    results = [(0, x)]
    for i in range(1, max_iter + 1):
        f = safe_eval(equation, x)
        df = safe_eval(derivative, x)
        if df == 0:
            messagebox.showerror("Error", "Derivative is zero, cannot continue!")
            return results
        x_new = x - f / df
        results.append((i, x_new))
        if abs(x_new - x) < tol:
            break
        x = x_new
    return results

# 📊 Display results in a table
def display_table(results, title):
    for widget in table_frame.winfo_children():
        widget.destroy()

    ttk.Label(table_frame, text=title, font=("Arial", 12, "bold")).pack(pady=5)

    table = ttk.Treeview(table_frame, columns=("Step", "Value"), show="headings")
    table.heading("Step", text="Step")
    table.heading("Value", text="Value (x, y)")
    table.pack()

    for i, (x, y) in enumerate(results):
        table.insert("", "end", values=(i + 1, f"({x:.6f}, {y:.6f})"))

# 📊 Main function to handle method execution
def run_method(method):
    try:
        equation = eq_entry.get()
        derivative = deriv_entry.get()

        # Initial values
        x0 = float(x0_entry.get())
        y0 = float(y0_entry.get())
        xn = float(xn_entry.get())
        h = float(h_entry.get())

        if method == "Euler":
            results = euler_method(equation, x0, y0, xn, h)
            display_table(results, "Euler Method")

        elif method == "Improved Euler":
            results = improved_euler(equation, x0, y0, xn, h)
            display_table(results, "Improved Euler Method")

        elif method == "Runge-Kutta":
            results = runge_kutta(equation, x0, y0, xn, h)
            display_table(results, "Runge-Kutta (4th Order)")

        elif method == "Newton-Raphson":
            if not derivative:
                messagebox.showerror("Error", "Derivative is required for Newton-Raphson!")
                return
            results = newton_raphson(equation, derivative, x0)
            display_table(results, "Newton-Raphson Method")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

window = tk.Tk()
window.title("Numerical Methods Solver")
window.geometry("800x600")

# 📌 Left Panel for Inputs
left_frame = tk.Frame(window, padx=20, pady=20, relief=tk.RIDGE, borderwidth=2)
left_frame.grid(row=0, column=0, sticky="ns")

tk.Label(left_frame, text="Differential Equation (dy/dx):", font=("Arial", 12)).pack(anchor="w")
eq_entry = tk.Entry(left_frame, width=40, font=("Arial", 10))
eq_entry.pack(pady=5)

tk.Label(left_frame, text="Derivative (Newton-Raphson):", font=("Arial", 12)).pack(anchor="w")
deriv_entry = tk.Entry(left_frame, width=40, font=("Arial", 10))
deriv_entry.pack(pady=5)

# 📌 Input Fields
for label, var in [("x0 (Initial x):", "x0_entry"), ("y0 (Initial y):", "y0_entry"),("xn (Final x):", "xn_entry"), ("Step Size (h):", "h_entry")]:
    tk.Label(left_frame, text=label, font=("Arial", 12)).pack(anchor="w")
    entry = tk.Entry(left_frame, width=10, font=("Arial", 10))
    entry.pack(pady=5)
    globals()[var] = entry

# 📌 Method Buttons
for method in ["Euler", "Improved Euler", "Runge-Kutta", "Newton-Raphson"]:
    tk.Button(left_frame, text=method, command=lambda m=method: run_method(m), font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", padx=10).pack(pady=10)

# 📊 Right Panel for Output Table
table_frame = tk.Frame(window, padx=20, pady=20, relief=tk.RIDGE, borderwidth=2)
table_frame.grid(row=0, column=1, sticky="nsew")

# Make the table frame expand
window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(0, weight=1)

# 🚀 Start Tkinter main loop
window.mainloop()