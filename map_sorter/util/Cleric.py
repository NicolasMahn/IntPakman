import json
import csv

def read_json(directory):
    f = open(directory, 'r', encoding='UTF8')
    data = json.loads(f.read())
    f.close()
    return data

def read_csv(directory):
    return read_comma_csv(directory)

def read_comma_csv(directory):
    f = open(directory, 'r', encoding='UTF8')
    file_data = csv.reader(f)
    data = []
    for fd in file_data:
        data.append(fd)
    f.close()
    return data

def read_semicolon_csv(directory):
    f = open(directory, 'r', encoding='UTF8')
    file_data = csv.reader(f, delimiter=';')
    data = []
    for fd in file_data:
        data.append(fd)
    f.close()
    return data

def read(directory):
    f = open(directory, 'r', encoding='UTF8')
    data = f.read()
    f.close()
    return data


def write_json(l, directory):
    f = open(directory, 'w', encoding='UTF8')
    j = json.dumps(l, indent = 4)
    f.write(j)

def write_csv(l, directory):
    write_comma_csv(l, directory)

def write_comma_csv(l, directory):
    f = open(directory, 'w', encoding='UTF8', newline='')
    writer = csv.writer(f)
    writer.writerows(l)
    f.close()

def write_semicolon_csv(l, directory):
    f = open(directory, 'w', encoding='UTF8', newline='')
    writer = csv.writer(f, delimiter=';')
    writer.writerows(l)
    f.close()

def write(l, directory):
    f = open(directory, 'w', encoding='UTF8')
    f.write(l)
    f.close()
