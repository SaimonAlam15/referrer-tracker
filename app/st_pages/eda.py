import streamlit as st
import matplotlib.pyplot as plt

from data import get_data
from queries import DATA_ANALYSIS_QUERY


def eda():
    data = get_data(DATA_ANALYSIS_QUERY)
    st.dataframe(data)

    # Get the top 5 most frequently occurring values for 'CAREER_LEVEL'
    top_career_levels = data['CAREER_LEVEL'].value_counts().nlargest(5)

    # Plot the bar chart
    fig, ax = plt.subplots()
    ax.bar(top_career_levels.index, top_career_levels.values)

    # Add labels and title
    ax.set_xlabel('CAREER LEVEL')
    ax.set_ylabel('Number of Referrers')
    ax.set_title('Top 5 Most Frequent Career levels amongst referrers')

    # Display the chart in Streamlit
    st.pyplot(fig)

    fig2, ax2 = plt.subplots()

    # Get the top 5 most frequently occurring values for 'titles'
    top_titles = data['TITLE_OF_LAST_POSITION'].value_counts().nlargest(5)

    ax2.bar(top_titles.index, top_titles.values)

    # Add labels and title
    ax2.set_xlabel('DESIGNATION')
    ax2.set_ylabel('Number of Referrers')
    ax2.set_title('Top 5 Most Frequent designations amongst referrers')
    fig2.autofmt_xdate(rotation=45)
    st.pyplot(fig2)


    top_expertise = data['FIELD_OF_EXPERTISE'].str.split(',').explode().value_counts().nlargest(10)

    # Plot the bar chart
    fig3, ax3 = plt.subplots()
    ax3.bar(top_expertise.index, top_expertise.values)

    # Add labels and title
    ax3.set_xlabel('FIELD OF EXPERTISE')
    ax3.set_ylabel('Number of Referrers')
    ax3.set_title('Top 5 fields of expertise amongst referrers')

    # Rotate x-axis labels for better visibility
    # st.pyplot(fig3, use_container_width=True)
    fig3.autofmt_xdate(rotation=45)

    # Display the chart in Streamlit
    st.pyplot(fig3)

    top_sources = data['SOURCE'].value_counts().nlargest(5)
    fig4, ax4 = plt.subplots()
    ax4.bar(top_sources.index, top_sources.values)

    # Add labels and title
    ax4.set_xlabel('SOURCE')
    ax4.set_ylabel('Number of Referrers')
    ax4.set_title('Top 5 sources amongst referrers')

    st.pyplot(fig4)

    filtered_rows = data[data['RECENTLY_ACTIVE'] == 1.0]

    # Count the number of rows
    count = len(data)
    print('Count:', count)
    print('Filtered Rows:', len(filtered_rows))

    # Create a pie chart
    fig5, ax5 = plt.subplots()
    ax5.pie([len(filtered_rows), count - len(filtered_rows)], labels=['ACTIVE', 'INACTIVE'], autopct='%1.1f%%')
    ax5.set_title('Percentage of referrers who have been active in the last 60 days')

    # Display the chart in Streamlit
    st.pyplot(fig5)