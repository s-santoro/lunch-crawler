# lunch-crawler
## Einleitung
Dieses Repository ist im Zusammenhang mit einer Bachelorarbeit erstellt worden.
## Abstract
Ziel dieser Arbeit ist das Erstellen einer Suchmaschine, über welches sich Menüs und Speisen suchen lassen.
Die Grundlage einer solchen Suchmaschine sind Websites von Restaurants, welche relevante Speiseinformationen beinhalten.
Im Kontext dieser Bachelorarbeit wurde manuell ein Gold-Standard aus Restaurantseiten zusammengestellt.
Für die Erstellung des Gold-Standards wurde eigens ein Webcrawler implementiert, welcher eine Vielzahl von Restaurant-Links besucht und den Webseiteninhalt abspeichert.
Der erstellte Gold-Standard dient dazu, eine Klassifikation der Restaurantseiten anhand zwei verschiedener Ansätze durchzuführen und zu messen.
Die zwei Ansätze sind regelbasiertes Klassifizieren sowie das Klassifizieren mittels Machine-Learning.
Um die einzelnen Klassifikationen prüfen zu können, wurden in beiden Bereichen mehrere Experimente durchgeführt.
Im praktischen Teil der Arbeit wurde neben dem Webcrawler eine Webapplikation erarbeitet, welche die Suchmaschine den Benutzern zugänglich macht.

The aim of this work is to create a search engine, which searches for menus and meals.
The basis of this search engine are websites of restaurants, which contain relevant food information.
In the context of this bachelor thesis, a gold standard has been created manually from restaurant pages.
To get the data for this gold standard, a webcrawler was implemented, which visits a large number of restaurant links and saves the website content.
This gold standard is used to execute and measure a classification of the restaurant webpages using two different approaches.
The two approaches are rule-based classification and classifying by means of machine learning.
In order to measure both classification outcomes, several experiments were executed for both approaches.
In the practical part of the work, a web application was developed in addition to the web crawler, which makes the search engine accessible to users.

## Dateistruktur
### Webcrawler
- [Impementierung StormCrawler](https://github.com/s-santoro/lunch-crawler/tree/master/storm-crawler-master)
  - [Angepasste Komponenten](https://github.com/s-santoro/lunch-crawler/tree/master/storm-crawler-master/archetype/src/main/resources/archetype-resources/src/main/java/ntb/iks)
  - [Docker-Compose](https://github.com/s-santoro/lunch-crawler/tree/master/storm-cluster)
  
### Gold Standard
- [Gold Standard](https://github.com/s-santoro/lunch-crawler/tree/master/gold-standard)
- [Tool zum manuellen Labeln]()

### Klassifikationspipeline
- [Übersicht](https://github.com/s-santoro/lunch-crawler/tree/master/classification)
- [Code](https://github.com/s-santoro/lunch-crawler/tree/master/classification/scripts)
- [Konfigurationen](https://github.com/s-santoro/lunch-crawler/tree/master/classification/scripts/configs)
- Diverse Files
  - [Stoppwortliste](https://github.com/s-santoro/lunch-crawler/blob/master/classification/stopwords_no_umlaute.txt)
  - [Getränkeliste](https://github.com/s-santoro/lunch-crawler/blob/master/classification/beverage_list.txt)
  - [Blacklist](https://github.com/s-santoro/lunch-crawler/blob/master/classification/blacklist.txt)
  - [Whitelist](https://github.com/s-santoro/lunch-crawler/blob/master/classification/whitelist.txt)
  
### Produktive Pipeline
- [Pipeline zur Klassifikation der Rohdaten](https://github.com/s-santoro/lunch-crawler/tree/master/prod-pipeline/classification)
- [Script zur Standardisierung von Restaurantinformationen](https://github.com/s-santoro/lunch-crawler/blob/master/prod-pipeline/nodejs/standardize_data.js)
- [Script zur Analyse von Restaurantinformationen](https://github.com/s-santoro/lunch-crawler/blob/master/prod-pipeline/nodejs/analyze_data.js)

### Webapplikation
- [Webapp](https://github.com/s-santoro/lunch-crawler/tree/master/webapp-lunch-crawler)
- Frontend
  - [Scripts](https://github.com/s-santoro/lunch-crawler/tree/master/webapp-lunch-crawler/public/javascripts)
  - [HTML](https://github.com/s-santoro/lunch-crawler/tree/master/webapp-lunch-crawler/views)
- [Backend](https://github.com/s-santoro/lunch-crawler/blob/master/webapp-lunch-crawler/app.js)
  - [Routes](https://github.com/s-santoro/lunch-crawler/tree/master/webapp-lunch-crawler/routes)
  
## Informationen
Studenten:
- [Sandro Santoro](https://github.com/s-santoro)
- [Gian Brunner](https://github.com/gianbrunner)

Referenten:
- Corsin Capol
- Lukas Toggenburger

Schule:
[Interstaatlichen Hochschule für Technik Buchs](http://ntb.ch)

Studiengang:
[Systemtechnik](https://www.ntb.ch/studium/systemtechnik/)

Vertiefungsrichtung:
[Informations- und Kommunikationssysteme](https://www.ntb.ch/studium/systemtechnik/studienrichtungen/iks/)
