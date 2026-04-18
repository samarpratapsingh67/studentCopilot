# Basic Import
import numpy as np
import pandas as pd

# Modelling
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object
from src.utils import evaluate_models
from src.utils import print_evaluated_results
from src.utils import model_metrics

from dataclasses import dataclass
import sys
import os

@dataclass 
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    
    def initate_model_training(self,train_array,test_array):
        try:
            logging.info('Splitting Dependent and Independent variables from train and test data')
            xtrain, ytrain, xtest, ytest = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )
            
            models = {
                "Logistic Regression": LogisticRegression(max_iter=1000),
                "K-Neighbors Classifier": KNeighborsClassifier(),
                "Decision Tree": DecisionTreeClassifier(),
                "Random Forest Classifier": RandomForestClassifier(random_state=42),
                "SVC": SVC(probability=True),
                "GradientBoosting Classifier": GradientBoostingClassifier(),
                "AdaBoost Classifier": AdaBoostClassifier()
            }

            model_report:dict = evaluate_models(xtrain,ytrain,xtest,ytest,models)

            print(model_report)
            print('\n====================================================================================\n')
            logging.info(f'Model Report : {model_report}')
            # To get best model score from dictionary 
            best_model_score = max(model_report.values())

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            if best_model_score < 0.6 :
                logging.info('Best model has f1 Score less than 60%')
                raise CustomException('No Best Model Found')
            
            print(f'Best Model Found , Model Name : {best_model_name} , F1 Score : {best_model_score}')
            print('\n====================================================================================\n')
            logging.info(f'Best Model Found , Model Name : {best_model_name} , F1 Score : {best_model_score}')
            logging.info('Hyperparameter tuning started for random forest')

            # Hyperparameter tuning on Random Forest
            rfc = RandomForestClassifier(random_state=42)

            # Creating the hyperparameter grid
            param_dist = {
                'n_estimators': [100, 200, 300, 400],
                'max_depth': [None, 5, 10, 15, 20],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            }

            #Instantiate RandomSearchCV object
            rscv = RandomizedSearchCV(rfc , param_dist, scoring='f1', cv =5, n_jobs=-1, random_state=42)

            # Fit the model
            rscv.fit(xtrain, ytrain)

            # Print the tuned parameters and score
            print(f'Best Random Forest parameters : {rscv.best_params_}')
            print(f'Best Random Forest Score : {rscv.best_score_}')
            print('\n====================================================================================\n')

            best_rfc = rscv.best_estimator_

            logging.info('Hyperparameter tuning complete for Random Forest')

            logging.info('Hyperparameter tuning started for KNN')

            # Initialize knn
            knn = KNeighborsClassifier()

            # parameters
            k_range = list(range(2, 31))
            param_grid = dict(n_neighbors=k_range)

            # Fitting the cvmodel
            grid = GridSearchCV(knn, param_grid, cv=5, scoring='f1',n_jobs=-1)
            grid.fit(xtrain, ytrain)

            # Print the tuned parameters and score
            print(f'Best KNN Parameters : {grid.best_params_}')
            print(f'Best KNN Score : {grid.best_score_}')
            print('\n====================================================================================\n')

            best_knn = grid.best_estimator_

            logging.info('Hyperparameter tuning Complete for KNN')

            logging.info('Voting Classifier model training started')

            # Creating final Voting classifier
            er = VotingClassifier([('rfc',best_rfc),('gbc',GradientBoostingClassifier()),('knn',best_knn)], voting='soft', weights=[3,2,1])
            er.fit(xtrain, ytrain)
            print('Final Model Evaluation :\n')
            print_evaluated_results(xtrain,ytrain,xtest,ytest,er)
            logging.info('Voting Classifier Training Completed')

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj = er
            )
            logging.info('Model pickle file saved')
            # Evaluating Ensemble Classifier on test data
            ytest_pred = er.predict(xtest)

            accuracy, precision, recall, f1 = model_metrics(ytest, ytest_pred)
            logging.info(f'Test Accuracy : {accuracy}')
            logging.info(f'Test Precision : {precision}')
            logging.info(f'Test Recall : {recall}')
            logging.info(f'Test F1 Score : {f1}')
            logging.info('Final Model Training Completed')
            
            return accuracy, precision, recall, f1 
        
        except Exception as e:
            logging.info('Exception occured at Model Training')
            raise CustomException(e,sys)



