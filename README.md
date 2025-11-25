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

# **Méthodologie Adoptée :**
## **EDA et Préparation Initiale ** 
Constats sur la Cible et le Déséquilibre
Déséquilibre Extrême : Le jeu de données présente un déséquilibre de classe extrême1. Le pourcentage de transactions frauduleuses ($is\_fraud = 1$) est très faible (typiquement moins de 0,2 % du total).Métrique Cible : En raison de ce déséquilibre, la métrique principale pour l'évaluation ne doit pas être l'exactitude (Accuracy), mais le F1-Score2. Le F1-Score est critique pour s'assurer que le modèle détecte effectivement les fraudes sans générer un nombre inacceptable de faux positifs (utilisateurs honnêtes bloqués)3.2. Variables Cléstype de Transaction : C'est la variable la plus discriminante.La fraude est presque exclusivement concentrée sur les transactions de type TRANSFER et CASH_OUT.Les transactions PAYMENT et DEBIT sont très rarement (voire jamais) frauduleuses.amount (Montant) : Les montants frauduleux montrent une distribution différente des montants légitimes, souvent avec des montants plus élevés et des schémas qui pourraient nécessiter une analyse plus poussée (montants ronds, montants maximaux).
