from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
from pprint import pprint
import sys
o = '====='*5

def main():

#---------------------------------LET'S FIND ALL TABLES----------------------------------------
    url = sys.argv[1]
    get_req = requests.get(url)
    soup = BeautifulSoup(get_req.text, 'html.parser')
    print(o)
    print(f'Loading the URL...')
    table = soup.findAll('table')

    list_radku = []
    list_odkazu = []

    for tabulka in table:

        for row in tabulka.findAll('tr'):

            list_bunek = []
            odkazy = []

            for cell in row.findAll(['td']):

                for a in row.findAll('a',href=True):
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
            odkaz = i
            list_odkazu_o.append(odkaz[0])

#-----------------------------------End the first URL-----------------------------------------------
    soup.clear()

#-----------------------------------Sends get for another URL----------------------------------------
    print('Loading the data...')
    tab_1 = []
    for i in list_odkazu_o:
        url_1 = "https://volby.cz/pls/ps2017nss/"+i
        get_req_o = requests.get(url_1)
        soup_o = BeautifulSoup(get_req_o.text, 'html.parser')
        table_o = soup_o.findAll('table')
        jme=[]

#------------------------------------for x table in table_o--------------------------
        for tabulka in table_o:

            for row in tabulka.findAll('tr'):
                udaje = []
#-----------------------------------Take data from first table for all towns-----------------
                for cell in tabulka.findAll('td', {'class': 'cislo'}):

                    text = cell.get_text()
                    udaje.append(text)

            tab_1.append(udaje)
#------------------------------------Saves the names of candidates into one list---------------
    jme=[]
    for cell in soup_o.findAll('td',{'class':'overflow_name'}):
        text = cell.get_text()
        jme.append(text)

#------------------------------------Take data from first table and save it into the variable----------------
    prvni_tabulka = tab_1[::3]
    prvni_souhrn = []
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
#------------------------------------Take data from second table and save it into the variable----------------
    druha_tabulka = tab_1[1::3]
    data_druha = []
    for a in druha_tabulka:
        data=[]
        data = a[1::3]
        data_druha.append(data)
#------------------------------------Take data from third table and save it into the variable----------------
    treti_tabulka = tab_1[2::3]
    data_treti = []
    for a in treti_tabulka:
        data=[]
        data = a[1::3]
        data_treti.append(data)

#----------------------------------------Remove blank lists---------------------------------------------
    list_radku_f = [x for x in list_radku if x]

#----------------------------------------Writing data into final list before exporting to csv-----------
    for i, mesto in enumerate(list_radku_f):
        if i in range(0, len(list_radku_f)):
            list_radku_f[i].append(prvni_souhrn[i][0]) #write a value from first table
            list_radku_f[i].append(prvni_souhrn[i][1])
            list_radku_f[i].append(prvni_souhrn[i][2])
            for index, data in enumerate(data_druha[i]): #write a value from second table
                list_radku_f[i].append(data_druha[i][index])
            for index, data in enumerate(data_treti[i]): #write a value from third table
                list_radku_f[i].append(data_treti[i][index])

#-----------------------------------------check and remove \xa0 characters-------------------------
        for temp_index,a in enumerate(mesto):
            if '\xa0' in a:
                list_radku_f[i][temp_index] = a.replace(u'\xa0',u'')

#----------------------------OPENING AND WRITING INTO CSV-------------------
    print("Writing the data into CSV...")
    f = open(sys.argv[2],'w',newline='', encoding='utf-8')
    headers = ["code", "location", "registered", "envelopes", "valid"]

    #---------Write all names of candidates to the header---------
    for index, strana in enumerate(jme):
        headers.append(strana.replace(',','|'))
    write = csv.writer(f, delimiter=';')
    write.writerow(headers)
    write.writerows(list_radku)
    print(f'The export to "{sys.argv[2]}.csv" has been done.')
    print(o)
    f.close()


#now check and delete empty rows
    df = pd.read_csv(sys.argv[2], sep='\t')
# Droping the empty rows
    modifiedDF = df.dropna()
# Saving it to the csv file
    modifiedDF.to_csv(sys.argv[2], index=False)

if __name__ == '__main__':
    main()
