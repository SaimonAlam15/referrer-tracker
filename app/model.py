# Classifer Models
from sklearn.ensemble import RandomForestClassifier

from data import get_data, encode_data, balance_data, split_data
from queries import MODEL_1_TRAINING_DATA_QUERY


def process_data(input_df):
    df_merged, feature_names = encode_data(input_df)
    X = df_merged[feature_names]
    y = df_merged['TARGET']
    X_balanced, y_balanced = balance_data(X, y)
    X_train, X_test, y_train, y_test = split_data(X_balanced, y_balanced)
    return X_train, X_test, y_train, y_test, feature_names


def train_model(X_train, y_train):
    params = {
        'criterion': 'gini', 'max_depth': 20, 'min_samples_leaf': 1,
        'min_samples_split': 5, 'n_estimators': 1000
    }
    reg = RandomForestClassifier(**params)
    reg.fit(X_train, y_train)
    return reg


def get_model():
    data = get_data(MODEL_1_TRAINING_DATA_QUERY)
    X_train, X_test, y_train, y_test, features = process_data(data)
    model = train_model(X_train, y_train)
    return model, X_test, y_test, features





