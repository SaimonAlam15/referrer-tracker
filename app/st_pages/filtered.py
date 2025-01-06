import streamlit as st

import pandas as pd
import numpy as np

from queries import ATTRIBUTES_FILTER_QUERY
from data import get_data



def filtered():
    job_location = st.sidebar.multiselect(
        'Select Job Location(s)*',
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
        if not job_location or not job_industry or not job_skills:
            st.warning('Please select Job Location(s), Job Industry and Required Job Skills.')
            return
        
        location_filter = tuple(job_location) if len(job_location) > 1 else f"(\'{job_location[0]}\')"

        query = ATTRIBUTES_FILTER_QUERY.format(
            industry = job_industry,
            location = ','.join(job_location),
            required_skills = ','.join(job_skills),
            state = location_filter,
            city = location_filter,
            field_of_expertise = ','.join(job_skills)
        )

        data = get_data(query)
        data.rename(columns={'NAME_OF_LAST_COMPANY': 'NAME_OF_CURRENT/LAST_COMPANY'}, inplace=True)
        # data.drop(columns=['ROW_NUM'], inplace=True)


        st.write("- **Fetch all members matching the given criteria**", ", ".join(job_location))
        st.write("- **Fetch all members that have referred for jobs matching the given criteria**")

        data.index = np.arange(1, len(data) + 1)

        st.dataframe(data)

        st.write('Total number of potential referrers:', data.shape[0])