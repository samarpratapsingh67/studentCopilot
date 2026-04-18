import os
import sys

import numpy as np 
import pandas as pd
import dill
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from src.exception import CustomException
from src.logger import logging

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    
def evaluate_models(xtrain,ytrain,xtest,ytest,models):
    try:
        report = {}
        for i in range(len(models)):
            model = list(models.values())[i]
            # Train model
            model.fit(xtrain,ytrain)

            # Predict Training data
            y_train_pred = model.predict(xtrain)

            # Predict Testing data
            y_test_pred =model.predict(xtest)

            # Get F1 score for test data
            test_model_score = f1_score(ytest, y_test_pred, zero_division=0)

            report[list(models.keys())[i]] =  test_model_score

        return report

    except Exception as e:
        logging.info('Exception occured during model training')
        raise CustomException(e,sys)
    
def model_metrics(true, predicted):
    try :
        accuracy = accuracy_score(true, predicted)
        precision = precision_score(true, predicted, zero_division=0)
        recall = recall_score(true, predicted, zero_division=0)
        f1 = f1_score(true, predicted, zero_division=0)
        return accuracy, precision, recall, f1
    except Exception as e:
        logging.info('Exception Occured while evaluating metric')
        raise CustomException(e,sys)
    

def print_evaluated_results(xtrain,ytrain,xtest,ytest,model):
    try:
        ytrain_pred = model.predict(xtrain)
        ytest_pred = model.predict(xtest)

        # Evaluate Train and Test dataset
        model_train_acc , model_train_prec, model_train_rec, model_train_f1 = model_metrics(ytrain, ytrain_pred)
        model_test_acc , model_test_prec, model_test_rec, model_test_f1 = model_metrics(ytest, ytest_pred)

        # Printing results
        print('Model performance for Training set')
        print("- Accuracy: {:.4f}".format(model_train_acc))
        print("- Precision: {:.4f}".format(model_train_prec))
        print("- Recall: {:.4f}".format(model_train_rec))
        print("- F1 Score: {:.4f}".format(model_train_f1))

        print('----------------------------------')
    
        print('Model performance for Test set')
        print("- Accuracy: {:.4f}".format(model_test_acc))
        print("- Precision: {:.4f}".format(model_test_prec))
        print("- Recall: {:.4f}".format(model_test_rec))
        print("- F1 Score: {:.4f}".format(model_test_f1))
    
    except Exception as e:
        logging.info('Exception occured during printing of evaluated results')
        raise CustomException(e,sys)
    
def load_object(file_path):
    try:
        with open(file_path,'rb') as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        logging.info('Exception Occured in load_object function utils')
        raise CustomException(e,sys)