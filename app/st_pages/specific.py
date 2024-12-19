import streamlit as st

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from model import get_model, encode_data
from queries import TEST_DATA_QUERY
from data import get_data


@st.cache_resource
def cached_model():
    return get_model()


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
        'Select Job Industry*',
        options=[
            'Communications', 'Technology', 'Health Care', 'Education',
            'Financial Services', 'Staffing and Recruiting', 'Real Estate',
            'Information Technology'
        ]
    )
    job_skills = st.sidebar.multiselect(
        'Select Required Job Skills*',
        options=[
            'Accounting', 'Advertising', 'Art & Creative', 'Bookkeeping', 'Brand Strategy', 'Business Strategy', 'Clinical Research', 'Cloud Computing',
            'Communications', 'Community & Partnerships', 'Compliance', 'Computer Programming', 'Customer Success/CX', 'Cybersecurity',
            'Data Science', 'DEI', 'Design', 'DevOps', 'Education', 'Engineering', 'Entrepreneurship', 'ESG/CSR', 'Events', 'Fashion',
            'Finance', 'Fundraising', 'Government', 'Health and Fitness', 'Hospitality', 'Human Resources', 'Insurance', 'Legal', 'Logistics',
            'Management Consulting', 'Manufacturing', 'Market Research', 'Marketing', 'Media', 'Merchandising', 'Military', 'Nonprofit', 'Operations',
            'Organizational Development', 'Other', 'Product Management', 'Production, Film', 'Public Relations', 'Recruitment & Talent Acquisition', 'Retail',
            'Sales & Business Development', 'Social Media', 'Social Services', 'Technology', 'Venture Capital & Private Equity', 'Web', 'Writing, Editing'
        ]
    )
    score_threshold = st.sidebar.slider('Score Threshold', 0, 100, 80, 5) / 100
    # st.sidebar.button('Predict')
    if st.sidebar.button('Predict'):
        if not job_industry and not job_skills:
            st.warning('Please select Job Location(s), Job Industry and Required Job Skills.')
            return
        
        data = get_data(TEST_DATA_QUERY)
        data.rename(columns={'NAME_OF_LAST_COMPANY': 'NAME_OF_CURRENT/LAST_COMPANY'}, inplace=True)
        filter_table_df = data.copy(deep=True)

        data['INDUSTRY'] = job_industry
        data['REQUIRED_SKILLS'] = ','.join(job_skills)


        if job_location:
            data['LOCATION'] = ','.join(job_location)

        encoded_data, _ = encode_data(data)
        
        model, _, _, features = cached_model()
        encoded_data = encoded_data.reindex(columns=features, fill_value=0.0)

        if job_location:
            filter_table_df = filter_table_df[
                (filter_table_df['CITY'].isin(job_location) | filter_table_df['STATE'].isin(job_location)) &
                (filter_table_df['FIELD_OF_EXPERTISE'].apply(lambda x: any(skill in x.split(',') for skill in job_skills if x)))
            ]
        else:
            filter_table_df = filter_table_df[
                filter_table_df['FIELD_OF_EXPERTISE'].apply(lambda x: any(skill in x.split(',') for skill in job_skills if x))
            ]

        filter_table_df.rename(columns={'TARGET': 'HAS_REFERRED'}, inplace=True)
        filter_table_df.drop(columns=['INDUSTRY', 'REQUIRED_SKILLS', 'LOCATION'], inplace=True)
        filter_table_df.reset_index(drop=True, inplace=True)
        filter_table_df.index += 1

        st.header('Filtered by job attributes only')
        if (len(filter_table_df) == 0):
            st.error('No matches found based on job attributes.')
        else:
            st.dataframe(filter_table_df)
        # y_pred = model.predict(x_test.values)
        # print('Encoded columns', list(encoded_data.columns)[: 20])
        # print('Features', features)
        y_pred = model.predict(encoded_data[features].values)
        # st.write("Predictions:", list(y_pred)[:50])

        st.header('Predicted on the basis of historical data')

        rows = []
        for i, pred in enumerate(y_pred):
            if pred > 0:
                rows.append({
                    'SCORE': pred,
                    'FIRST_NAME': data.iloc[i]['FIRST_NAME'],
                    'LAST_NAME': data.iloc[i]['LAST_NAME'],
                    'EMAIL': data.iloc[i]['EMAIL'],
                    'SOURCE': data.iloc[i]['SOURCE'],
                    'CITY': data.iloc[i]['CITY'],
                    'STATE': data.iloc[i]['STATE'],
                    'CAREER_LEVEL': data.iloc[i]['CAREER_LEVEL'],
                    'NAME_OF_CURRENT/LAST_COMPANY': data.iloc[i]['NAME_OF_CURRENT/LAST_COMPANY'],
                    'TITLE_OF_LAST_POSITION': data.iloc[i]['TITLE_OF_LAST_POSITION'],
                    'FIELD_OF_EXPERTISE': data.iloc[i]['FIELD_OF_EXPERTISE'],
                    'RECENTLY_ACTIVE': data.iloc[i]['RECENTLY_ACTIVE'],
                    'HAS_REFERRED': data.iloc[i]['TARGET']
                })
        
        matching_data = pd.DataFrame(rows)
        matching_data.sort_values(by='SCORE', inplace=True, ascending=False)
        matching_data = matching_data[matching_data['SCORE'] >= score_threshold]
        matching_data['SCORE'] = (matching_data['SCORE'] * 100).round(2).astype(str) + '%'
        matching_data.reset_index(drop=True, inplace=True)
        matching_data.index += 1
        st.dataframe(matching_data)


        st.write("Total:", len(y_pred))
        st.write("Total predictions equal to 0%:", np.sum(y_pred == 0))
        st.write("Total predictions below 50%:", np.sum(y_pred <= 0.5))
        st.write("Total predictions between 50 and 70%:", np.sum((y_pred > 0.5) & (y_pred <= 0.7)))
        st.write("Total predictions between 70 and 90%:", np.sum((y_pred > 0.7) & (y_pred <= 0.9)))
        st.write("Total predictions between 90 and 100%:", np.sum((y_pred > 0.9) & (y_pred < 1.0)))
        st.write("Total predictions equal to 1:", np.sum(y_pred == 1.0))

        st.header('Analysis of existing data')
                
        # Get the top 5 most frequently occurring values for 'CAREER_LEVEL'
        top_career_levels = matching_data['CAREER_LEVEL'].value_counts().nlargest(5)

        # Plot the bar chart
        fig, ax = plt.subplots()
        ax.bar(top_career_levels.index, top_career_levels.values)

        # Add labels and title
        ax.set_xlabel('CAREER LEVEL')
        ax.set_ylabel('Number of Referrers')
        ax.set_title('Top 5 most frequent career levels amongst predicted referrers')

        # Display the chart in Streamlit
        st.pyplot(fig)

        fig2, ax2 = plt.subplots()

        # Get the top 5 most frequently occurring values for 'titles'
        top_titles = matching_data['TITLE_OF_LAST_POSITION'].value_counts().nlargest(5)

        ax2.bar(top_titles.index, top_titles.values)

        # Add labels and title
        ax2.set_xlabel('DESIGNATION')
        ax2.set_ylabel('Number of Referrers')
        ax2.set_title('Top 5 most frequent designations amongst predicted referrers')
        fig2.autofmt_xdate(rotation=45)
        st.pyplot(fig2)

        

        top_expertise = matching_data['FIELD_OF_EXPERTISE'].str.split(',').explode().value_counts().nlargest(10)

        # Plot the bar chart
        fig3, ax3 = plt.subplots()
        ax3.bar(top_expertise.index, top_expertise.values)

        # Add labels and title
        ax3.set_xlabel('FIELD OF EXPERTISE')
        ax3.set_ylabel('Number of Referrers')
        ax3.set_title('Top 5 fields of expertise amongst predicted referrers')

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
        ax4.set_title('Top 5 sources amongst predicted referrers')

        st.pyplot(fig4)

        filtered_rows = matching_data[matching_data['RECENTLY_ACTIVE'] == 1.0]

        # Count the number of rows
        count = len(matching_data)
        print('Count:', count)
        print('Filtered Rows:', len(filtered_rows))

        # Create a pie chart
        fig5, ax5 = plt.subplots()
        ax5.pie([len(filtered_rows), count - len(filtered_rows)], labels=['ACTIVE', 'INACTIVE'], autopct='%1.1f%%')
        ax5.set_title('Percentage of predicted referrers who have been active in the last 60 days')

        # Display the chart in Streamlit
        st.pyplot(fig5)