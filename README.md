## Prédiction de consommation électrique à partir de séries temporelles

Ce projet vise à utiliser les techniques du Machine Learning pour prédire la consommation électrique espagnole à partir d'observations sur les années précédentes. Il s'appuie sur des données horaires[^first] sur les années 2014 à 2023 mises à disposition par l'opérateur espagnol Red Eléctrica[^second].

Démarche du projet :
1) Choix méthodologiques adaptés au traitement de séries temporelles
2) Acquisition des données (mise à jour via l'API publique[^third] de Red Eléctrica) 
3) Exploration des données
4) Nettoyage et transformation des données
5) Modélisation (cf. Choix du projet)
6) Développement et hébergement d'une Web App.[^fourth] pour la fourniture de prédictions de consommation électrique
7) Observations et conclusion.

Choix du projet :
+ Valeur à prédire : consommation totale en Espagne continentale
+ Méthodologie pour la modélisation : vérifications de saisonnalité et stationnarité, modélisation ARMA et LSTM
+ Développement logiciel :
  + Exploration des données avec R et Python
  + Acquisition des données avec Python
  + Web App. avec Python et Dash (serveur Apache)
+ Données d'entraînement et de validation : période du 1er janvier 2014 au 30 avril 2020
+ Données de test : période du 1er janvier 2021 au 31 décembre 2023.

[^first]: Electricity demand tracking | Red Eléctrica : https://demanda.ree.es/visiona/home
[^second]: Red Eléctrica : https://www.ree.es/en
[^third]: REData API | Red Eléctrica : https://www.ree.es/en/apidatos
[^fourth]: Fil Rouge | ELO : https://fil-rouge.cerfs21.fr