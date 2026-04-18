from functools import lru_cache
from pathlib import Path

import pandas as pd
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


@lru_cache(maxsize=1)
def get_model_comparison_metrics():
    root_dir = Path(__file__).resolve().parents[2]
    candidate_paths = [
        root_dir / 'data' / 'netflix_customer_churn.csv',
        root_dir / 'notebook' / 'data' / 'netflix_customer_churn.csv',
    ]

    dataset_path = next((path for path in candidate_paths if path.exists()), None)
    if dataset_path is None:
        raise FileNotFoundError('netflix_customer_churn.csv not found in expected data directories.')

    df = pd.read_csv(dataset_path)
    df = df.drop(columns=['customer_id'], errors='ignore')

    x = df.drop(columns=['churned'])
    y = df['churned']

    xtrain, xtest, ytrain, ytest = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    xtrain_encoded = pd.get_dummies(xtrain, drop_first=False)
    xtest_encoded = pd.get_dummies(xtest, drop_first=False)
    xtrain_encoded, xtest_encoded = xtrain_encoded.align(xtest_encoded, join='left', axis=1, fill_value=0)

    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000),
        'K-Neighbors Classifier': KNeighborsClassifier(),
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'Random Forest': RandomForestClassifier(random_state=42),
        'SVC': SVC(probability=True),
        'Gradient Boosting': GradientBoostingClassifier(random_state=42),
        'AdaBoost': AdaBoostClassifier(random_state=42),
    }

    results = []
    for model_name, model in models.items():
        model.fit(xtrain_encoded, ytrain)
        ypred = model.predict(xtest_encoded)

        results.append(
            {
                'model': model_name,
                'accuracy': float(accuracy_score(ytest, ypred)),
                'f1_score': float(f1_score(ytest, ypred, zero_division=0)),
            }
        )

    results.sort(key=lambda item: item['f1_score'], reverse=True)
    best_model = results[0]['model'] if results else None

    return {
        'results': results,
        'best_model': best_model,
    }
