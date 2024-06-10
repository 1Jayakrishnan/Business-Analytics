import streamlit as st
import plotly.express as px
import plotly.subplots as sp
import pandas as pd
from streamlit_extras.metric_cards import style_metric_cards
theme_ploty=None

#call connection file
from mysql_con import *

#create page config
st.set_page_config("Business analyics Dashbaord",page_icon="",layout="wide")
st.subheader("Business analyics Dashbaord")

#call css style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}<style",unsafe_allow_html=True)

#process data from query
result = view_all_data()
df=pd.DataFrame(result,columns=["EEID","FullName","JobTitle","Department","BusinessUnit","Gender","Ethnicity","Age","HireDate","AnnualSalary","Bonus","Country","City","id"])

#print dataframe
#st.dataframe(df)

#sidebar

st.sidebar.header("Filter")
department= st.sidebar.multiselect(
    label="Filter Department",
    options=df["Department"].unique(),
    default=df["Department"].unique(),
)

st.sidebar.header("Filter Country")
country=st.sidebar.multiselect(
    label="Filter Country",
    options=df["Country"].unique(),
    default=df["Country"].unique(),
)

st.sidebar.header("Filter BusinessUnit")
businessunit=st.sidebar.multiselect(
    label="Filter BusinessUnit",
    options=df["BusinessUnit"].unique(),
    default=df["BusinessUnit"].unique(),
)

#process query

df_selection=df.query(
    "Department==@department & Country==@country & BusinessUnit==@businessunit"
)

def metrics():
    col1,col2,col3=st.columns(3)
    #total customer metric
    col1.metric("Total Customers",value=df_selection.id.count(),delta="All Customers")
    #sum
    col2.metric("Annual Salary",value=f"{df_selection.AnnualSalary.sum():,.0f}",delta="Annual Salary Total")
    #max
    col3.metric("Annual Salary",value=f"{df_selection.AnnualSalary.max():,.0f}",delta="Maximum Salary")
    # Apply styles to metric cards
    style_metric_cards(background_color="#071021", border_left_color="#1f66bd")


#pie chart
div1,div2=st.columns(2)

def pie():
    with div1:
        fig=px.pie(df_selection,values="AnnualSalary",names="Department",title="Customers by Department")
        fig.update_layout(legend_title="Department",legend_y=0.8)
        fig.update_traces(textinfo="percent+label",textposition="inside")
        st.plotly_chart(fig,use_container_width=True,theme=theme_ploty)


def bar():
    with div2:
        fig=px.bar(df_selection,y="AnnualSalary",x="Department",text_auto='.2s',title="Simple Bar Graph")
        fig.update_traces(textfont_size=18,textangle=0,textposition="outside",cliponaxis=False)
        st.plotly_chart(fig,use_container_width=True,theme=theme_ploty)


def table():
    with st.expander("My Database Table"):
        shwdata=st.multiselect("Filter Dataset",df_selection.columns,default=["EEID","FullName","JobTitle","Department","BusinessUnit","Gender","Ethnicity","Age","HireDate","AnnualSalary","Bonus","Country","City","id"])
        st.dataframe(df_selection[shwdata],use_container_width=True)


#side navigation
from streamlit_option_menu import option_menu
with st.sidebar:
    selected=option_menu(
        menu_title="Main Menu",
        options=["Home","Table"],
        icons=["House","Book"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
    )

if selected=="Home":
    metrics()
    pie()
    bar()
else:
    table()
    df_selection.describe().T