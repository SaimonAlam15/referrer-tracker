import streamlit as st

import pandas as pd
import numpy as np

from queries import ATTRIBUTES_FILTER_QUERY
from data import get_data



def filtered():
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
            'Information Technology', 'Marketing and Advertising'
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
    # st.sidebar.button('Predict')
    if st.sidebar.button('Fetch'):
        if not job_industry and not job_skills:
            st.warning('Please select Job Location(s), Job Industry and Required Job Skills.')
            return
        
        query = ATTRIBUTES_FILTER_QUERY.format(
            industry = job_industry,
            location = job_location[0], # TODO - Handle multiple locations
            required_skills = job_skills[0], # TODO - Handle multiple skills
            state = job_location[0], # TODO - Handle multiple locations
            city = job_location[0], # TODO - Handle multiple locations
            field_of_expertise = job_skills[0] # TODO - Handle multiple skills
        )
        data = get_data(query)
        data.rename(columns={'NAME_OF_LAST_COMPANY': 'NAME_OF_CURRENT/LAST_COMPANY'}, inplace=True)
        # data.drop(columns=['ROW_NUM'], inplace=True)

        st.dataframe(data)

        st.write('Total number of potential referrers:', data.shape[0])