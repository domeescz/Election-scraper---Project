<H2> Popis projektu </H2>
Tento projekt slouží k exportu výsledků parlamentních voleb za územní celky v jednotlivých volebních obdobích.

<H2>Instalace knihoven</H2>
Pro zjištění všech knihoven, které jsou v kódu použity, použijte soubor requirements.txt
Instalace v novém virtuálním prostředí může vypadat například takhle:<br>
<pre>$ pip3 --version
$ pip3 install -r requirements.txt</pre>

<h2>Spuštění programu</h2>
Pro spuštění programu do příkazového řádku vložte příkaz v následující podobě (příkaz obsahuje 2 povinné argumenty):
<br><pre>py main.py <URL_územního_celku> <název_csv_souboru></pre>
<h3>Vzorový příklad</h3>
Spuštění programu může vypadat takhle (exportuji výsledky pro břeclavský okres):<br>
<pre>py main.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6204" "vysledky_voleb_breclavsko.csv"</pre>
