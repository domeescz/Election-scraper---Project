from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
from pprint import pprint


url = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"

get_req = requests.get(url)
soup = BeautifulSoup(get_req.text, 'html.parser')

table = soup.findAll('table')

list_radku = []
list_odkazu = []

#funkce pro zápis do CSV
def csv_file_writer(filename):
#----------------------------HEADER OF CSV----------------------------------

#----------------------------OPENING AND WRITING INTO CSV-------------------

    f = open(filename,'w',newline='', encoding='utf-8')
    headers = ["code", "location", "registered", "envelopes", "valid"]
    #---------write all strany to the header---------
    for index, strana in enumerate(jme):
        headers.append(jme[index])
    write = csv.writer(f, delimiter=';', quotechar='"')
    write.writerow(headers)
    write.writerows(list_radku)
    print('done')
    f.close()


#now check and delete empty rows
    df = pd.read_csv(filename, sep='\t')
# Droping the empty rows
    modifiedDF = df.dropna()
# Saving it to the csv file
    modifiedDF.to_csv(filename, index=False)

#-----------------------------LET'S FIND ALL TABLES-------------------------
for tabulka in table:

    for row in tabulka.findAll('tr'):

        list_bunek = []
        odkazy = []

        for cell in row.findAll(['td']):

            for a in row.findAll('a',href=True):
                #if a.text:
                    odkazy.append(a["href"])

            if cell not in row.findAll('td',{"class":"hidden_td"}):

                text = cell.get_text()

                if text != 'X':     #zahození znaku X pro sběr dat
                    list_bunek.append(text)
        list_odkazu.append(odkazy)
        list_radku.append(list_bunek)
list_odkazu_o = []

#ziska odkazy z tabulky
for i in list_odkazu:
    if i != []:
        #print(i)
        odkaz = i
        list_odkazu_o.append(odkaz[0])

#ukončí GET první URL
soup.clear()
#-----------------------------------pošle GET na další URL----------------------------------------
tab_1 = []
tab_2 = []
detailni = []
#-----------------------------------loop for all found urls----------------------------
for i in list_odkazu_o:
    url_1 = "https://volby.cz/pls/ps2017nss/"+i
    get_req_o = requests.get(url_1)
    soup_o = BeautifulSoup(get_req_o.text, 'html.parser')
    #print(soup_o)
    table_o = soup_o.findAll('table')
    table_jmena = soup_o.find('table')
    jme=[]


    for tabulka in table_o:

        for row in tabulka.findAll('tr'):
            udaje = []

#-----------------------------------vytáhne údaje z 1. tabulky  pro všechny okrsky-----------------

            for cell in tabulka.findAll('td', {'class': 'cislo'}):

                    text = cell.get_text()
                    udaje.append(text)

        tab_1.append(udaje)  # každou tabulku zapíše do listu
#        continue

jmena_stran = []
#------------------------------------uloží jména kandidujících stran do jednoho listu---------------
jme=[]
for cell in soup_o.findAll('td',{'class':'overflow_name'}):
        text = cell.get_text()
        jme.append(text)
print(jme)

#------------------------------------vytáhne data z první tabulky-----------------------------------
prvni_tabulka = tab_1[::3]
new_tab = []
prvni_souhrn = []
#------------------------------------upraví data z první tabulky potřebné pro export----------------
for i, a in enumerate(prvni_tabulka):
    prvni = []
    for cislo in a:
        if cislo == a[3]:
            prvni.append(cislo)

        elif cislo == a[4]:
            prvni.append(cislo)
            break
    for cislo in a:
        if cislo == a[7]:
            prvni.append(cislo)
            break

    prvni_souhrn.append(prvni)
#------------------------------------vytáhne data z druhé tabulky-----------------------------------
druha_tabulka = tab_1[1::3]
data_druha = []
for a in druha_tabulka:
    data=[]
    data = a[1::3]
    data_druha.append(data)
#------------------------------------vytáhne data z třetí tabulky-----------------------------------
treti_tabulka = tab_1[2::3]
data_treti = []
for a in treti_tabulka:
    data=[]
    data = a[1::3]
    data_treti.append(data)

#----------------------------------------Collects data for each town------------------------------------
for i, a in enumerate(tab_1):
    if i in range(0,len(tab_1), 3):
        new_tab.append(tab_1[i:i+3])

#----------------------------------------Remove blank lists---------------------------------------------
list_radku_f = [x for x in list_radku if x]
#----------------------------------------writing data into final list before exporting to csv-----------

for i, mesto in enumerate(list_radku_f):
    if i in range(0, len(list_radku_f)):
        list_radku_f[i].append(prvni_souhrn[i][0]) #zapíše hodnotu z 1.tabulky
        list_radku_f[i].append(prvni_souhrn[i][1]) #zapíše hodnotu z 1. tabulky
        list_radku_f[i].append(prvni_souhrn[i][2])  # zapíše hodnotu z 1. tabulky
        for index, data in enumerate(data_druha[i]):
            list_radku_f[i].append(data_druha[i][index]) #zapíše hodnotu z 2.tabulky
        for index, data in enumerate(data_treti[i]):
            list_radku_f[i].append(data_treti[i][index])  # zapíše hodnotu z 3. tabulky

#-----------------------------------------check and remove \xa0 characters-------------------------
    for temp_index,a in enumerate(mesto):
        if '\xa0' in a:
            list_radku_f[i][temp_index] = a.replace(u'\xa0',u'')

csv_file_writer('ahojda10.csv')
