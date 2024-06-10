import mysql.connector
import streamlit as st

#connection
conn = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    passwd="",
    db="my_streamlit"
)

c=conn.cursor()

#fetch data 
def view_all_data():
    c.execute("SELECT * FROM customers ORDER BY id ASC")
    data = c.fetchall()
    return data

