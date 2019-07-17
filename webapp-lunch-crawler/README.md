# Lunch-Crawler Webapp
## Voraussetzungen:
- Docker
- Node.js
- npm
- Webbrowser (getestet mit Mozilla Firefox)

## Ablauf der Installation:
1. Das [Github-Repository](https://github.com/s-santoro/lunch-crawler) herunterladen
2. Docker-Image von Elasticsearch herunterladen: docker pull docker.elastic.co/elasticsearch/elasticsearch:7.0.1
3. Docker-Container starten: docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.0.1
4. Das [Zipfile mit den Daten für Elasticsearch](https://github.com/s-santoro/lunch-crawler/blob/master/webapp-lunch-crawler/run_webapp/data_for_elasticsearch.zip) entpacken
5. Das [Script zum Hinzufügen dieser Daten zu Elasticsearch](https://github.com/s-santoro/lunch-crawler/blob/master/webapp-lunch-crawler/run_webapp/add_to_elasticSearch.sh) ausführen
6. In den Ordner "lunch-crawler/webapp-lunch-crawler" wechseln
7. Den folgenden Befehl ausführen: npm init
8. Den folgenden Befehl ausführen: npm install
9. Den folgenden Befehl ausführen: npm start

## Benutzung der Webapplikation
1. Gewünschtes Gericht im Suchfeld eingeben
2. Standortabfrage zulassen
3. Ergebnisse betrachten (falls kein Ergebnis angezeigt wird, muss manuell herausgezoomt werden)
