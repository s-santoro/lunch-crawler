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