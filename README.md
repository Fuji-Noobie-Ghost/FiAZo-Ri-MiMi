# PoketraFinday

# **Rapport de Projet \- PoketraFinday**

### **1\. Informations sur le Groupe**
#### Membre 1 : 
* nom : ANDRIAMANALINA 
* prénom(s) : Rita Harenah
* classe : ESIIA 5
* numéro : 05
* rôle : *Préparation du slide*

#### Membre 2 : 
* nom : RAKOTONOELINA 
* prénom(s) : Lala Minoniaina Joannah
* classe : ESIIA 5
* numéro : 09
* rôle : *Conception du Readme.md*

#### Membre 3 : 
* nom : RAKOTONJANAHARY
* prénom(s) : Miora Irinah
* classe : ESIIA 5
* numéro : 10
* rôle : *Préparation slide*

#### Membre 4 : 
* nom : RATOVONARIVO
* prénom(s) : Zo Michaël 
* classe : ESIIA 5
* numéro : 15
* rôle : *(développeur, analyste, présentateur, ...)*

#### Membre 5 : 
* nom : ANDRIAMIHAJA
* prénom(s) : Alan Steven
* classe : ESIIA 5
* numéro : 16
* rôle : *Analyse de données*

#### Membre 6 : 
* nom : RATIA ANDRIAFITAHIANA
* prénom(s) : Joseph Tellia
* classe : ESIIA 5
* numéro : 19
* rôle : *(développeur, analyste, présentateur, ...)*

### **2\. Résumé du Travail**

Problématique :  
Le problème de sécurité détecté chez PoketraFinday est une recrudescence de fraudes qui menacent la plateforme.
Le cœur du problème réside dans l'augmentation d'attaques plus ou moins sophistiquées, incluant :
Des vols de comptes nocturnes, de l'ingénierie sociale ciblant les seniors.
Il est critique de résoudre ce problème pour les raisons suivantes :
- Confiance et Réputation (Mission Critique);
- Impact Opérationnel et Développement 

### **Méthodologie Adoptée :**
#### **EDA et Préparation Initiale ** 
###### Structure du Dataset
- Le jeu de données d'entraînement est volumineux, avec plusieurs millions d'observations et 7 colonnes initiales.
- Aucune valeur manquante (NaN) n'a été détectée dans les colonnes fournies.
- Les colonnes transaction_id et customer_id ont été identifiées comme des identifiants non prédictifs et ont été mises de côté/supprimées pour la modélisation.

###### Analyse de la Cible (is_fraud)
- Déséquilibre Extrême : Nous avons confirmé un déséquilibre de classe extrême (Imbalanced Data). Le pourcentage de transactions frauduleuses (is_fraud = 1) est très faible (généralement moins de 0.2% du total).
- Conséquence : L'évaluation du modèle doit impérativement se faire sur le F1-Score, car l'exactitude (Accuracy) serait trompeuse.

###### Analyse des Variables Catégorielles (type)
- Variables Clés : La variable type est l'un des prédicteurs les plus puissants.
- Concentration de la Fraude : La fraude est quasi-exclusivement concentrée sur deux types de transactions:
  - TRANSFER
  - CASH_OUT
Les types PAYMENT et DEBIT présentent un taux de fraude négligeable ou nul.

###### Analyse Temporelle (step)
En utilisant l'indice crucial que Step 1 est la première heure d'un LUNDI, nous avons créé deux nouvelles caractéristiques (features) :
- hour (Heure de la journée) : L'analyse du taux de fraude par heure révèle que les transactions frauduleuses ne sont pas uniformes. Elles sont souvent concentrées sur des plages spécifiques, notamment les heures nocturnes (confirmant l'indice sur les "vols de comptes nocturnes" ) ou en dehors des heures de bureau.
- day_of_week (Jour de la semaine) : Le taux de fraude présente des variations importantes selon le jour, ce qui peut indiquer des schémas d'attaque spécifiques à la semaine ou au week-end.

###### Préparation des Données pour la Modélisation
Le jeu de données a été préparé comme suit :
- Suppression des identifiants (transaction_id, customer_id) et de la variable source (step).
- Feature Engineering : Ajout des variables hour et day_of_week.
- Encodage Catégoriel : Application du One-Hot Encoding aux variables type, hour et day_of_week pour les rendre utilisables par la Régression Logistique.
