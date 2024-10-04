from db import get_snowflake_connection
import pandas as pd

from sklearn.model_selection import train_test_split

from imblearn.over_sampling import SMOTE
import streamlit as st


conn = get_snowflake_connection()


@st.cache_resource
def get_data(query):
    if not query:
        return None
    
    cur = conn.cursor()

    cur.execute(query)
    return cur.fetch_pandas_all()


def encode_data(input_df):
    categorical_columns = ['SOURCE', 'CAREER_LEVEL', 'TITLE_OF_LAST_POSITION', 'FIELD_OF_EXPERTISE', 'INDUSTRY', 'LOCATION']
    feature_names = []
    for col in categorical_columns:
        cols = []
        if col in ['FIELD_OF_EXPERTISE', 'LOCATION']:
            value_counts = input_df[col].str.split(',').explode().value_counts().nlargest(10)
            cols = [f'{col}_{val}' for val in value_counts.index]
        else:
            value_counts = input_df[col].value_counts().nlargest(5)
            cols = [f'{col}_{val}' for val in value_counts.index]
        feature_names.extend(cols)

    expertise_df = input_df['FIELD_OF_EXPERTISE'].str.get_dummies(sep=",").add_prefix('FIELD_OF_EXPERTISE_')
    input_df = pd.concat([input_df.drop('FIELD_OF_EXPERTISE', axis=1), expertise_df], axis=1)

    location_df = input_df['LOCATION'].str.get_dummies(sep=",").add_prefix('LOCATION_')
    input_df = pd.concat([input_df.drop('LOCATION', axis=1), location_df], axis=1)
    
    new_df = pd.get_dummies(input_df, columns=['SOURCE', 'CAREER_LEVEL', 'TITLE_OF_LAST_POSITION', 'INDUSTRY'])
    
    df_merged = pd.concat([input_df, new_df]).drop_duplicates(['ID'], keep='last')
    
    # Drop the original categorical columns
    df_merged = df_merged.drop(['SOURCE', 'CAREER_LEVEL', 'TITLE_OF_LAST_POSITION', 'INDUSTRY'], axis=1).fillna(0)
    return df_merged, feature_names


def balance_data(X, y):
    smote = SMOTE(sampling_strategy='minority')
    x, y = smote.fit_resample(X, y)
    return x, y


def split_data(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0, test_size=0.3)
    return X_train, X_test, y_train, y_test