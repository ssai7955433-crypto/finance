import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Initialize DB
conn = sqlite3.connect("finance.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                type TEXT,
                category TEXT,
                amount REAL)""")
conn.commit()

st.title("💰 Personal Finance Tracker")

menu = ["Add Transaction", "View Summary"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Transaction":
    date = st.date_input("Date")
    ttype = st.selectbox("Type", ["Income", "Expense"])
    category = st.text_input("Category")
    amount = st.number_input("Amount", min_value=0.0)
    if st.button("Save"):
        c.execute("INSERT INTO transactions(date,type,category,amount) VALUES(?,?,?,?)",
                  (str(date), ttype, category, amount))
        conn.commit()
        st.success("Transaction saved!")

elif choice == "View Summary":
    df = pd.read_sql("SELECT * FROM transactions", conn)
    st.dataframe(df)

    if not df.empty:
        income = df[df["type"]=="Income"]["amount"].sum()
        expense = df[df["type"]=="Expense"]["amount"].sum()
        balance = income - expense

        st.write(f"Total Income: {income}")
        st.write(f"Total Expense: {expense}")
        st.write(f"Balance: {balance}")

        # Pie chart
        fig, ax = plt.subplots()
        df.groupby("category")["amount"].sum().plot.pie(ax=ax, autopct='%1.1f%%')
        st.pyplot(fig)
