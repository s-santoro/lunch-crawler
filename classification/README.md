# Luigi Pipeline
Die Luigi Pipeline Software wird für das Preprocessing, Klassifikation und Evaluation verwendet.
Luigi managed dependency resolution, workflow management und Visualisierung von ausgeführten Tasks.
[Luigi Documentation](https://luigi.readthedocs.io/en/latest/index.html)

### Pipeline starten
Luigi in Kombination mit dem luigidaemon starten (webinterface).
Das Webinterface ist auf localhost:8082 verfügbar.
Befehl um Luigidaemon zu starten: `$ luigid`  
Befehl um die Pipeline mit Modul _Evaluator.py_ zu starten (zuerst in scripts-Ordner wechseln):
`$ python3 -m luigi --module Evaluator Evaluator --scheduler-host localhost`  

Luigi ohne Webinterface starten.
Befehl um die Pipeline mit Modul _Evaluator.py_ zu starten (zuerst in scripts-Ordner wechseln):
`$ python3 -m luigi --module Evaluator Evaluator --local-scheduler`  

### WICHTIGER HINWEIS
Zuerst muss das Konfigurationsfile zu "./configs/Configurations.py" umbenannt werden.
Vorhandene Konfigurationsfiles sind:
- "./configs/ConfigurationsML.py" für Machine-learning pipeline
- "./configs/ConfigurationsRB.py" für Rule-based pipeline

### Quellen der Stoppwortliste
[Solariz](https://github.com/solariz/german_stopwords/blob/master/german_stopwords_full.txt)
[Countwordfree](https://countwordsfree.com/stopwords/german)
[Ranks](https://www.ranks.nl/stopwords/german)
[Tradloff](https://github.com/tradloff/haiku/blob/master/wsgi/static/nltk-corpus-stopwords-german.txt)

### Quellen der Blacklist
[fddb1](https://fddb.info/db/de/listen/261057_4_fleisch_im_vergleich/index.html)
[fddb2](https://fddb.info/db/de/listen/149538__01__vergleichsliste__fisch/index.html)
[fddb3](https://fddb.info/db/de/listen/150984__01__vergleichsliste__gemuese_i/index.html)
[fddb4](https://fddb.info/db/de/listen/151001__01__vergleichsliste__gemuese_ii/index.html)
[fddb5](https://fddb.info/db/de/listen/152634__01__vergleichsliste__scharf/index.html)
[fddb6](https://fddb.info/db/de/listen/442751_vergleichsliste_beilagen/index.html)
[fddb7](https://fddb.info/db/de/listen/155259__01__vergleichsliste__obst/index.html)
