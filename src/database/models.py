from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON
from src.database.db_config import Base


class PredictionRecord(Base):
    """
    SQLAlchemy model to store customer predictions and input data.
    
    Every prediction (form-based or API) will create a record here.
    This enables:
    - Historical tracking of predictions
    - Data for retraining
    - Audit trail
    """
    __tablename__ = "prediction_records"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Customer Input Data
    age = Column(Integer)
    gender = Column(String(50))
    subscription_type = Column(String(100))
    watch_hours = Column(Float)
    last_login_days = Column(Integer)
    region = Column(String(100))
    device = Column(String(100))
    monthly_fee = Column(Float)
    payment_method = Column(String(100))
    number_of_profiles = Column(Integer)
    avg_watch_time_per_day = Column(Float)
    favorite_genre = Column(String(100))

    # Prediction Results
    prediction = Column(Integer)  # 0 = Not Churned, 1 = Churned
    prediction_status = Column(String(20))  # "Churned" or "Not Churned"
    prediction_probability = Column(Float)  # Confidence score

    # Metadata
    model_version = Column(String(50), default="1.0")  # Track which model version was used
    source = Column(String(50), default="form")  # "form" or "api"
    ip_address = Column(String(50), nullable=True)

    def __repr__(self):
        return f"<PredictionRecord(id={self.id}, prediction={self.prediction_status}, created_at={self.created_at})>"

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'age': self.age,
            'gender': self.gender,
            'subscription_type': self.subscription_type,
            'watch_hours': self.watch_hours,
            'last_login_days': self.last_login_days,
            'region': self.region,
            'device': self.device,
            'monthly_fee': self.monthly_fee,
            'payment_method': self.payment_method,
            'number_of_profiles': self.number_of_profiles,
            'avg_watch_time_per_day': self.avg_watch_time_per_day,
            'favorite_genre': self.favorite_genre,
            'prediction': self.prediction,
            'prediction_status': self.prediction_status,
            'prediction_probability': self.prediction_probability,
            'model_version': self.model_version,
            'source': self.source,
        }


class ModelMetrics(Base):
    """
    Store model performance metrics over time.
    Useful for monitoring model drift and performance.
    """
    __tablename__ = "model_metrics"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    model_version = Column(String(50))
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    auc_score = Column(Float)
    total_predictions = Column(Integer, default=0)

    def __repr__(self):
        return f"<ModelMetrics(version={self.model_version}, f1={self.f1_score})>"
