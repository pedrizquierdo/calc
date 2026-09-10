from operaciones import sumar, multiplicar


def test_sumar():
    #En este caso de prueba, verificamos que el resultado obtenido
    #de la funcion sea igual al resultado esperado que es 13
    assert sumar(6, 7) == 13


def test_mult():
    #En este caso de prueba, verificamos que el resultado obtenido
    #de la funcion sea igual al resultado esperado que es 42
    assert multiplicar(6, 7) == 42