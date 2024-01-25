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

# Display Info()
# In order to display output on our app. we first need to capture it.
# We can use an IO buffer to capture the output.  Then we will use the .getvalue() arugment to retrive it
# Create a string buffer to capture the content
buffer = StringIO()
# Write the info into the buffer
df.info(buf=buffer)
# Retrieve the content from the buffer
summary_info = buffer.getvalue()


# Use streamlit to display the info
if st.button('Show Summary Info'):
    st.text(summary_info)

# Display an interactive Null Values
st.markdown("#### Null Values as DataFrame and String")

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



import plotly.express as px
import plotly.io as pio
pio.templates.default = 'plotly_dark'
column_to_use = ['Item_Weight', 'Item_Fat_Content', 'Item_Visibility', 'Item_Type', 'Item_MSRP', "Outlet_Size", 'Outlet_Location_Type', 'Outlet_Type', 'Item_Outlet_Sales']

# Use plotly for explore functions
def plotly_explore_numeric(df,x):
    fig = px.histogram(df,x=x,marginal='box',title='Distribution of {x}',width=1000,height=500)
    return fig

def plotly_explore_categorical(df,x):
    fig=px.histogram(df,x=x,color=x,title='Distribution of {x}',width=1000,height=500)
    fig.update_layout(showlegend=False)
    return fig

st.markdown('#### Displaying approprate Plotly plot based on selected column')

column = st.selectbox(label="Select a column", options=column_to_use)

# Conditional statement to determin which function to use
if df[column].dtype == 'object':
    fig=plotly_explore_categorical(df,column)
else:
    fig=plotly_explore_numeric(df,column)

# Display appropriate eda plots
st.plotly_chart(fig)

st.markdown("#### Explore Features vs. Sale Price with Plotly")
# Add a selectbox for all possible features 
# Copy list of columns
feature_to_use = column_to_use[:]
# Define target
target = 'Item_Outlet_Sales'
# Remove target from list of features
feature_to_use.remove(target)

# Add a selectbox for all possible columns
feature = st.selectbox(label='Select a feature to compare with Item Outlet Sales', options=feature_to_use)


# functionizing numeric vs target
def plotly_numeric_vs_target(df, x, y='Item_Outlet_Sales', trendline='ols',add_hoverdata=True):
    if add_hoverdata == True:
        hover_data = list(df.columns)
    else: 
        hover_data = None
        
    pfig = px.scatter(df, x=x, y=y,width=800, height=600,
                     hover_data=hover_data,
                      trendline=trendline,
                      trendline_color_override='red',
                     title=f"{x} vs. {y}")
    
    pfig.update_traces(marker=dict(size=3),
                      line=dict(dash='dash'))
    return pfig

def plotly_catagorical_vs_target(df,x,y="Item_Outlet_Sales",histfunc='avg',
                                 width=800,height=500):

    fig = px.histogram(df,x=x,y=y,color=x,width=width,height=height,histfunc=histfunc,
                      title=f'Compare {histfunc.title()} {y} by {x}')
    fig.update_layout(showlegend=False)
    return fig

# Conditional statement to determin which function to use
if df[feature].dtype =='object':
    fig_vs = plotly_catagorical_vs_target(df,x=feature)
else:
    fig_vs = plotly_numeric_vs_target(df,x = feature)

st.plotly_chart(fig_vs)







