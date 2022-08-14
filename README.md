# Analyzing tweets

Dieses Repository enthält die Codes, die für die Sammeln/Erstellung/Verarbeitung der Daten geschrieben wurden.

## Ordner "analyzer"
Im Ordner "analyzer" sind die Konfigurationsfiles für Elasticsearch zu finden.

## Ordner "forLogstash"
Hier gibt es ein Python-Code, der die gesammelten Tweetsdaten in CSV-Format in eine für Logstash konforme Format umschreibt.
Die Datei "uploadTweet.conf" steht für die Konfiguration von Logstash

## Ordner "models"
Hier sind Word2Vec-Modelle, die aus Twitter-Corpus mit Hilfe von Gensim erstellt worden sind



