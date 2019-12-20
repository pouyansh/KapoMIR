from xml.etree import ElementTree
import csv


def read_xml(path, namespace):
    document = ElementTree.parse(path)
    root = document.getroot()
    documents = []
    for page in root.findall(namespace + 'page'):
        documents.append(
            page.find(namespace + 'revision/' + namespace + 'text').text)
    return documents


def read_csv(path):
    documents = []
    with open(path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            temp_line = ""
            for l in line:
                temp_line += l + " "
            documents.append(temp_line)
    return documents[1:]


def read_csv_phase2(path):
    documents = []
    with open(path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            temp_line = ""
            for l in range(1, len(line)):
                temp_line += line[l] + " "
            documents.append([line[0], temp_line])
    return documents[1:]
