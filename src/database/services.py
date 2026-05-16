"""
Database Service Layer
Handles all database operations for predictions and metrics.
"""

from src.database.db_config import SessionLocal
from src.database.models import PredictionRecord, ModelMetrics


class PredictionService:
    """Service for handling prediction storage and retrieval."""

    @staticmethod
    def save_prediction(
        age, gender, subscription_type, watch_hours, last_login_days,
        region, device, monthly_fee, payment_method, number_of_profiles,
        avg_watch_time_per_day, favorite_genre, prediction, prediction_status,
        prediction_probability, source="form", model_version="1.0", ip_address=None
    ):
        """
        Save a prediction record to the database.
        
        Args:
            All customer input fields
            prediction: 0 or 1 (binary)
            prediction_status: "Churned" or "Not Churned"
            prediction_probability: float between 0 and 1
            source: "form" or "api"
            model_version: version of the model used
            ip_address: client IP for audit trail
            
        Returns:
            PredictionRecord object with id
        """
        db = SessionLocal()
        try:
            prediction_record = PredictionRecord(
                age=age,
                gender=gender,
                subscription_type=subscription_type,
                watch_hours=watch_hours,
                last_login_days=last_login_days,
                region=region,
                device=device,
                monthly_fee=monthly_fee,
                payment_method=payment_method,
                number_of_profiles=number_of_profiles,
                avg_watch_time_per_day=avg_watch_time_per_day,
                favorite_genre=favorite_genre,
                prediction=prediction,
                prediction_status=prediction_status,
                prediction_probability=prediction_probability,
                source=source,
                model_version=model_version,
                ip_address=ip_address,
            )
            db.add(prediction_record)
            db.commit()
            db.refresh(prediction_record)
            return prediction_record
        except Exception as e:
            db.rollback()
            print(f"Error saving prediction: {e}")
            raise
        finally:
            db.close()

    @staticmethod
    def get_prediction_by_id(prediction_id):
        """Retrieve a specific prediction by ID."""
        db = SessionLocal()
        try:
            return db.query(PredictionRecord).filter(
                PredictionRecord.id == prediction_id
            ).first()
        finally:
            db.close()

    @staticmethod
    def get_all_predictions(limit=100, offset=0):
        """Retrieve all predictions with pagination."""
        db = SessionLocal()
        try:
            return db.query(PredictionRecord).order_by(
                PredictionRecord.created_at.desc()
            ).offset(offset).limit(limit).all()
        finally:
            db.close()

    @staticmethod
    def get_predictions_by_status(status, limit=100):
        """Get predictions filtered by churn status."""
        db = SessionLocal()
        try:
            return db.query(PredictionRecord).filter(
                PredictionRecord.prediction_status == status
            ).order_by(
                PredictionRecord.created_at.desc()
            ).limit(limit).all()
        finally:
            db.close()

    @staticmethod
    def get_churn_rate():
        """Calculate churn rate from stored predictions."""
        db = SessionLocal()
        try:
            total = db.query(PredictionRecord).count()
            if total == 0:
                return 0.0
            
            churned = db.query(PredictionRecord).filter(
                PredictionRecord.prediction == 1
            ).count()
            
            return (churned / total) * 100
        finally:
            db.close()

    @staticmethod
    def get_prediction_stats():
        """Get stored prediction counts for dashboard display."""
        db = SessionLocal()
        try:
            total = db.query(PredictionRecord).count()
            churned = db.query(PredictionRecord).filter(PredictionRecord.prediction == 1).count()
            not_churned = max(total - churned, 0)
            return {
                'total_predictions': total,
                'churned_predictions': churned,
                'not_churned_predictions': not_churned,
                'records_ready_for_retraining': total,
            }
        finally:
            db.close()


class MetricsService:
    """Service for handling model metrics storage."""

    @staticmethod
    def save_metrics(model_version, accuracy, precision, recall, f1_score, auc_score, total_predictions=None):
        """Save model performance metrics."""
        db = SessionLocal()
        try:
            metrics = ModelMetrics(
                model_version=model_version,
                accuracy=accuracy,
                precision=precision,
                recall=recall,
                f1_score=f1_score,
                auc_score=auc_score,
                total_predictions=total_predictions if total_predictions is not None else 0,
            )
            db.add(metrics)
            db.commit()
            db.refresh(metrics)
            return metrics
        except Exception as e:
            db.rollback()
            print(f"Error saving metrics: {e}")
            raise
        finally:
            db.close()

    @staticmethod
    def get_latest_metrics(model_version=None):
        """Get the latest metrics (optionally for a specific model version)."""
        db = SessionLocal()
        try:
            query = db.query(ModelMetrics).order_by(
                ModelMetrics.created_at.desc()
            )
            if model_version:
                query = query.filter(ModelMetrics.model_version == model_version)
            return query.first()
        finally:
            db.close()

    @staticmethod
    def get_metrics_history(model_version=None, limit=10):
        """Get historical metrics for monitoring."""
        db = SessionLocal()
        try:
            query = db.query(ModelMetrics).order_by(
                ModelMetrics.created_at.desc()
            )
            if model_version:
                query = query.filter(ModelMetrics.model_version == model_version)
            return query.limit(limit).all()
        finally:
            db.close()

    @staticmethod
    def get_dashboard_stats():
        """Get combined dashboard stats for frontend display."""
        db = SessionLocal()
        try:
            latest_metrics = db.query(ModelMetrics).order_by(ModelMetrics.created_at.desc()).first()
            metrics_count = db.query(ModelMetrics).count()
            prediction_stats = PredictionService.get_prediction_stats()

            return {
                **prediction_stats,
                'retrain_runs': metrics_count,
                'latest_retrain_at': latest_metrics.created_at.isoformat() if latest_metrics and latest_metrics.created_at else None,
                'latest_model_version': latest_metrics.model_version if latest_metrics else None,
                'latest_training_sample_size': latest_metrics.total_predictions if latest_metrics and latest_metrics.total_predictions else prediction_stats['total_predictions'],
                'latest_metrics': {
                    'accuracy': latest_metrics.accuracy if latest_metrics else None,
                    'precision': latest_metrics.precision if latest_metrics else None,
                    'recall': latest_metrics.recall if latest_metrics else None,
                    'f1_score': latest_metrics.f1_score if latest_metrics else None,
                    'auc_score': latest_metrics.auc_score if latest_metrics else None,
                } if latest_metrics else None,
            }
        finally:
            db.close()


class DashboardService:
    """Service for dashboard-level aggregated statistics."""

    @staticmethod
    def get_dashboard_stats():
        return MetricsService.get_dashboard_stats()
