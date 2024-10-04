import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from model import get_model
from model_generic_rforest import get_generic_model, encode_data as encode_generic_data
from data import get_data, encode_data
from queries import MODEL_1_TRAINING_DATA_QUERY, TEST_DATA_QUERY


@st.cache_resource
def cached_model():
    return get_model()


@st.cache_resource
def cached_generic_model():
    return get_generic_model()


def eda():
    data = get_data(MODEL_1_TRAINING_DATA_QUERY)
    st.write(data.head(50))


def job_specific_referrers():
    job_location = st.sidebar.multiselect(
        'Select Job Location(s)',
        options=[
            'Remote', 'New York', 'CT', 'TX', 'Austin', 'Greenwich',
            'San Francisco', 'Miami', 'Remote/Various Locations', 'Remote/Hybrid',
            'Toronto', 'Philadelphia'
        ]
    )
    job_industry = st.sidebar.selectbox(
        'Select Job Industry',
        options=[
            'Communications', 'Technology', 'Health Care', 'Education',
            'Financial Services', 'Staffing and Recruiting', 'Real Estate',
        ]
    )
    # st.sidebar.button('Predict')
    if st.sidebar.button('Predict'):
        if not job_location or not job_industry:
            st.warning('Please select both Job Location(s) and Job Industry.')
            return
        
        data = get_data(TEST_DATA_QUERY)
        data['INDUSTRY'] = job_industry
        data['LOCATION'] = ','.join(job_location)
        encoded_data, _ = encode_data(data)
        
        model, x_test, y_test, features = cached_model()
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
                    'INDUSTRY': data.iloc[i]['INDUSTRY'],
                    'LOCATION': data.iloc[i]['LOCATION'],
                    'RECENTLY_ACTIVE': data.iloc[i]['RECENTLY_ACTIVE'],
                    'HAS_REFERRED': data.iloc[i]['TARGET']
                })
        
        matching_data = pd.DataFrame(rows)
        matching_data.sort_values(by='HAS_REFERRED', inplace=True)
        st.dataframe(matching_data)
                
        # Get the top 5 most frequently occurring values for 'CAREER_LEVEL'
        top_career_levels = matching_data['CAREER_LEVEL'].value_counts().nlargest(5)

        # Plot the bar chart
        fig, ax = plt.subplots()
        ax.bar(top_career_levels.index, top_career_levels.values)

        # Add labels and title
        ax.set_xlabel('CAREER LEVEL')
        ax.set_ylabel('Number of Referrers')
        ax.set_title('Top 5 Most Frequent Career levels amongst predicted referrers')

        # Display the chart in Streamlit
        st.pyplot(fig)

        fig2, ax2 = plt.subplots()

        # Get the top 5 most frequently occurring values for 'titles'
        top_titles = matching_data['TITLE_OF_LAST_POSITION'].value_counts().nlargest(5)

        ax2.bar(top_titles.index, top_titles.values)

        # Add labels and title
        ax2.set_xlabel('DESIGNATION')
        ax2.set_ylabel('Number of Referrers')
        ax2.set_title('Top 5 Most Frequent designations amongst predicted referrers')

        st.pyplot(fig2)

        

        top_expertise = matching_data['FIELD_OF_EXPERTISE'].str.split(',').explode().value_counts().nlargest(10)

        # Plot the bar chart
        fig3, ax3 = plt.subplots()
        ax3.bar(top_expertise.index, top_expertise.values)

        # Add labels and title
        ax3.set_xlabel('FIELD OF EXPERTISE')
        ax3.set_ylabel('Number of Referrers')
        ax3.set_title('Top 5 Fields of Expertise Amongst Referrers')

        # Rotate x-axis labels for better visibility
        # st.pyplot(fig3, use_container_width=True)
        fig3.autofmt_xdate(rotation=45)

        # Display the chart in Streamlit
        st.pyplot(fig3)

        top_sources = matching_data['SOURCE'].value_counts().nlargest(5)
        fig4, ax4 = plt.subplots()
        ax4.bar(top_sources.index, top_sources.values)

        # Add labels and title
        ax4.set_xlabel('SOURCE')
        ax4.set_ylabel('Number of Referrers')
        ax4.set_title('Top 5 Sources Amongst Referrers')

        st.pyplot(fig4)

        filtered_rows = matching_data[matching_data['RECENTLY_ACTIVE'] == 1.0]

        # Count the number of rows
        count = len(matching_data)
        print('Count:', count)
        print('Filtered Rows:', len(filtered_rows))

        # Create a pie chart
        fig5, ax5 = plt.subplots()
        ax5.pie([len(filtered_rows), count - len(filtered_rows)], labels=['ACTIVE', 'INACTIVE'], autopct='%1.1f%%')
        ax5.set_title('Percentage of referrers who have been active in the last 60 days')

        # Display the chart in Streamlit
        st.pyplot(fig5)




def generic_referrers():
    if st.sidebar.button('Predict'):    
        data = get_data(TEST_DATA_QUERY)
        encoded_data, _ = encode_generic_data(data)
        
        model, x_test, y_test, features = cached_generic_model()
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

pages = {"Data Analysis":eda, "Referrers - Generic": generic_referrers, "Referrers - Job Specific": job_specific_referrers}

def main():
    st.set_page_config(layout="wide")
    st.markdown("<h1 style='text-align: center;'>Referrer Finder</h1>", unsafe_allow_html=True)
    selected_page = st.sidebar.selectbox("Choose a page", options=list(pages.keys()))
    pages[selected_page]()

if __name__ == '__main__':
    main()
