import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO

# Add title
st.title('Sale Price Analysis')

# Function for loading data
# Adding data caching
@st.cache_data
def load_data():
    fpath = 'Data/cleaned_sales_prediction.csv'
    df = pd.read_csv(fpath)
    return df

# Load the Data
df = load_data()

# Display an interactive dataframe
st.markdown('#### Product Sales Data')

# If the button is presseed, print the message
if st.button('Show DataFrame'):
    st.dataframe(df)

# Display Discriptive stats
st.markdown("#### Discriptive Statistics")

# If button is pressed, print message
if st.button('Show Discriptive Statistics'):
    st.dataframe(df.describe().round(2))

# Display Summary Stats
st.markdown("#### Summary Info")

# Use streamlit to display the info
if st.button('Show Summary Info'):
    st.text(summary_info)

# Display an interactive Null Values
st.markdown("#### Null Values as DataFrame and String")
# Display Info()
# In order to display output on our app. we first need to capture it.
# We can use an IO buffer to capture the output.  Then we will use the .getvalue() arugment to retrive it
# Create a string buffer to capture the content
buffer = StringIO()
# Write the info into the buffer
df.info(buf=buffer)
# Retrieve the content from the buffer
summary_info = buffer.getvalue()

# Null valuse two ways 
if st.button('Show Null Values as DataFrame'):
    nulls = df.isna().sum()
    st.dataframe(nulls)

# Create a string buffer to capture the content
na_buffer = StringIO()
# Write the content inot the buffer...use to_string
df.isna().sum().to_string(na_buffer)
# Retrieve the content from the buffer
null_values = na_buffer.getvalue()
# Use Streamlit to display the info
if st.button('Show Null Values as String'):
    st.text(null_values)