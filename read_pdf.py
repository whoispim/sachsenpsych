import glob
import pypdf
from datetime import time

def pdf_to_csv(folder = ''):
    file_list = glob.glob(folder + 'Detailansicht*.pdf')
    if len(file_list) < 1:
        print('Keine Dateien gefunden.')
        print('Die Dateinamen der PDFs müssen mit "Detailansicht" beginnen.')
        exit()
        
    psy_pages = []
    for filename in file_list:
        print(f'{filename} wird geladen.')
        reader = pypdf.PdfReader(filename)
        psy_pages.extend([p.extract_text() for p in reader.pages])

    psych_csv = ''
    psych_num = 0
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

        psych_num += 1
    
    with open('Detailansicht.csv', 'w', encoding='utf-8') as f:
        f.write(psych_csv)

    print(f'Erreichbarkeits- und Kontaktdaten zu {psych_num} Praxen wurden passend formatiert in der Datei beepboop.csv ausgegeben.')

if __name__ == '__main__':
    pdf_to_csv()
    