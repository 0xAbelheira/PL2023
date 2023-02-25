linha = input("%")
soma = 0

aux = ""

state = True
aux_state = ""


for c in linha:
    c = c.upper()

    if state == True:
        if '0' <= c <= '9':
            aux += c
        else:
            if len(aux) != 0:
                soma += int(aux)
                aux = ""

    if c == "O":
        aux_state = c
    elif c == "N" and aux_state == "O": 
        state = True
        aux_state = ""
    elif c == "F" and aux_state == "OF":
        state = False
        aux_state = ""
    elif c == "F" and aux_state == "O":
        aux_state += c
    elif c == "=":
        print(soma)

    

