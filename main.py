import tkinter as tk
from tkinter import ttk, messagebox
import sympy as sp
import re

def safe_eval(expr, x, y=0):
    try:
        x_sym, y_sym = sp.symbols('x y')
        expr = expr.replace("^", "**") 
        expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
        expr = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', expr) 
        expr = re.sub(r'([a-zA-Z])([a-zA-Z])', r'\1*\2', expr)
        f = sp.sympify(expr)
        return float(f.evalf(subs={x_sym: x, y_sym: y}))
    except Exception as e:
        messagebox.showerror("Error", f"Ecuacion invalida: {e}")
        return None

def safe_eval_raphson(ecuacion,x):
        x_sym = sp.Symbol('x')
        ecuacion = ecuacion.replace("^", "**")
        ecuacion = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', ecuacion)
        ecuacion = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', ecuacion) 
        ecuacion = re.sub(r'([a-zA-Z])([a-zA-Z])', r'\1*\2', ecuacion)
        f = sp.sympify(ecuacion)
        print(f)
        return float(f.evalf(subs={x_sym: x}))

def derive(ecuacion, x):
        x_sym = sp.Symbol('x')
        ecuacion = ecuacion.replace("^", "**")
        ecuacion = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', ecuacion)
        ecuacion = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', ecuacion) 
        ecuacion = re.sub(r'([a-zA-Z])([a-zA-Z])', r'\1*\2', ecuacion)
        f = sp.sympify(ecuacion)
        f_prime = sp.diff(f, x_sym)
        print(f_prime)
        return float(f_prime.evalf(subs={x_sym: x}))


def euler_mejorado(ecuacion, x0, y0, xn, h):
    x, y = x0, y0
    resultados = []
    n = 0
    tolerancia = 1e-9
    while x <= xn + tolerancia:
        fxy = safe_eval(ecuacion, x, y) 
        y_p = y + h * fxy
        fxy_p = safe_eval(ecuacion, x + h, y_p)
        y_nuevo = y + h / 2 * (fxy + fxy_p)
        x_nuevo = x + h

        resultados.append((n, x, y, y_p, x_nuevo, y_nuevo))

        x, y = x_nuevo, y_nuevo
        n += 1
    return resultados

def runge_kutta(ecuacion, x0, y0, xn, h):
    x, y = x0, y0
    resultados = []
    n = 0
    tolerancia = 1e-9
    while x <= xn + tolerancia:
        k1 = safe_eval(ecuacion, x, y)
        k2 = safe_eval(ecuacion, x + (h / 2), y + (h*k1 / 2))
        k3 = safe_eval(ecuacion, x + (h / 2), y + (h*k2 / 2))
        k4 = safe_eval(ecuacion, x + h, y + h*k3)
        y_nuevo = y + h*(k1 + 2 * k2 + 2 * k3 + k4) / 6
        x_nuevo = x+h
        resultados.append((n,x,y,k1,k2,k3,k4,y_nuevo))
        y = y_nuevo
        x = x_nuevo
        n += 1
    return resultados

def newton_raphson(ecuacion, x0, tole):
        x = x0
        tolerancia = tole
        max_iterations = 100
        resultados = []
        n = 0
        for i in range(max_iterations):
            f_val = safe_eval_raphson(ecuacion, x)
            f_prime_val = derive(ecuacion, x)
            
            if f_prime_val == 0:
                messagebox.showerror("Error", "Derivada es 0")
                return
            
            xn_nuevo = x - f_val / f_prime_val
            
            resultados.append((n, x, f_val, f_prime_val, xn_nuevo))
            
            if abs(xn_nuevo - x) < tolerancia:
                break
            x = xn_nuevo
            n +=1
        return resultados


def display_table(resultados, titulo):
    for widget in table_frame.winfo_children():
        widget.destroy()

    ttk.Label(table_frame, text=titulo, font=("Arial", 12, "bold")).pack(pady=5)

    if titulo == "Metodo Euler Mejorado":
        columns = ("n", "x_n", "y_n", "(y_n+1)*", "x_n+1", "y_n+1")
    elif titulo == "Metodo Runge-Kutta (4th Orden)":
        columns = ("n", "x_n", "y_n", "k1", "k2","k3","k4", "y_n+1")
    elif titulo == "Metodo Newton-Raphson":
        columns = ("n", "x_n","f(x)", "f'(x)", "x_nuevo")
    table = ttk.Treeview(table_frame, columns=columns, show="headings")

    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=100)

    table.pack()

    for row in resultados:
        table.insert("", "end", values=[f"{v:.6f}" if isinstance(v, float) else v for v in row])


def run_metodo(metodo):
    try:
        if metodo == "Euler Mejorado":
            ecuacion = ecuacion_input.get()
            x0 = float(x0_input.get())
            y0 = float(y0_input.get())
            xn = float(xn_input.get())
            h = float(h_input.get())
            resultados = euler_mejorado(ecuacion, x0, y0, xn, h)
            display_table(resultados, "Metodo Euler Mejorado")

        elif metodo == "Runge-Kutta":
            ecuacion = ecuacion_input.get()
            x0 = float(x0_input.get())
            y0 = float(y0_input.get())
            xn = float(xn_input.get())
            h = float(h_input.get())
            resultados = runge_kutta(ecuacion, x0, y0, xn, h)
            display_table(resultados, "Metodo Runge-Kutta (4th Orden)")

        elif metodo == "Newton-Raphson":
            ecuacion = ecuacion_input.get()
            x0 = float(x0_input.get())
            tole = float(tolerancia_input.get())
            resultados = newton_raphson(ecuacion, x0, tole)
            display_table(resultados, "Metodo Newton-Raphson")
    except Exception as e:
        messagebox.showerror("Error", f"Salio un error: {e}")
        return None


window = tk.Tk()
window.title("Metodos de Ecuaciones Unidad III")
window.geometry("1200x600")

lado_izq = tk.Frame(window, padx=20, pady=20, relief=tk.RIDGE, borderwidth=2)
lado_izq.grid(row=0, column=0, sticky="ns")

tk.Label(lado_izq, text="Ecuacion diferencial (dy/dx):", font=("Arial", 12)).pack(anchor="w")
ecuacion_input = tk.Entry(lado_izq, width=40, font=("Arial", 10))
ecuacion_input.pack(pady=5)

for label, var in [("x0:", "x0_input"), ("y0:", "y0_input"),("xn:", "xn_input"), ("h:", "h_input"),("Tole:", "tolerancia_input")]:
    tk.Label(lado_izq, text=label, font=("Arial", 12)).pack(anchor="w")
    input = tk.Entry(lado_izq, width=10, font=("Arial", 10))
    input.pack(pady=5)
    globals()[var] = input

for metodo in ["Euler Mejorado", "Runge-Kutta", "Newton-Raphson"]:
    tk.Button(lado_izq, text=metodo, command=lambda m=metodo: run_metodo(m), font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", padx=10).pack(pady=10)

table_frame = tk.Frame(window, padx=20, pady=20, relief=tk.RIDGE, borderwidth=2)
table_frame.grid(row=0, column=1, sticky="nsew")

window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(0, weight=1)

window.mainloop()