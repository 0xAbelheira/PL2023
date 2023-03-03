import re
import json

def processes_per_year(lines):
    processes = dict()

    for data in lines:
        year = data["year"]
        if year not in processes:
            processes[year] = 1
        else:
            processes[year] += 1

    return processes


def names_per_century(lines):
    first_names = dict()
    last_names = dict()
    
    for data in lines:
        #print(data["name"])
        first_name = re.match(r"[A-Za-z]+\b", data["name"]).group()
        last_name = re.search(r"[A-Za-z]+$", data["name"]).group()
        year = data["year"]
        sec = (int(year) % 100) + 1

        if sec not in first_names:
            first_names[sec] = dict()

        if sec not in last_names:
            last_names[sec] = dict()
        
        if first_name not in first_names[sec]:
            first_names[sec][first_name] = 0
        
        if last_name not in last_names[sec]:
            last_names[sec][last_name] = 0

        first_names[sec][first_name] += 1
        last_names[sec][last_name] += 1

    return (first_names, last_names)
        

def relationshiop_frequency(lines):
    frequency = dict()

    for data in lines:
        obs = data["obs"]
        if match := re.search(r"?i:irmao|irma|pai|mae|tio|tia|avo|primo|prima|sobrinho|sobrinha", obs):
            relation = match.group().lower()
            
            if relation not in frequency:
                frequency[relation] = 0

            frequency[relation] += 1

    return frequency


def processes_to_json(lines):
    first_twenty = lines[:20]

    file = open("registos.json", "w")
    json.dump(first_twenty, file)
    file.close()

def main():
    file = open("processos.txt")
    valid_lines = list()

    regex = re.compile(r"(?P<folder>\d+)::(?P<year>\d{4})\-(?P<month>\d{2})-(?P<day>\d{2})::(?P<name>[A-Za-z ]+)::(?P<f_name>[A-Za-z ]+)::(?P<m_name>[A-Za-z ]+)::(?P<obs>[^:]*)::")

    matches = regex.finditer(file.read())

    for match in matches:
        valid_lines.append(match.groupdict())

    processes_to_json(valid_lines)

    option = 0
    while option != 5:
        print('\n')
        print('Escolha uma opção')
        print('-----------------------------------------')
        print('1 - Frequência de processos por ano')
        print('2 - Frequência de nomes próprios e apelidos')
        print('3 - Frequência dos vários tipos de relação')
        print('4 - Converter os 20 primeiros registos para formato Json')
        print('5 - Sair')
        print('-----------------------------------------')
        option = int(input())

        match option:
            case 1:
                print(processes_per_year(valid_lines))
                
            case 2:
                print(names_per_century(valid_lines))

            case 3:
                print(relationshiop_frequency(valid_lines))

            case 4:
                open("registos.json")

            case 5: 
                print("A sair...")

            case _:
                print("Opção inválida!")
    
if __name__ == '__main__':
    main()