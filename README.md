# PoketraFinday

# **Rapport de Projet \- PoketraFinday**

### **1\. Informations sur le Groupe**
#### Membre 1 : 
* nom : ANDRIAMANALINA 
* prénom(s) : Rita Harenah
* classe : ESIIA 5
* numéro : 05
* rôle : *Préparation de la présentation*

#### Membre 2 : 
* nom : RAKOTONOELINA 
* prénom(s) : Lala Minoniaina Joannah
* classe : ESIIA 5
* numéro : 09
* rôle : *Rédaction du documentation*

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
* rôle : *Développeur*

#### Membre 5 : 
* nom : ANDRIAMIHAJA
* prénom(s) : Alan Steven
* classe : ESIIA 5
* numéro : 16
* rôle : *Analyste*

#### Membre 6 : 
* nom : RATIA ANDRIAFITAHIANA
* prénom(s) : Joseph Tellia
* classe : ESIIA 5
* numéro : 19
* rôle : *Développeur*

### **2\. Résumé du Travail**

Problématique :  
Le problème de sécurité détecté chez PoketraFinday est une recrudescence de fraudes qui menacent la plateforme.
Le cœur du problème réside dans l'augmentation d'attaques plus ou moins sophistiquées, incluant :
Des vols de comptes nocturnes, de l'ingénierie sociale ciblant les seniors.
Il est critique de résoudre ce problème pour les raisons suivantes :
- Confiance et Réputation (Mission Critique);
- Impact Opérationnel et Développement 

### **Méthodologie Adoptée :**
#### EDA et Préparation Initiale 
###### Structure du Dataset
- Le jeu de données d'entraînement est volumineux, avec plusieurs millions d'observations et 7 colonnes initiales.
- Aucune valeur manquante (NaN) n'a été détectée dans les colonnes fournies.
- Les colonnes transaction_id et customer_id ont été identifiées comme des identifiants non prédictifs et ont été mises de côté/supprimées pour la modélisation.

##### 1. Pré-traitement Spécifique (Feature Engineering)
Le cœur du pré-traitement réside dans l'exploitation de la variable temporelle step (nombre d'heures totales) :
- Caractéristiques Temporelles Cycliques : La colonne step est transformée en deux variables plus pertinentes :
  - hour_of_day ( step  (mod 24) ) : L'heure spécifique à laquelle la transaction a eu lieu (0 à 23).
  - day_of_week ( ([ step / 24 ])  (mod 7) ) : Le jour de la semaine (0=Lundi à 6=Dimanche).
  - Importance : Cette transformation introduit une information comportementale essentielle, car la fraude suit souvent des schémas temporels (ex: nuit, week-end).
- Nettoyage : Les colonnes customer_id (trop de valeurs uniques) et transaction_id (simple identifiant) sont exclues du modèle d'entraînement.

##### 2. Choix du Préprocesseur (Pipeline ColumnTransformer)
Un ColumnTransformer est utilisé pour appliquer des transformations différentes aux types de variables :
- Caractéristiques Numériques (step, amount, age, hour_of_day, day_of_week) : Application d'un StandardScaler pour centrer et réduire les données. Cela est nécessaire, surtout pour la Régression Logistique, afin que les différentes échelles de valeurs (ex: amount vs day_of_week) ne biaisent pas le modèle.
- Caractéristiques Catégorielles (type) : Application d'un OneHotEncoder pour transformer les catégories (ex: 'CASH_OUT', 'TRANSFER') en variables binaires numériques, utilisables par le modèle.
  
##### 3. Choix des Modèles
Deux modèles sont comparés dans une stratégie de baseline vs. modèle avancé :
- Baseline : LogisticRegression (Régression Logistique). C'est un modèle linéaire simple, rapide à entraîner et souvent utilisé comme point de référence minimal.
- Modèle Avancé : RandomForestClassifier (Forêt Aléatoire). C'est un modèle ensembliste non linéaire, robuste, et généralement plus performant pour capturer les relations complexes dans les données.
•	Stratégie Anti-Déséquilibre : Les deux modèles utilisent class_weight='balanced'. Ceci ajuste implicitement les poids des classes pendant l'entraînement, donnant un poids plus important aux rares transactions frauduleuses pour éviter qu'elles ne soient ignorées.

##### 4. Stratégie de Validation
- Séparation des Données : Le jeu d'entraînement complet (X, y) est divisé en 80% Entraînement (X_train) et 20% Validation (X_val) en utilisant train_test_split.
- Stratification : L'argument stratify=y est utilisé. Cela garantit que la proportion de fraudes (classe 1) dans le jeu de validation est la même que dans le jeu d'entraînement, ce qui est crucial dans un contexte de déséquilibre.
-	Métrique d'Évaluation : Le F1-Score est la métrique principale pour comparer les modèles.
o	Le F1-Score est la moyenne harmonique de la Précision (des fraudes prédites, quelle proportion est réelle ?) et du Rappel (des fraudes réelles, quelle proportion est détectée ?). Il est préférable à la simple précision pour les jeux de données déséquilibrés.

