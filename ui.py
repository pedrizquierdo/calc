import tkinter as tk
from tkinter import ttk

from operaciones import sumar, restar, multiplicar, dividir


def crear_interfaz():
    ventana = tk.Tk()
    ventana.title("Calculadora")
    ventana.resizable(False, False)
    ventana.configure(bg="#1c1c1e")

    estilo = ttk.Style()
    estilo.theme_use("clam")
    estilo.configure("TFrame", background="#1c1c1e")
    estilo.configure("TLabel", background="#1c1c1e", foreground="#ffffff")
    estilo.configure("TEntry", fieldbackground="#333333", foreground="white",
                      insertcolor="white", borderwidth=0)

    estilo.configure("Op.TButton", background="#ff9f0a", foreground="white",
                      font=("Segoe UI", 13, "bold"), padding=10, borderwidth=0)
    estilo.map("Op.TButton", background=[("active", "#ffb340")])

    estilo.configure("Func.TButton", background="#a5a5a5", foreground="black",
                      font=("Segoe UI", 11), padding=8, borderwidth=0)
    estilo.map("Func.TButton", background=[("active", "#c7c7c7")])

    marco = ttk.Frame(ventana, padding=20)
    marco.grid()

    ttk.Label(marco, text="Calculadora", font=("Segoe UI", 18, "bold")).grid(
        row=0, column=0, columnspan=4, pady=(0, 15)
    )

    ttk.Label(marco, text="Primer numero:").grid(
        row=1, column=0, columnspan=4, sticky="w"
    )
    entrada_a = ttk.Entry(marco, width=35)
    entrada_a.grid(row=2, column=0, columnspan=4, sticky="ew", pady=(5, 10))

    ttk.Label(marco, text="Segundo numero:").grid(
        row=3, column=0, columnspan=4, sticky="w"
    )
    entrada_b = ttk.Entry(marco, width=35)
    entrada_b.grid(row=4, column=0, columnspan=4, sticky="ew", pady=(5, 15))

    resultado = tk.StringVar(value="Resultado: -")

    def calcular(operacion):
        try:
            a = float(entrada_a.get())
            b = float(entrada_b.get())
        except ValueError:
            resultado.set("Escribe dos numeros validos.")
            return

        try:
            valor = operacion(a, b)
            resultado.set(f"Resultado: {valor:g}")
        except ValueError as error:
            resultado.set(str(error))

    ttk.Button(marco, text="+", style="Op.TButton", command=lambda: calcular(sumar)).grid(
        row=5, column=0, padx=3
    )
    ttk.Button(marco, text="-", style="Op.TButton", command=lambda: calcular(restar)).grid(
        row=5, column=1, padx=3
    )
    ttk.Button(marco, text="*", style="Op.TButton", command=lambda: calcular(multiplicar)).grid(
        row=5, column=2, padx=3
    )
    ttk.Button(marco, text="/", style="Op.TButton", command=lambda: calcular(dividir)).grid(
        row=5, column=3, padx=3
    )

    ttk.Label(marco, textvariable=resultado, wraplength=320,
              font=("Segoe UI", 14)).grid(
        row=6, column=0, columnspan=4, pady=(20, 10)
    )

    def limpiar():
        entrada_a.delete(0, tk.END)
        entrada_b.delete(0, tk.END)
        resultado.set("Resultado: -")
        entrada_a.focus_set()

    ttk.Button(marco, text="Limpiar", style="Func.TButton", command=limpiar).grid(
        row=7, column=0, columnspan=4, pady=(5, 0)
    )

    entrada_a.focus_set()
    ventana.mainloop()
