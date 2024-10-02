import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

# Classifer Models
from sklearn.ensemble import RandomForestClassifier

from imblearn.over_sampling import SMOTE
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix

from data import get_data, balance_data, split_data
from queries import MODEL_2_TRAINING_DATA_QUERY



def encode_data(input_df):
    categorical_columns = ['SOURCE', 'CAREER_LEVEL', 'TITLE_OF_LAST_POSITION', 'FIELD_OF_EXPERTISE']
    filtered_df = input_df[input_df['TARGET'] == 1]
    feature_names = []
    for col in categorical_columns:
        cols = []
        if col == 'FIELD_OF_EXPERTISE':
            value_counts = filtered_df['FIELD_OF_EXPERTISE'].str.split(',').explode().value_counts().nlargest(10)
            cols = [f'FIELD_OF_EXPERTISE_{val}' for val in value_counts.index]
        else:
            value_counts = filtered_df[col].value_counts().nlargest(5)
            cols = [f'{col}_{val}' for val in value_counts.index]
        feature_names.extend(cols)

    expertise_df = input_df['FIELD_OF_EXPERTISE'].str.get_dummies(sep=",").add_prefix('FIELD_OF_EXPERTISE_')
    input_df = pd.concat([input_df.drop('FIELD_OF_EXPERTISE', axis=1), expertise_df], axis=1)
    
    new_df = pd.get_dummies(input_df, columns=categorical_columns[:-1])
    
    df_merged = pd.concat([input_df, new_df]).drop_duplicates(['ID'], keep='last')
    
    # Drop the original categorical columns
    df_merged = df_merged.drop(categorical_columns[:-1], axis=1)

    return df_merged, feature_names


def process_data(input_df):
    df_merged, feature_names = encode_data(input_df)
    X = df_merged[feature_names]
    y = df_merged['TARGET']
    X_balanced, y_balanced = balance_data(X, y)
    X_train, X_test, y_train, y_test = split_data(X_balanced, y_balanced)
    return X_train, X_test, y_train, y_test, feature_names


def train_model(X_train, y_train):
    # params = {
    #     'criterion': 'gini', 'max_depth': 20, 'min_samples_leaf': 1,
    #     'min_samples_split': 5, 'n_estimators': 1000
    # }
    # reg = RandomForestClassifier(**params)
    params = {'n_estimators': 50, 'min_samples_split': 10, 'min_samples_leaf': 2, 'max_depth': 5, 'criterion': 'gini'}
    # Initialize the RandomForestClassifier with the new parameters
    reg = RandomForestClassifier(**params, n_jobs=-1)
    reg.fit(X_train, y_train)
    return reg


def get_generic_model():
    data = get_data(MODEL_2_TRAINING_DATA_QUERY)
    X_train, X_test, y_train, y_test, features = process_data(data)
    model = train_model(X_train, y_train)
    return model, X_test, y_test, features





