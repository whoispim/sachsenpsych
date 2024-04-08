import sys
import pypdf
from datetime import time

# if len(sys.argv) <= 1:
#     print('Please enter file names of Detailansicht.pdf-files.')
#     exit()

# psy_pages = []
# for i in range(1, len(sys.argv)):
#     reader = pypdf.PdfReader(sys.argv[i])
#     psy_pages.extend([p.extract_text() for p in reader.pages])
reader = pypdf.PdfReader('Detailansicht_04103.pdf')
psy_pages = [p.extract_text() for p in reader.pages]
# print(psy_pages)

for p in psy_pages:
    p_name = p.split('\n')[3]
    p_fachgebiet = p.split('\n')[4][12:]
    p_praxis = p.split('\n')[5][8:] + ', ' + p.split('\n')[6]
    p_telefon = p.split('\n')[7][9:]
    p_erreichbarkeit = {}
    for line in p.split('Telefonische Erreichbarkeit\n')[1][5:].split('\n'):
        if line.split()[0] not in ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']:
            break
        line = line.replace(' Uhr', '')
        elements = line.split()
        p_erreichbarkeit[elements[0]] = []
        for pair in elements[1:]:
            a, b = pair.split('-')
            p_erreichbarkeit[elements[0]].append([
                time(*[int(x) for x in a.split(':')]), 
                time(*[int(x) for x in b.split(':')])
                ])
    p_leistungen = ''
    for line in p.split('Genehmigungspflichtige\nLeistungen: ')[1].split('\n'):
        if 'Die Leistung wird' in line or 'Fremdsprache: ' in line:
            break
        p_leistungen += line.replace('Psychotherapie: ', '') + ', '
    p_leistungen = p_leistungen[:-2]
    
    print(f'Name:       {p_name}')
    print(f'Adresse:    {p_praxis}')
    print(f'Fachgebiet: {p_fachgebiet}')
    print(f'Telefon:    {p_telefon}')
    print(f'Erreichbar: {p_erreichbarkeit}')
    print(f'Leistungen: {p_leistungen}')
    print()
