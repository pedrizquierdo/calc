def calcular(a, b, operador):
    if operador == "+":
        return a + b
    elif operador == "-":
        return a - b
    else:
        return "Operador no válido"

num1 = float(input("Ingresa el primer número: "))
operador = input("Ingresa la operación (+ o -): ")
num2 = float(input("Ingresa el segundo número: "))

resultado = calcular(num1, num2, operador)

print("Resultado:", resultado)