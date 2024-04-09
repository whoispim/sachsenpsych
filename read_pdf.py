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

psychs = []
psych_csv = ''
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
    
    # print(f'Name:       {p_name}')
    # print(f'Adresse:    {p_praxis}')
    # print(f'Fachgebiet: {p_fachgebiet}')
    # print(f'Telefon:    {p_telefon}')
    # print(f'Erreichbar: {p_erreichbarkeit}')
    # print(f'Leistungen: {p_leistungen}')
    # print()
    
    erreich_list = []
    for tag in p_erreichbarkeit.keys():
        for zeit in p_erreichbarkeit[tag]:
            erreich_list.append(tag + '\t' + zeit[0].strftime('%H:%M') + '\t'+ zeit[1].strftime('%H:%M'))
    # print(erreich_list)
    
    psych_csv += f'TRUE\t{p_name}\t\t\t'
    if len(erreich_list) > 0: psych_csv += erreich_list.pop(0)
    psych_csv += f'\n\t{p_fachgebiet}\t{p_praxis}\t\t'
    if len(erreich_list) > 0: psych_csv += erreich_list.pop(0)
    psych_csv += f'\n\t{p_leistungen}\t{p_telefon}\t\t'
    if len(erreich_list) > 0: psych_csv += erreich_list.pop(0)
    psych_csv += '\n'
    while len(erreich_list) > 0:
        psych_csv += f'\t\t\t\t{erreich_list.pop(0)}\n'
    psych_csv += '\n'


    # psychs.append([p_name, p_fachgebiet, p_praxis, p_leistungen, p_telefon, p_erreichbarkeit])

with open('beepboop.csv', 'w', encoding='utf-8') as f:
    f.write(psych_csv)
