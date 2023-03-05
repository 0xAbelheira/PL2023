import re
import json

def print_dict(dict):
    print(' ' * 50 + "| Frequência")
    print('-' * 100)
    for key in dict.keys():
        print(key + ' ' * (50-len(key)) + "| " + str(dict[key]))

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
        

def relationshiop_frequency(data):
    relationship = dict()

    for process in data:
        obs = process["obs"]
        if match := re.search(r"(?i)[a-zA-Z ],([A-Z][a-zA-Z ]*)\.", obs):
            relation = match.group(1)
            
            if relation not in relationship:
                relationship[relation] = 0
            relationship[relation] += 1
    
    return relationship

def most_used_names_per_sec(first_names, last_names):
    first_name_keys_sorted = list(first_names.keys())
    last_name_keys_sorted = list(last_names.keys())

    first_name_keys_sorted.sort()
    last_name_keys_sorted.sort()
    
    print("================================================================")
    print("                         First names")
    print("================================================================")
    for sec in first_name_keys_sorted:
        print('-' * 20)
        print("     Século " + str(sec))

        items = list(first_names[sec].items())
        items.sort(key=lambda x : x[1], reverse=True)

        for i in range(0, 5):
            print(items[i])


    print("================================================================")
    print("                         Last names")
    print("================================================================")
    for sec in last_name_keys_sorted:
        print('-' * 20)
        print("     Século " + str(sec))

        items = list(last_names[sec].items())
        items.sort(key=lambda x : x[1], reverse=True)

        for i in range(0, 5):
            print(items[i])

def processes_to_json(data, path):
    file = open(path + ".json", "w")
    json.dump(data[:20], file)
    file.close()

def main():
    file = open("processos.txt")
    regex = re.compile(r"(?P<folder>\d+)::(?P<year>\d{4})\-(?P<month>\d{2})-(?P<day>\d{2})::(?P<name>[A-Za-z ]+)::(?P<f_name>[A-Za-z ]+)::(?P<m_name>[A-Za-z ]+)::(?P<obs>.*)::")

    valid_lines = list()
    matches = regex.finditer(file.read())
    for match in matches:
        valid_lines.append(match.groupdict())

    option = 0
    while option != 5:
        print("------------------------------------------")
        print("1 - Frequência de processos por ano")
        print("2 - Frequência de nomes por século")
        print("3 - Frequência de tipos de relação")
        print("4 - 20 primeiros registos para json")
        print("5 - Sair")
        print("------------------------------------------")

        option = int(input())

        match option:
            case 1:
                print_dict(processes_per_year(valid_lines))

            case 2:
                first_names, last_names = names_per_century(valid_lines)
                most_used_names_per_sec(first_names, last_names)
            case 3:
                print_dict(relationshiop_frequency(valid_lines))
            case 4:
                print("Nome do ficheiro:")
                path = input()
                processes_to_json(valid_lines, path)
            case 5:
                print("A sair...")
            case _:
                print("Opção inválida!")
    
if __name__ == '__main__':
    main()