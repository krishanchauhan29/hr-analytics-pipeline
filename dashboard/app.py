import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="👥",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv('data/hr_processed.csv')
    return df

df = load_data()

# Sidebar
st.sidebar.image("https://img.icons8.com/color/96/conference-call.png", width=80)
st.sidebar.title("👥 HR Analytics")
st.sidebar.markdown("---")

departments = ['All'] + sorted(df['Department'].unique().tolist())
selected_dept = st.sidebar.selectbox("Select Department", departments)

age_range = st.sidebar.slider("Age Range", 
                               int(df['Age'].min()), 
                               int(df['Age'].max()), 
                               (18, 60))

# Filter
filtered = df.copy()
if selected_dept != 'All':
    filtered = filtered[filtered['Department'] == selected_dept]
filtered = filtered[(filtered['Age'] >= age_range[0]) & 
                    (filtered['Age'] <= age_range[1])]

# Header
st.title("👥 HR Analytics & Attrition Dashboard")
st.markdown("**Data-driven workforce insights for strategic HR decision making**")
st.markdown("---")

# KPIs
total = len(filtered)
attrited = filtered['Attrition'].sum()
attrition_rate = attrited / total * 100
avg_salary = filtered['MonthlyIncome'].mean()
avg_age = filtered['Age'].mean()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("👥 Total Employees", f"{total:,}")
col2.metric("⚠️ Attrited", f"{attrited:,}")
col3.metric("📉 Attrition Rate", f"{attrition_rate:.1f}%")
col4.metric("💰 Avg Salary", f"${avg_salary:,.0f}")
col5.metric("🎂 Avg Age", f"{avg_age:.1f} yrs")

st.markdown("---")

# Row 1
col1, col2 = st.columns(2)

with col1:
    dept_attr = filtered.groupby('Department')['Attrition'].mean() * 100
    fig = px.bar(x=dept_attr.index, y=dept_attr.values,
                 title='🏢 Attrition Rate by Department',
                 color=dept_attr.values,
                 color_continuous_scale='RdYlGn_r',
                 labels={'x': 'Department', 'y': 'Attrition Rate (%)'})
    fig.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    ot_attr = filtered.groupby('OverTime')['Attrition'].mean() * 100
    fig = px.bar(x=ot_attr.index, y=ot_attr.values,
                 title='⏰ Overtime Impact on Attrition',
                 color=ot_attr.values,
                 color_continuous_scale='RdYlGn_r',
                 labels={'x': 'OverTime', 'y': 'Attrition Rate (%)'},
                 text=ot_attr.values.round(1))
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    fig.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# Row 2
col1, col2 = st.columns(2)

with col1:
    role_attr = filtered.groupby('JobRole')['Attrition'].mean() * 100
    role_attr = role_attr.sort_values(ascending=True)
    fig = px.bar(x=role_attr.values, y=role_attr.index,
                 orientation='h',
                 title='💼 Attrition Rate by Job Role',
                 color=role_attr.values,
                 color_continuous_scale='RdYlGn_r',
                 labels={'x': 'Attrition Rate (%)', 'y': 'Job Role'})
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.scatter(filtered, x='MonthlyIncome', y='Age',
                     color='Attrition',
                     title='💰 Salary vs Age (Attrition Pattern)',
                     color_discrete_map={0: '#43A047', 1: '#E53935'},
                     opacity=0.6,
                     labels={'Attrition': 'Churned'})
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# Row 3
col1, col2 = st.columns(2)

with col1:
    sal_attr = filtered.groupby('SalaryGroup', observed=True)['Attrition'].mean() * 100
    fig = px.funnel(x=sal_attr.values, y=sal_attr.index,
                    title='💵 Attrition by Salary Band')
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    exp_attr = filtered.groupby('ExperienceGroup', observed=True)['Attrition'].mean() * 100
    fig = px.line(x=exp_attr.index, y=exp_attr.values,
                  title='📈 Attrition by Experience Group',
                  markers=True,
                  color_discrete_sequence=['#E53935'],
                  labels={'x': 'Experience', 'y': 'Attrition Rate (%)'})
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("**📌 Key Insights:** Sales has highest attrition (20.6%) | Overtime employees 3x more likely to leave | Low salary band: 28.6% attrition | Fresh employees (0-5 yrs) at highest risk")
st.caption("Built by Krishan Kumar Chauhan | M.Tech Data Science, GBU")