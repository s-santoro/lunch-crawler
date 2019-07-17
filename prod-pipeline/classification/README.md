# Production Pipeline
## Starten der Production Pipeline
Zuerst müssen die Webpages in den neu-angelegten Ordner "./input" kopiert werden.
Danach müssen die Pickle-Files in den neu-angelegten Ordner "./pickled_files/" kopiert werden.
Anschliessend kann mit dem Befehl `./start_pipeline.sh` die Pipeline gestartet werden.
## Ablauf Production Pipeline
Die Production Pipeline liest alle Webpages vom Ordner "./input" in den Speicher.
Anschliessend wird das Preprocessing entsprechend dem Konfigurationsfile im Ordner "./config/" durchgeführt.
Schlussendlich werden die Webpages klassifiziert und in den passenden Ordner "./output/menu" oder "./output/no_menu" abgelegt.