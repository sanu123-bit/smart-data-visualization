import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Function to load data
def load_data(uploaded_file):
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith('.json'):
            df = pd.read_json(uploaded_file)
        else:
            st.error("❌ Unsupported file format. Please upload CSV, Excel, or JSON.")
            return None
        return df
    except Exception as e:
        st.error(f"⚠ Error loading file: {e}")
        return None

# Streamlit UI
st.set_page_config(page_title="📊 Smart Data Visualizer", layout="wide")
st.title("📊 Smart Data Visualizer")

# Sidebar for UI Enhancements
st.sidebar.title("⚙️ Settings")

# File uploader
uploaded_file = st.file_uploader("📂 Upload your dataset (CSV, Excel, or JSON)", type=['csv', 'xlsx', 'json'])

if uploaded_file:
    df = load_data(uploaded_file)
    
    if df is not None:
        st.subheader("📌 Data Preview")
        st.dataframe(df.head())

        # Select columns for visualization
        numeric_cols = df.select_dtypes(include=['number']).columns
        categorical_cols = df.select_dtypes(include=['object']).columns

        st.sidebar.subheader("📊 Visualization Settings")
        chart_type = st.sidebar.selectbox("Choose a Chart Type", ["Histogram", "Line Chart", "Bar Chart", "Scatter Plot", "Heatmap"])

        # Generate chart based on selection
        st.subheader(f"📈 {chart_type}")

        if chart_type == "Histogram":
            column = st.sidebar.selectbox("Select Column", numeric_cols)
            if column:
                fig = px.histogram(df, x=column, title=f"Histogram of {column}")
                st.plotly_chart(fig)

        elif chart_type == "Line Chart":
            x_col = st.sidebar.selectbox("X-axis", df.columns)
            y_col = st.sidebar.selectbox("Y-axis", numeric_cols)
            if x_col and y_col:
                fig = px.line(df, x=x_col, y=y_col, title=f"Line Chart ({x_col} vs {y_col})")
                st.plotly_chart(fig)

        elif chart_type == "Bar Chart":
            x_col = st.sidebar.selectbox("X-axis", categorical_cols)
            y_col = st.sidebar.selectbox("Y-axis", numeric_cols)
            if x_col and y_col:
                fig = px.bar(df, x=x_col, y=y_col, title=f"Bar Chart ({x_col} vs {y_col})")
                st.plotly_chart(fig)

        elif chart_type == "Scatter Plot":
            x_col = st.sidebar.selectbox("X-axis", numeric_cols)
            y_col = st.sidebar.selectbox("Y-axis", numeric_cols)
            if x_col and y_col:
                fig = px.scatter(df, x=x_col, y=y_col, title=f"Scatter Plot ({x_col} vs {y_col})")
                st.plotly_chart(fig)

        elif chart_type == "Heatmap":
            numeric_df = df.select_dtypes(include=['number'])  # Filter only numeric columns
            if numeric_df.empty:
                st.error("❌ No numeric columns found for a heatmap.")
            else:
                fig, ax = plt.subplots(figsize=(12, 6))
                sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax)
                st.pyplot(fig)

# Footer
st.sidebar.markdown("---")
st.sidebar.info("📌 Created by Sanika.")