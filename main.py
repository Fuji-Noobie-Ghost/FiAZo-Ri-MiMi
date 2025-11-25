import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, Optional
from dataclasses import dataclass

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, classification_report, confusion_matrix

import warnings
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)


@dataclass
class ModelConfig:
    """Configuration pour l'entraînement du modèle"""
    test_size: float = 0.2
    random_state: int = 42
    rf_n_estimators: int = 100
    logistic_max_iter: int = 1000
    

class DataLoader:
    """Gestion du chargement des données"""
    
    @staticmethod
    def load_data(train_path: str = 'resources/train.csv', 
                  test_path: str = 'resources/test.csv') -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Charge les datasets d'entraînement et de test"""
        try:
            df_train = pd.read_csv(train_path)
            df_test = pd.read_csv(test_path)
            print(f"Train set chargé: {df_train.shape}")
            print(f"Test set chargé: {df_test.shape}")
            return df_train, df_test
        except FileNotFoundError as e:
            print("ERREUR: Les fichiers CSV doivent être dans le dossier 'resources/'")
            raise e


class FeatureEngine:
    """Gestion de l'ingénierie des features et du prétraitement des données"""
    
    @staticmethod
    def process_data(df: pd.DataFrame, is_train: bool = True) -> pd.DataFrame:
        """
        Nettoie et prépare les données avec ingénierie des features temporelles.
        
        Args:
            df: Dataframe d'entrée
            is_train: Indique si ce sont des données d'entraînement (affecte les colonnes à supprimer)
            
        Returns:
            Dataframe traité avec les features créées
        """
        df_processed = df.copy()
        
        # Features temporelles - cruciales pour la détection de fraude
        df_processed['hour_of_day'] = df_processed['step'] % 24
        df_processed['day_of_week'] = (df_processed['step'] // 24) % 7
        
        # Suppression des colonnes inutiles
        cols_to_drop = ['customer_id']
        if is_train:
            cols_to_drop.append('transaction_id')
            
        df_processed = df_processed.drop(columns=cols_to_drop, errors='ignore')
        
        return df_processed
    
    @staticmethod
    def get_feature_lists() -> Tuple[list, list]:
        """Retourne les listes des features numériques et catégorielles"""
        numeric_features = ['step', 'amount', 'age', 'hour_of_day', 'day_of_week']
        categorical_features = ['type']
        return numeric_features, categorical_features


class EDA:
    """Utilitaires pour l'analyse exploratoire des données"""
    
    @staticmethod
    def analyze_fraud_distribution(df: pd.DataFrame, target_col: str = 'is_fraud'):
        """Analyse la distribution des fraudes dans le dataset"""
        fraud_ratio = df[target_col].mean()
        print(f"\nTaux de fraude dans le dataset: {fraud_ratio:.4%}")
        
        print("\nFraudes par type de transaction:")
        print(df[df[target_col] == 1]['type'].value_counts())
        
        return fraud_ratio


class FraudDetectionPipeline:
    """Pipeline principal pour l'entraînement et la prédiction du modèle de détection de fraude"""
    
    def __init__(self, config: Optional[ModelConfig] = None):
        self.config = config or ModelConfig()
        self.preprocessor = None
        self.baseline_model = None
        self.rf_model = None
        self.best_model = None
        self.best_model_name = None
        
    def create_preprocessor(self) -> ColumnTransformer:
        """Crée le pipeline de prétraitement des features"""
        numeric_features, categorical_features = FeatureEngine.get_feature_lists()
        
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numeric_features),
                ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
            ])
        
        return preprocessor
    
    def create_models(self) -> Tuple[Pipeline, Pipeline]:
        """Crée les pipelines des modèles baseline et avancé"""
        self.preprocessor = self.create_preprocessor()
        
        # Baseline: Régression Logistique
        baseline = Pipeline(steps=[
            ('preprocessor', self.preprocessor),
            ('classifier', LogisticRegression(
                class_weight='balanced',
                random_state=self.config.random_state,
                max_iter=self.config.logistic_max_iter
            ))
        ])
        
        # Avancé: Random Forest
        rf = Pipeline(steps=[
            ('preprocessor', self.preprocessor),
            ('classifier', RandomForestClassifier(
                n_estimators=self.config.rf_n_estimators,
                class_weight='balanced',
                random_state=self.config.random_state,
                n_jobs=-1
            ))
        ])
        
        return baseline, rf
    
    def train_and_evaluate(self, X: pd.DataFrame, y: pd.Series) -> dict:
        """
        Entraîne les deux modèles et sélectionne le meilleur.
        
        Returns:
            Dictionnaire avec les métriques d'évaluation
        """
        # Séparation des données
        X_train, X_val, y_train, y_val = train_test_split(
            X, y,
            test_size=self.config.test_size,
            stratify=y,
            random_state=self.config.random_state
        )
        
        # Création des modèles
        self.baseline_model, self.rf_model = self.create_models()
        
        # Entraînement et évaluation de la baseline
        print("\n--- ENTRAÎNEMENT BASELINE (RÉGRESSION LOGISTIQUE) ---")
        self.baseline_model.fit(X_train, y_train)
        y_pred_base = self.baseline_model.predict(X_val)
        f1_base = f1_score(y_val, y_pred_base)
        
        print(f"\nRapport Baseline:\n{classification_report(y_val, y_pred_base)}")
        print(f"-> F1-Score Baseline: {f1_base:.4f}")
        
        # Entraînement et évaluation Random Forest
        print("\n--- ENTRAÎNEMENT MODÈLE AVANCÉ (RANDOM FOREST) ---")
        self.rf_model.fit(X_train, y_train)
        y_pred_rf = self.rf_model.predict(X_val)
        f1_rf = f1_score(y_val, y_pred_rf)
        
        print(f"\nRapport Random Forest:\n{classification_report(y_val, y_pred_rf)}")
        print(f"-> F1-Score Random Forest: {f1_rf:.4f}")
        
        # Sélection du meilleur modèle
        if f1_rf > f1_base:
            print("\n>> Le Random Forest est meilleur. Il sera utilisé pour la soumission.")
            self.best_model = self.rf_model
            self.best_model_name = "Random Forest"
        else:
            print("\n>> La Baseline est meilleure. Elle sera utilisée pour la soumission.")
            self.best_model = self.baseline_model
            self.best_model_name = "Régression Logistique"
        
        return {
            'baseline_f1': f1_base,
            'rf_f1': f1_rf,
            'best_model': self.best_model_name,
            'best_f1': max(f1_base, f1_rf)
        }
    
    def retrain_on_full_data(self, X: pd.DataFrame, y: pd.Series):
        """Ré-entraîne le meilleur modèle sur l'ensemble complet des données d'entraînement"""
        print(f"\n--- RÉ-ENTRAÎNEMENT {self.best_model_name} SUR TOUT LE DATASET ---")
        self.best_model.fit(X, y)
        print("✓ Modèle ré-entraîné avec succès")
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Génère les prédictions avec le meilleur modèle"""
        if self.best_model is None:
            raise ValueError("Modèle non entraîné. Appelez train_and_evaluate d'abord.")
        return self.best_model.predict(X)
    
    def create_submission(self, predictions: np.ndarray, 
                         test_ids: pd.Series,
                         output_path: str = 'submission.csv'):
        """Crée et sauvegarde le fichier de soumission"""
        submission = pd.DataFrame({
            "transaction_id": test_ids,
            "is_fraud": predictions
        })
        submission.to_csv(output_path, index=False)
        print(f"\n✓ Succès! Le fichier '{output_path}' a été généré.")
        print(submission.head())
        return submission


def main():
    """Fonction principale d'exécution"""
    print("=" * 60)
    print("PIPELINE DE DÉTECTION DE FRAUDE")
    print("=" * 60)
    
    # Chargement des données
    print("\n--- CHARGEMENT DES DONNÉES ---")
    df_train, df_test = DataLoader.load_data()
    
    # Ingénierie des features
    print("\n--- FEATURE ENGINEERING ---")
    X_full_train = FeatureEngine.process_data(df_train, is_train=True)
    y = X_full_train['is_fraud']
    X = X_full_train.drop(columns=['is_fraud'])
    
    test_ids = df_test['transaction_id']
    X_test_final = FeatureEngine.process_data(df_test, is_train=False).drop(
        columns=['transaction_id']
    )
    
    print(f"Features utilisées pour l'entraînement: {X.columns.tolist()}")
    
    # Analyse exploratoire des données
    print("\n--- ANALYSE EXPLORATOIRE (EDA) ---")
    EDA.analyze_fraud_distribution(df_train)
    
    # Entraînement des modèles
    pipeline = FraudDetectionPipeline()
    metrics = pipeline.train_and_evaluate(X, y)
    
    # Ré-entraînement sur toutes les données
    pipeline.retrain_on_full_data(X, y)
    
    # Génération des prédictions
    print("\n--- GÉNÉRATION DU FICHIER SUBMISSION.CSV ---")
    predictions = pipeline.predict(X_test_final)
    submission = pipeline.create_submission(predictions, test_ids)
    
    print("\n" + "=" * 60)
    print("PIPELINE TERMINÉ AVEC SUCCÈS")
    print("=" * 60)
    print(f"\nMeilleur Modèle: {metrics['best_model']}")
    print(f"Meilleur F1-Score: {metrics['best_f1']:.4f}")


if __name__ == "__main__":
    main()

