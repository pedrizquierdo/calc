import tkinter as tk
from tkinter import ttk

from operaciones import sumar, restar, multiplicar, dividir


def crear_interfaz():
    ventana = tk.Tk()
    ventana.title("Calculadora")
    ventana.resizable(False, False)

    marco = ttk.Frame(ventana, padding=20)
    marco.grid()

    ttk.Label(marco, text="Calculadora", font=("Segoe UI", 18)).grid(
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

    ttk.Button(marco, text="+", command=lambda: calcular(sumar)).grid(
        row=5, column=0, padx=3
    )
    ttk.Button(marco, text="-", command=lambda: calcular(restar)).grid(
        row=5, column=1, padx=3
    )
    ttk.Button(marco, text="*", command=lambda: calcular(multiplicar)).grid(
        row=5, column=2, padx=3
    )
    ttk.Button(marco, text="/", command=lambda: calcular(dividir)).grid(
        row=5, column=3, padx=3
    )

    ttk.Label(marco, textvariable=resultado, wraplength=320).grid(
        row=6, column=0, columnspan=4, pady=(20, 10)
    )

    def limpiar():
        entrada_a.delete(0, tk.END)
        entrada_b.delete(0, tk.END)
        resultado.set("Resultado: -")
        entrada_a.focus_set()

    ttk.Button(marco, text="Limpiar", command=limpiar).grid(
        row=7, column=0, columnspan=4
    )

    entrada_a.focus_set()
    ventana.mainloop()
