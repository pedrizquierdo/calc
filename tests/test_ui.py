import tkinter as tk
from tkinter import ttk
from unittest.mock import Mock

import pytest
import ui


@pytest.fixture(scope="module")
def ventana_tk():
    """Start Tk once for this test file, then close it after all tests."""
    ventana = tk.Tk()
    ventana.withdraw()
    try:
        yield ventana
    finally:
        ventana.destroy()


@pytest.fixture
def interfaz(monkeypatch, ventana_tk):
    """Build fresh calculator widgets for each test on the shared window."""
    ventana = ventana_tk

    # Make crear_interfaz use this window.
    monkeypatch.setattr(ui.tk, "Tk", lambda: ventana)

    # Prevent mainloop from waiting until someone closes the window.
    monkeypatch.setattr(ventana, "mainloop", lambda: None)

    # Tkinter normally prints callback errors instead of raising them.
    # Collect them so unexpected button errors fail the test.
    errores = []
    monkeypatch.setattr(
        ventana,
        "report_callback_exception",
        lambda tipo, error, traceback: errores.append(error),
    )

    try:
        ui.crear_interfaz()

        marco = ventana.winfo_children()[0]
        widgets = marco.winfo_children()

        entradas = [
            widget
            for widget in widgets
            if isinstance(widget, ttk.Entry)
        ]

        botones = {
            widget.cget("text"): widget
            for widget in widgets
            if isinstance(widget, ttk.Button)
        }

        etiqueta_resultado = next(
            widget
            for widget in widgets
            if isinstance(widget, ttk.Label)
            and widget.cget("textvariable")
        )

        # Read the StringVar connected to the result label.
        def leer_resultado():
            nombre = etiqueta_resultado.cget("textvariable")
            return ventana.getvar(nombre)

        yield {
            "ventana": ventana,
            "entradas": entradas,
            "botones": botones,
            "resultado": leer_resultado,
        }

        assert not errores, f"Unexpected callback errors: {errores}"

    finally:
        # Remove this test's widgets, but keep Tk alive for the next test.
        for widget in ventana.winfo_children():
            widget.destroy()


def escribir_numeros(interfaz, primero, segundo):
    """Helper to fill both inputs."""
    entrada_a, entrada_b = interfaz["entradas"]

    entrada_a.delete(0, tk.END)
    entrada_b.delete(0, tk.END)

    entrada_a.insert(0, primero)
    entrada_b.insert(0, segundo)


# ---------- crear_interfaz ----------

def test_crear_interfaz(interfaz):
    ventana = interfaz["ventana"]

    assert ventana.winfo_exists()
    assert ventana.title() == "Calculadora"
    assert tuple(map(int, ventana.resizable())) == (0, 0)

    assert len(interfaz["entradas"]) == 2
    assert set(interfaz["botones"]) == {"+", "-", "*", "/", "Limpiar"}

    assert all(entrada.get() == "" for entrada in interfaz["entradas"])
    assert interfaz["resultado"]() == "Resultado: -"


# ---------- calcular ----------

@pytest.mark.parametrize(
    "boton, esperado",
    [
        ("+", "Resultado: 9"),
        ("-", "Resultado: 3"),
        ("*", "Resultado: 18"),
        ("/", "Resultado: 2"),
    ],
)
def test_calcular_con_cada_boton(interfaz, boton, esperado):
    escribir_numeros(interfaz, "6", "3")

    interfaz["botones"][boton].invoke()

    assert interfaz["resultado"]() == esperado


def test_calcular_acepta_decimales_y_negativos(interfaz):
    escribir_numeros(interfaz, "-2.5", "1")

    interfaz["botones"]["+"].invoke()

    assert interfaz["resultado"]() == "Resultado: -1.5"


@pytest.mark.parametrize(
    "primero, segundo",
    [
        ("", ""),
        ("", "3"),
        ("6", ""),
        ("hola", "3"),
        ("6", "hola"),
    ],
)
def test_calcular_con_entrada_invalida(interfaz, primero, segundo):
    escribir_numeros(interfaz, primero, segundo)

    interfaz["botones"]["+"].invoke()

    assert interfaz["resultado"]() == "Escribe dos numeros validos."
    assert interfaz["ventana"].winfo_exists()


def test_calcular_division_entre_cero(interfaz):
    escribir_numeros(interfaz, "6", "0")

    interfaz["botones"]["/"].invoke()

    assert interfaz["resultado"]() == "No se puede dividir entre 0"
    assert interfaz["ventana"].winfo_exists()


def test_calcular_despues_de_corregir_un_error(interfaz):
    escribir_numeros(interfaz, "hola", "3")
    interfaz["botones"]["+"].invoke()

    assert interfaz["resultado"]() == "Escribe dos numeros validos."

    escribir_numeros(interfaz, "6", "3")
    interfaz["botones"]["+"].invoke()

    assert interfaz["resultado"]() == "Resultado: 9"


# ---------- limpiar ----------

@pytest.mark.parametrize(
    "primero, segundo, boton",
    [
        ("6", "3", "+"),       # Clear a successful calculation.
        ("hola", "3", "+"),    # Clear an invalid-input error.
        ("6", "0", "/"),       # Clear a division-by-zero error.
    ],
)
def test_limpiar(interfaz, monkeypatch, primero, segundo, boton):
    escribir_numeros(interfaz, primero, segundo)
    interfaz["botones"][boton].invoke()

    entrada_a, entrada_b = interfaz["entradas"]

    # Check that limpiar asks to focus the first input.
    enfocar = Mock()
    monkeypatch.setattr(entrada_a, "focus_set", enfocar)

    interfaz["botones"]["Limpiar"].invoke()

    assert entrada_a.get() == ""
    assert entrada_b.get() == ""
    assert interfaz["resultado"]() == "Resultado: -"
    enfocar.assert_called_once()


def test_limpiar_dos_veces(interfaz):
    interfaz["botones"]["Limpiar"].invoke()
    interfaz["botones"]["Limpiar"].invoke()

    assert all(entrada.get() == "" for entrada in interfaz["entradas"])
    assert interfaz["resultado"]() == "Resultado: -"