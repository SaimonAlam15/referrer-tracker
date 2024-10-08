from db import get_snowflake_connection
import pandas as pd

from sklearn.model_selection import train_test_split

from imblearn.over_sampling import SMOTE

import streamlit as st


conn = get_snowflake_connection()


def encode_data(input_df):
    categorical_columns = ['SOURCE', 'CAREER_LEVEL', 'TITLE_OF_LAST_POSITION', 'FIELD_OF_EXPERTISE']
    filtered_df = input_df[input_df['TARGET'] == 1]
    feature_names = []
    cols = []
    for col in categorical_columns:
        if col == 'FIELD_OF_EXPERTISE':
            value_counts = filtered_df['FIELD_OF_EXPERTISE'].str.split(',').explode().value_counts().nlargest(10)
            cols = [f'FIELD_OF_EXPERTISE_{val}' for val in value_counts.index]
        else:
            value_counts = filtered_df[col].value_counts().nlargest(5)
            cols = [f'{col}_{val}' for val in value_counts.index]
        feature_names.extend(cols)

    expertise_df = input_df['FIELD_OF_EXPERTISE'].str.get_dummies(sep=",").add_prefix('FIELD_OF_EXPERTISE_')
    expertise_df = expertise_df.loc[:, expertise_df.columns.isin(feature_names)]
    input_df = input_df.drop('FIELD_OF_EXPERTISE', axis=1)
    input_df = input_df.join(expertise_df)
    # input_df = pd.concat([input_df.drop('FIELD_OF_EXPERTISE', axis=1), expertise_df], axis=1)
    
    new_df = pd.get_dummies(input_df, columns=categorical_columns[:-1])
    new_df = new_df.loc[:, new_df.columns.isin(feature_names) & ~new_df.columns.str.startswith('FIELD_OF_EXPERTISE')]
    
    # df_merged = pd.concat([input_df, new_df]).drop_duplicates(['ID'], keep='last')
    input_df = input_df.drop(categorical_columns[:-1], axis=1)
    input_df = input_df.join(new_df)

    
    # Drop the original categorical columns
    # df_merged = df_merged.drop(categorical_columns[:-1], axis=1)

    return input_df.drop_duplicates(['ID'], keep='last'), feature_names


@st.cache_resource
def get_data(query):
    if not query:
        return None

    cur = conn.cursor()

    cur.execute(query)
    return cur.fetch_pandas_all()


def balance_data(X, y):
    smote = SMOTE(sampling_strategy='minority')
    x, y = smote.fit_resample(X, y)
    return x, y


def split_data(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0, test_size=0.3)
    return X_train, X_test, y_train, y_test