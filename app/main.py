import streamlit as st

from st_pages.eda import eda
from st_pages.generic import generic_referrers
from st_pages.specific import job_specific_referrers
from st_pages.filtered import filtered


pages = {
    "Data Analysis": eda,
    "Referrers - Generic": generic_referrers,
    "Referrers - Job Specific": job_specific_referrers,
    "Filtered": filtered
}


def main():
    st.set_page_config(layout="wide")
    st.markdown("<h1 style='text-align: center;'>Referrer Finder</h1>", unsafe_allow_html=True)
    selected_page = st.sidebar.selectbox("Choose a page", options=list(pages.keys()))
    pages[selected_page]()

if __name__ == '__main__':
    main()
