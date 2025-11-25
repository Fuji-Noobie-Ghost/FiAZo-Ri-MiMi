# =============================================================================
# TITRE : DETECTION DE FRAUDE - POKETRAFINDAY
# AUTEUR : Équipe FiAZo Ri MiMi
# CONTEXTE : Examen Final - Prédiction de la cible 'is_fraud'
# SLOGAN : Until we die
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, classification_report, confusion_matrix

import warnings
warnings.filterwarnings('ignore') # Pour garder la sortie propre
pd.set_option('display.max_columns', None)


print("--- CHARGEMENT DES DONNÉES ---")
try:
    df_train = pd.read_csv('resources/train.csv')
    df_test = pd.read_csv('resources/test.csv')
    print(f"Train set chargé : {df_train.shape}")
    print(f"Test set chargé : {df_test.shape}")
except FileNotFoundError:
    print("ERREUR : Les fichiers csv doivent être dans un dossier 'resources/'")
    raise


def process_data(df, is_train=True):
    """
    Fonction centralisée pour nettoyer et préparer les données (Train et Test).
    Applique l'indice du 'Lundi' sur la colonne 'step'.
    """
    df_processed = df.copy()
    
    """
    TRAITEMENT TEMPOREL (INDICE CRUCIAL)
        On transforme 'step' (heures totales) en features cycliques
        Heure de la journée (0-23h)
        Jour de la semaine (0=Lundi, 1=Mardi ... 6=Dimanche)
    """
    df_processed['hour_of_day'] = df_processed['step'] % 24
    df_processed['day_of_week'] = (df_processed['step'] // 24) % 7
    
    """
    SUPPRESSION DES COLONNES INUTILES
        'customer_id' a trop de valeurs uniques pour ce modèle
        'transaction_id' est inutile pour l'entraînement (c'est juste un ID)
    """
    cols_to_drop = ['customer_id']
    if is_train:
        cols_to_drop.append('transaction_id')
        
    df_processed = df_processed.drop(columns=cols_to_drop, errors='ignore')
    
    return df_processed

print("\n--- FEATURE ENGINEERING ---")

X_full_train = process_data(df_train, is_train=True)
y = X_full_train['is_fraud']
X = X_full_train.drop(columns=['is_fraud'])

# Préparation du TEST set (on garde transaction_id pour la soumission finale)
test_ids = df_test['transaction_id']
X_test_final = process_data(df_test, is_train=False).drop(columns=['transaction_id'])

print(f"Colonnes utilisées pour l'apprentissage : {X.columns.tolist()}")


print("\n--- ANALYSE EXPLORATOIRE (EDA) ---")

# Ratio de fraude
fraud_ratio = y.mean()
print(f"Taux de fraude dans le dataset : {fraud_ratio:.4%}")

# Analyse par type
print("Fraudes par type de transaction :")
print(df_train[df_train['is_fraud']==1]['type'].value_counts())

"""
PRÉPARATION DES PIPELINES (BASELINE & AVANCÉ)
Séparation Train / Validation (80% / 20%) pour évaluer nos modèles
"""
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

numeric_features = ['step', 'amount', 'age', 'hour_of_day', 'day_of_week']
categorical_features = ['type']

"""
Préprocesseur :
    Normalisation (StandardScaler) pour les données de type numérique
    Encodage (OneHot) pour les données de type string
"""
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

"""
BASELINE : RÉGRESSION LOGISTIQUE
class_weight='balanced' est vital car il y a peu de fraudes
"""
baseline_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(class_weight='balanced', random_state=42, max_iter=1000))
])

"""
MODÈLE AVANCÉ : RANDOM FOREST
n_estimators à 100 pour la rapidité et stabilité, suffisant pour notre cas
"""
rf_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, 
                                          class_weight='balanced', 
                                          random_state=42, 
                                          n_jobs=-1))
])

"""
ENTRAÎNEMENT ET ÉVALUATION
"""
print("\n--- ENTRAÎNEMENT BASELINE (LOGISTIC REGRESSION) ---")
baseline_pipeline.fit(X_train, y_train)
y_pred_base = baseline_pipeline.predict(X_val)
f1_base = f1_score(y_val, y_pred_base)

print(f"Rapport Baseline :\n{classification_report(y_val, y_pred_base)}")
print(f"-> F1-Score Baseline : {f1_base:.4f}")

print("\n--- ENTRAÎNEMENT MODÈLE AVANCÉ (RANDOM FOREST) ---")
rf_pipeline.fit(X_train, y_train)
y_pred_rf = rf_pipeline.predict(X_val)
f1_rf = f1_score(y_val, y_pred_rf)

print(f"Rapport Random Forest :\n{classification_report(y_val, y_pred_rf)}")
print(f"-> F1-Score Random Forest : {f1_rf:.4f}")

# Comparaison
if f1_rf > f1_base:
    print("\n>> Le Random Forest est meilleur. Il sera utilisé pour la soumission.")
    best_model = rf_pipeline
else:
    print("\n>> La Baseline est meilleure (surprenant !). Elle sera utilisée.")
    best_model = baseline_pipeline

"""
GÉNÉRATION DE LA SOUMISSION
    On ré-entraîne le meilleur modèle sur TOUT le jeu de données Train (Train + Val)
    Cela permet de maximiser l'information apprise
"""
print("\n--- GÉNÉRATION DU FICHIER SUBMISSION.CSV ---")

best_model.fit(X, y)

final_predictions = best_model.predict(X_test_final)

"""
Création et sauvegarde du DataFrame final
"""
submission = pd.DataFrame({
    "transaction_id": test_ids,
    "is_fraud": final_predictions
})
submission.to_csv("submission.csv", index=False)

print("✅ Succès ! Le fichier 'submission.csv' a été généré.")
print(submission.head())