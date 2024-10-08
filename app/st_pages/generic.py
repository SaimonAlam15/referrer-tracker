import streamlit as st

import pandas as pd
import numpy as np

from model_generic_rforest import get_generic_model
from data import get_data, encode_data as encode_generic_data
from queries import TEST_DATA_QUERY, DATA_ANALYSIS_QUERY


@st.cache_resource
def cached_generic_model():
    return get_generic_model()


def eda():
    data = get_data(DATA_ANALYSIS_QUERY)
    st.dataframe(data)


def generic_referrers():
    if st.sidebar.button('Predict'):    
        data = get_data(TEST_DATA_QUERY)
        encoded_data, _ = encode_generic_data(data)
        
        model, _, _, features = cached_generic_model()
        encoded_data = encoded_data.reindex(columns=features, fill_value=0.0)
        # y_pred = model.predict(x_test.values)
        # print('Encoded columns', list(encoded_data.columns)[: 20])
        # print('Features', features)
        y_pred = model.predict(encoded_data[features].values)
        # st.write("Predictions:", list(y_pred)[:50])
        st.write("Total:", len(y_pred))
        st.write("Number of likely referrers:", np.sum(y_pred == 1))
        st.write("Number of unlikely referrers:", np.sum(y_pred == 0))

        rows = []
        for i, pred in enumerate(y_pred):
            if pred == 1:
                rows.append({
                    'EMAIL': data.iloc[i]['EMAIL'],
                    'SOURCE': data.iloc[i]['SOURCE'],
                    'CAREER_LEVEL': data.iloc[i]['CAREER_LEVEL'],
                    'TITLE_OF_LAST_POSITION': data.iloc[i]['TITLE_OF_LAST_POSITION'],
                    'FIELD_OF_EXPERTISE': data.iloc[i]['FIELD_OF_EXPERTISE'],
                    'HAS_REFERRED': data.iloc[i]['TARGET']
                })
        
        matching_data = pd.DataFrame(rows)
        matching_data.sort_values(by='HAS_REFERRED', inplace=True)
        st.dataframe(matching_data)
        del matching_data, rows, data