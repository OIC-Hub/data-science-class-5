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


def create_sidebar_filter(df):
  """Create sidebar filter and return filter values"""
  st.sidebar.header("Filter")

  department = st.sidebar.multiselect(
    "Select Department(s)",
    options=df['department'].unique(),
    default=df['department'].unique()
  )

  locations = st.sidebar.multiselect(
    "Select Office Location(s)",
    options=df['office_location'].unique(),
    default=df['office_location'].unique()
  )

  remote_filter = st.sidebar.radio(
    "Remote Work Status",
    options=["All", "Yes", "No"],
    index=0
  )

  return department, locations, remote_filter

def filter_data(df, department, locations, remote_filter):
  """Apply filter to the dataframe"""
  filtered_df = df[df['department'].isin(department) & df['office_location'].isin(locations)]
  if remote_filter != "All":
    filtered_df = filtered_df[filtered_df['remote'] == remote_filter]
  return filtered_df

def display_metrics(filtered_df):
  """Display key metrics in columns"""
  col1, col2, col3, col4 = st.columns(4)

  with col1:
    st.metric("👤Total Employee", len(filtered_df))
  
  with col2:
    avg_salary = filtered_df['salary'].mean() if len(filtered_df) > 0 else 0 
    st.metric("Average Salary", f"${avg_salary:,.2f}")

  with col3:
    avg_performance = filtered_df['performance'].mean() if len(filtered_df) > 0 else 0
    st.metric("Average Performance", f"{avg_performance:.1f}")

  with col4:
    remote_pct = (filtered_df['remote'] == 'Yes').sum() / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
    st.metric("Remote Workers", f"{remote_pct:.1f}")

def display_charts(filtered_df):
  """Create visualization charts"""
  if len(filtered_df) == 0:
    st.warning("No available data for selected filters. Please adjust your filter selections.")
    return
  
  col1, col2 = st.columns(2)

  with col1:
    st.subheader("Employee by Department")
    dept_counts = filtered_df['department'].value_counts()
    fig1 = px.pie(values=dept_counts.values, names=dept_counts.index, hole=0.5)
    st.plotly_chart(fig1, use_container_width=True)

  with col2:
    st.subheader("Average Salary by Department")
    dept_salary = filtered_df.groupby('department')['salary'].mean().sort_values(ascending=True)
    fig2 = px.bar(
      x=dept_salary.values,
      y=dept_salary.index,
      orientation='h'
    )
    fig2.update_layout(xaxis_title="Salary", yaxis_title="Department")
    st.plotly_chart(fig2, use_container_width=True)
  

  col3, col4 = st.columns(2)

  with col3:
    st.subheader("Performance Distribution")
    fig3 = px.histogram(filtered_df, x='performance', nbins=6)
    fig3.update_layout(xaxis_title="Performance Score", yaxis_title="Count")
    fig3.update_traces(marker_line_color='white', marker_line_width=1.5)
    st.plotly_chart(fig3, use_container_width=True)

  with col4:
    st.subheader("Employee by Location")
    location_counts = filtered_df['office_location'].value_counts()
    fig4 = px.bar(x=location_counts.index, y=location_counts.values)
    fig4.update_layout(xaxis_title="Office Location", yaxis_title="Count")
    st.plotly_chart(fig4, use_container_width=True)
  

def display_table_data(filtered_df):
  """Display employee table data"""
  if len(filtered_df) > 0:
    st.dataframe(filtered_df, use_container_width=True, height=300)
  else:
    st.info("No employee data to display.")
  

def main():
  """Main function to run the dashboard"""
  #load data
  df = load_data()

  #create sidebar filter
  department, locations, remote_filter = create_sidebar_filter(df)

  #filtered data
  filtered_df = filter_data(df, department, locations, remote_filter)

  #display metrics
  display_metrics(filtered_df)

  #markdown
  st.markdown("---")

  display_charts(filtered_df)

  #employee filtered data
  display_table_data(filtered_df)

if __name__ == "__main__":
  main()