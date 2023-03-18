import re

state = {
    "on/off" : False,
    "money" : 0
}


def get_saldo_str():
    return str(state["money"]//100)+"e"+(str(state["money"]%100))+"c"

def troco():
    coins = {
        1: 0, 
        2: 0,
        5: 0,
        10: 0,
        20: 0,
        50: 0,
        100: 0,
        200: 0 
    }

    for coin in [200,100,50,20,10,5,2,1]:
        while state["money"] >= 0:
            if state["money"] // coin == 0:
                break
            else:
                div = state["money"] // coin
                state["money"] -= div * coin
                coins[coin] += 1
    
    print(f"Sys: 'Troco = {coins[200]}x2e, {coins[100]}x1e, {coins[50]}x50c, {coins[20]}x20c, {coins[10]}x10c, {coins[5]}x5c, {coins[2]}x2c, {coins[1]}x1c'", end="")


def levantar():
    if state["on/off"] == True:
        print("Sys: 'Já esta levantado!'")
    else:
        print("Sys: 'Introduza moedas.'")
        state["on/off"] = True


def pousar():
    if state["on/off"] == False:
        print("Sys: 'Telefone não foi levantado!'")
    else:
        troco()
        print(" Volte sempre!'")
        state["on/off"] = False
        state["money"] = 0


def moeda(line):
    values = re.split(r"\s*,\s*", line[6:][:-1])
    invalid_coins = list()

    for coin in values:
        if match := re.match(r"(\d+)c", coin):
            value = int(match.group(1))
            if value in [1,2,5,10,20,50]:
                state["money"] += value
            else:
                invalid_coins.append(coin)
        elif match := re.match(r"(\d+)e", coin):
            value = int(match.group(1))
            if value in [1,2]:
                state["money"] += value*100
            else:
                invalid_coins.append(coin)
        else:
            invalid_coins.append(coin)

    string = "Sys : "
    for coin in invalid_coins:
        string += coin + " - moeda inválida; "
    string += f"saldo = {get_saldo_str()}" 
    print(string)


def numero(line):
    if state["on/off"] == False:
        print("Sys: 'Telefone não está levantado!'")
    else:
        number = line[2:]

        if not re.match(r"(\d{9}|00\d{9})$", number):
            print("Sys: 'Número inválido!'")

        elif re.match(r"601|641", number):
            print("Sys: 'Este indicativo está bloqueado.'")

        elif re.match(r"00", number):
            saldo = state["money"]
            if saldo >= 150:
                state["money"] -= 150
                print(f"Sys: 'saldo = {get_saldo_str()}'")
            else:
                print("Sys: 'Saldo insuficiente!'")

        elif re.match(r"2", number):
            saldo = state["money"]
            if saldo >= 25:
                state["money"] -= 25
                print(f"Sys: 'saldo = {get_saldo_str()}'")
            else:
                print("Sys: 'Saldo insuficiente!'")

        elif re.match(r"808", number):
            saldo = state["money"]
            if saldo >= 10:
                state["money"] -= 10
                print(f"Sys: 'saldo = {get_saldo_str()}'")
            else:
                print("Sys: 'Saldo insuficiente!'")
        elif re.match(r"800", number):
            print(f"Sys: 'saldo = {get_saldo_str()}'")




def abortar():
    if state["on/off"] == False:    
        print("Sys: 'Telefone não está levantado!'")
    else:
        troco()
        print()
        state["money"] = 0


def main():
    print("- Informações:")
    print("1. Para números iniciados por 601 ou 641 a chamada é bloqueada")
    print("2. Para chamadas internacionais (iniciadas por 00) o utilizador tem que ter um saldo mínimo de 1,5 euros")
    print("3. Para chamadas nacionais (iniciadas por 2) o saldo mínimo e custo de chamada é de 25 cêntimos")
    print("4. Para chamadas verdes (iniciadas por 800) o custo é 0")
    print("5. Para chamadas azuis (iniciadas por 808) o custo é de 10 cêntimos")
    print("")
    print("- Lista de comandos: LEVANTAR, MOEDA, T=, POUSAR, ABORTAR")
    print("")
    print("NOTAS:")
    print("As moedas são 'e', euros, ou 'c', cêntimos.")
    print("Os comandos LEVANTAR, POUSAR e ABORTAR devem não têm argumentos")
    print("Os comandos T= e MOEDA são seguidos por um nº de telemóvel e uma lista de moedas, respetivamente")
    print("")
    while True:
        line = input()

        if re.match(r"LEVANTAR", line):
            levantar()
        elif re.match(r"POUSAR", line):
            pousar()
        elif re.match(r"MOEDA", line):
            moeda(line)
        elif re.match(r"T", line):
            numero(line)
        elif re.match(r"ABORTAR", line):
            abortar()



if __name__ == '__main__':
    main()