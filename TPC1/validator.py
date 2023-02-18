def validar_sexo(sexo):
    return sexo == "M" or sexo == "F"

def validar_inteiro(numero):
    try:
        integer = int(numero)

        return integer > 0
    except ValueError:
        return False

def validar_bit(bit):
    return bit == "0" or bit == "1"



