import os
from datetime import datetime

import pandas as pd
from sklearn.model_selection import train_test_split

from src.database.db_config import SessionLocal
from src.database.models import PredictionRecord
from src.database.services import MetricsService
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.logger import logging


def _build_training_frame(records):
    data = []
    for record in records:
        data.append(
            {
                'customer_id': record.id,
                'age': record.age,
                'gender': record.gender,
                'subscription_type': record.subscription_type,
                'watch_hours': record.watch_hours,
                'last_login_days': record.last_login_days,
                'region': record.region,
                'device': record.device,
                'monthly_fee': record.monthly_fee,
                'payment_method': record.payment_method,
                'number_of_profiles': record.number_of_profiles,
                'avg_watch_time_per_day': record.avg_watch_time_per_day,
                'favorite_genre': record.favorite_genre,
                'churned': record.prediction,
            }
        )
    return pd.DataFrame(data)


def retrain_from_db(min_records=25, model_version='1.0'):
    """
    Retrain the model using data stored in the prediction_records table.
    Returns a status dictionary for API responses.
    """
    db = SessionLocal()
    try:
        records = db.query(PredictionRecord).order_by(PredictionRecord.created_at.asc()).all()
    finally:
        db.close()

    if not records:
        return {
            'status': 'skipped',
            'reason': 'No prediction records found.',
            'records_available': 0,
        }

    if len(records) < min_records:
        return {
            'status': 'skipped',
            'reason': f'Need at least {min_records} records to retrain.',
            'records_available': len(records),
        }

    df = _build_training_frame(records)
    if df.empty:
        return {
            'status': 'skipped',
            'reason': 'No usable training rows built from stored predictions.',
            'records_available': len(records),
        }

    if df['churned'].nunique() < 2:
        return {
            'status': 'skipped',
            'reason': 'Need at least two churn classes to retrain.',
            'records_available': len(records),
        }

    os.makedirs('artifacts', exist_ok=True)
    train_df, test_df = train_test_split(
        df,
        test_size=0.2,
        random_state=42,
        stratify=df['churned'],
    )

    train_path = os.path.join('artifacts', 'retrain_train.csv')
    test_path = os.path.join('artifacts', 'retrain_test.csv')

    train_df.to_csv(train_path, index=False, header=True)
    test_df.to_csv(test_path, index=False, header=True)

    transformation = DataTransformation()
    train_arr, test_arr, _ = transformation.initate_data_transformation(train_path, test_path)

    trainer = ModelTrainer()
    accuracy, precision, recall, f1 = trainer.initate_model_training(train_arr, test_arr)

    MetricsService.save_metrics(
        model_version=model_version,
        accuracy=accuracy,
        precision=precision,
        recall=recall,
        f1_score=f1,
        auc_score=None,
        total_predictions=len(df),
    )

    logging.info(
        'Retraining completed. Records used=%s, Accuracy=%s, Precision=%s, Recall=%s, F1=%s',
        len(df),
        accuracy,
        precision,
        recall,
        f1,
    )

    return {
        'status': 'success',
        'records_used': len(df),
        'model_version': model_version,
        'trained_at': datetime.utcnow().isoformat(),
        'metrics': {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
        },
    }
