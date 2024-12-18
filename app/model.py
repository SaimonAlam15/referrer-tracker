# Classifer Models
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

from data import get_data, balance_data, split_data
from queries import MODEL_1_TRAINING_DATA_QUERY


def encode_data(input_df):
    categorical_columns = [
        'SOURCE', 'CAREER_LEVEL', 'TITLE_OF_LAST_POSITION', 'FIELD_OF_EXPERTISE', 
        'INDUSTRY', 'LOCATION', 'REQUIRED_SKILLS'
    ]
    filtered_df = input_df[input_df['TARGET'] == 1]
    feature_names = []
    cols = []
    for col in categorical_columns:
        if col in ['FIELD_OF_EXPERTISE', 'LOCATION', 'REQUIRED_SKILLS']:
            value_counts = filtered_df[col].str.split(',').explode().value_counts().nlargest(10)
            cols = [f'{col}_{val}' for val in value_counts.index]
        else:
            value_counts = filtered_df[col].value_counts().nlargest(5)
            cols = [f'{col}_{val}' for val in value_counts.index]
        feature_names.extend(cols)

    expertise_df = input_df['FIELD_OF_EXPERTISE'].str.get_dummies(sep=",").add_prefix('FIELD_OF_EXPERTISE_')
    expertise_df = expertise_df.loc[:, expertise_df.columns.isin(feature_names)]
    input_df = input_df.drop('FIELD_OF_EXPERTISE', axis=1)
    input_df = input_df.join(expertise_df)

    location_df = input_df['LOCATION'].str.get_dummies(sep=",").add_prefix('LOCATION_')
    location_df = location_df.loc[:, location_df.columns.isin(feature_names)]
    input_df = input_df.drop('LOCATION', axis=1)
    input_df = input_df.join(location_df)

    required_skills_df = input_df['REQUIRED_SKILLS'].str.get_dummies(sep=",").add_prefix('REQUIRED_SKILLS_')
    required_skills_df = required_skills_df.loc[:, required_skills_df.columns.isin(feature_names)]
    input_df = input_df.drop('REQUIRED_SKILLS', axis=1)
    input_df = input_df.join(required_skills_df)

    new_df = pd.get_dummies(input_df, columns=['SOURCE', 'CAREER_LEVEL', 'TITLE_OF_LAST_POSITION', 'INDUSTRY'])
    new_df = new_df.loc[:, new_df.columns.isin(feature_names) &
                        ~new_df.columns.str.startswith(('FIELD_OF_EXPERTISE', 'LOCATION', 'REQUIRED_SKILLS'))]

    # df_merged = pd.concat([input_df, new_df]).drop_duplicates(['ID'], keep='last')
    input_df = input_df.drop(['SOURCE', 'CAREER_LEVEL', 'TITLE_OF_LAST_POSITION', 'INDUSTRY'], axis=1).fillna(0)
    input_df = input_df.join(new_df)

    # Drop the original categorical columns
    # df_merged = df_merged.drop(['SOURCE', 'CAREER_LEVEL', 'TITLE_OF_LAST_POSITION', 'INDUSTRY'], axis=1).fillna(0)
    return input_df.drop_duplicates(['ID'], keep='last'), feature_names


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
    # n_estimators=100, max_depth=20, n_jobs=-1
    params = {
        'bootstrap': True, 'max_depth': 30, 'min_samples_leaf': 1,
        'min_samples_split': 5, 'n_estimators': 300
    }
    reg = RandomForestRegressor(**params)
    reg.fit(X_train, y_train)
    return reg


def get_model():
    data = get_data(MODEL_1_TRAINING_DATA_QUERY)
    X_train, X_test, y_train, y_test, features = process_data(data)
    model = train_model(X_train, y_train)
    return model, X_test, y_test, features





