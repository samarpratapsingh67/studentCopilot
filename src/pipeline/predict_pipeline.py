import sys
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from src.utils import load_object

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            preprocessor_path = 'artifacts/preprocessor.pkl'
            model_path = 'artifacts/model.pkl'
            preprocessor = load_object(file_path=preprocessor_path)
            model = load_object(file_path=model_path)
            data_scaled = preprocessor.transform(features)
            pred = model.predict(data_scaled)
            probability = None

            if hasattr(model, 'predict_proba'):
                probability = float(model.predict_proba(data_scaled)[0][1])

            return {
                'prediction': int(pred[0]),
                'probability': probability,
            }
        except Exception as e:
            logging.info('Exception occured in prediction pipeline')
            raise CustomException(e,sys)
        

class CustomData:
    def __init__(self,
                 age: int,
                 gender: str,
                 subscription_type: str,
                 watch_hours: float,
                 last_login_days: int,
                 region: str,
                 device: str,
                 monthly_fee: float,
                 payment_method: str,
                 number_of_profiles: int,
                 avg_watch_time_per_day: float,
                 favorite_genre: str):
        
        self.age = age
        self.gender = gender
        self.subscription_type = subscription_type
        self.watch_hours = watch_hours
        self.last_login_days = last_login_days
        self.region = region
        self.device = device
        self.monthly_fee = monthly_fee
        self.payment_method = payment_method
        self.number_of_profiles = number_of_profiles
        self.avg_watch_time_per_day = avg_watch_time_per_day
        self.favorite_genre = favorite_genre

    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                'age': [self.age],
                'gender': [self.gender],
                'subscription_type': [self.subscription_type],
                'watch_hours': [self.watch_hours],
                'last_login_days': [self.last_login_days],
                'region': [self.region],
                'device': [self.device],
                'monthly_fee': [self.monthly_fee],
                'payment_method': [self.payment_method],
                'number_of_profiles': [self.number_of_profiles],
                'avg_watch_time_per_day': [self.avg_watch_time_per_day],
                'favorite_genre': [self.favorite_genre]
            }
            df = pd.DataFrame(custom_data_input_dict)
            logging.info('Dataframe Gathered')
            return df
        except Exception as e:
            logging.info('Exception Occured in prediction pipeline')
            raise CustomException(e,sys)
