# Prédictions de consommation électrique à partir de séries temporelles

Ce projet vise à utiliser les techniques du Machine Learning pour prédire la consommation électrique sur une année à partir des observations des années précédentes. Il est basé sur des données[^first] sur les années 2014 à 2022 mises à disposition par l'opérateur espagnol Red Eléctrica[^second].

Il s'appuie sur la démarche suivante:
1) Transformation des données.
2) Sélection des jeux d'entraînement, validation et test, la période test retenue s'étendant du 1er janvier 2021 au 30 avril 2022.
3) Mise en oeuvre de modèles simples pour la production d'une base line.
4) Mise en oeuvre de modèles plus élaborés, en particulier des réseaux de neurones
5) Observations et conclusion.

[^first]: DeepSolar Dataset | Kaggle: https://demanda.ree.es/visiona/home
[^second]: Red Eléctrica: https://www.ree.es/en