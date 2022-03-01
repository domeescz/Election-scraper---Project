<H2> Popis projektu </H2>
Tento projekt slouží k exportu výsledků parlamentních voleb za územní celky v daném volebním období.

<H2>Instalace knihoven</H2>
Pro zjištění všech knihoven, které jsou v kódu použity, použijte soubor requirements.txt
Instalace v novém virtuálním prostředí může vypadat například takhle:<br>
<pre>$ pip3 --version
$ pip3 install -r requirements.txt</pre>

<h2>Spuštění programu</h2>
Pro spuštění programu do příkazového řádku je nutné zadat 2 argumenty: URL adresu daného okresu a název *.CSV souboru.
<h2>Vzorový příklad</h2>
<br>Pro daný příklad byly použity územní celky okresu Břeclav (link - https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6204).<br>
<br>
Spuštění programu může vypadat takhle:<br>
<pre>py main.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6204" "vysledky_voleb_breclavsko.csv"</pre>
