import streamlit as st
import pandas as pd
import plotly.express as px

#page configuration
st.set_page_config(page_title='Employee Dashboard', page_icon="👥", layout='wide')

@st.cache_data
def load_data():
  #load employee dataset
  df = pd.read_csv('cleaned_employee_dataset.csv')
  return df

