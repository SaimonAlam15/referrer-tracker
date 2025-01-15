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
            'Choose an option', 'Communications', 'Technology', 'Health Care', 'Education',
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

    st.sidebar.write("Filtering Criteria")

    filter_string = ""

    if job_location and job_industry != 'Choose an option' and job_skills:
        location_filter = tuple(job_location) if len(job_location) > 1 else f"(\'{job_location[0]}\')"
        filter_options = [
            {
            'text': f"Members located in:  {','.join(job_location)}",
            'sql': f"c.state in {location_filter} or c.city in {location_filter}"
            },
            {
            'text': f"Members posessing some or all of the following skills: {','.join(job_skills)}",
            'sql': f"""ARRAY_SIZE(
            ARRAY_INTERSECTION(
                SPLIT(c.field_of_expertise, ','), 
                SPLIT('{','.join(job_skills)}', ',') 
            )
        ) > 0"""
            },
            {
            'text': f"Members who have referred people for jobs in the {job_industry} industry",
            'sql': f""" ARRAY_SIZE(
            ARRAY_INTERSECTION(
                SPLIT(a.industries, ','), 
                SPLIT('{job_industry}', ',') 
            )
        ) > 0 """
            },
            {
            'text': f"Members who have referred people for jobs located in {','.join(job_location)}",
            'sql': f"""ARRAY_SIZE(
            ARRAY_INTERSECTION(
                SPLIT(a.locations, ','), 
                SPLIT('{','.join(job_skills)}', ',') 
            )
        ) > 0 """
            },
            {
            'text': f"Members who have referred people for jobs requiring the following skills: {','.join(job_skills)}",
            'sql': f"""ARRAY_SIZE(
            ARRAY_INTERSECTION(
                SPLIT(a.skills, ','),  
                SPLIT('{','.join(job_skills)}', ',') 
            )
        ) > 0"""
            }
        ]

        query_steps = []
        if 'query_steps' not in st.session_state:
            st.session_state.query_steps = query_steps

        def add_query_step():
            st.session_state.query_steps.append({'filter': '', 'condition': 'AND'})

        def delete_query_step(index):
            st.session_state.query_steps.pop(index)

        used_filters = [step['filter'] for step in st.session_state.query_steps]

        for i, step in enumerate(st.session_state.query_steps):
            col1, col2, col3 = st.sidebar.columns([1, 2, 0.5])
            with col1:
                if i > 0:
                    step['condition'] = st.selectbox(f'Condition {i+1}', options=['AND', 'OR'], index=0, key=f'condition_{i}')
            with col2:
                available_options = [option['text'] for option in filter_options if option['text'] not in used_filters or option['text'] == step['filter']]
                step['filter'] = st.selectbox(f'Filter {i+1}', options=available_options, index=available_options.index(step['filter']) if step['filter'] in available_options else 0, key=f'filter_{i}')
            with col3:
                if st.button('X', key=f'delete_{i}'):
                    delete_query_step(i)

        # for step in st.session_state.query_steps:
        #     if filter_string:
        #         filter_string += f" {step['condition']} "
        #         filter_string += step['filter']

        st.sidebar.button('Add Step', on_click=add_query_step)

        print('Filter', st.session_state.query_steps)

        def build_filter_string(steps, options):
            filter_str = ""
            total_steps = len(steps)
            for i, step in enumerate(steps):
                for option in options:
                    if step['filter'] == option['text']:
                        if i == total_steps - 1:
                            filter_str += f"{option['sql']}"
                        else:
                            filter_str += f"{option['sql']} {step['condition']} "
                        break
            return filter_str

        filter_string = build_filter_string(st.session_state.query_steps, filter_options)


        print('Query String: ', filter_string)
    
    if st.sidebar.button('Fetch'):
        if not job_location or not job_industry or not job_skills:
            st.warning('Please select Job Location(s), Job Industry and Required Job Skills.')
            return
        
        if not filter_string:
            st.warning('Please provide at least 1 filtering criterion.')
            return

        query = ATTRIBUTES_FILTER_QUERY.format(
            # industry = job_industry,
            # location = ','.join(job_location),
            # required_skills = ','.join(job_skills),
            # state = location_filter,
            # city = location_filter,
            # field_of_expertise = ','.join(job_skills)
            filter = filter_string
        )
        print('Query:', query)

        data = get_data(query)
        data.rename(columns={'NAME_OF_LAST_COMPANY': 'NAME_OF_CURRENT/LAST_COMPANY'}, inplace=True)
        # data.drop(columns=['ROW_NUM'], inplace=True)

        # st.write('Fetch all members:')
        # st.write(f"- **Located in _{','.join(job_location)}_, or**")
        # st.write(f"- **Posessing some or all of the following skills: _{','.join(job_skills)}_**")
        # st.write("Or those who have referred people for jobs:")
        # st.write(f"- **From the _{job_industry}_ industry, or**")
        # st.write(f"- **Located in _{','.join(job_location)}_**, or")
        # st.write(f"- **Requiring the following skills: _{','.join(job_skills)}_**.")

        data.index = np.arange(1, len(data) + 1)

        if 'ROW_NUM' in data.columns:
            data = data.drop(columns=['ROW_NUM'])

        if 'JOB_ID' in data.columns:
            data = data.drop(columns=['JOB_ID'])

        st.dataframe(data)

        st.write('Total number of potential referrers:', data.shape[0])