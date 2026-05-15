import streamlit as st
import pandas as pd
import os
from datetime import date

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="centered"
)

# -------------------------------
# Load Existing Data
# -------------------------------
if "transactions" not in st.session_state:

    if os.path.exists("transactions.csv"):

        df = pd.read_csv("transactions.csv")

        st.session_state.transactions = df.to_dict("records")

    else:
        st.session_state.transactions = []

# -------------------------------
# Sidebar Navigation
# -------------------------------
st.sidebar.title("📂 Navigation")

page = st.sidebar.radio(
    "Go To",
    ["Home", "Add Transaction", "View Transactions", "Summary"]
)

# -------------------------------
# Home Page
# -------------------------------
if page == "Home":

    st.title("💰 Personal Expense Tracker")

    st.markdown("""
    ## Welcome to the Expense Tracker App

    This application helps users to:

    ✔️ Track Income  
    ✔️ Track Expenses  
    ✔️ Monitor Remaining Balance  
    ✔️ Analyze Spending Habits  
    """)

    
# -------------------------------
# Add Transaction Page
# -------------------------------
elif page == "Add Transaction":

    st.title("➕ Add Transaction")

    transaction_type = st.selectbox(
        "Select Transaction Type",
        ["Income", "Expense"]
    )

    # Income Input
    if transaction_type == "Income":

        category = st.text_input("Income Source")

    # Expense Input
    else:

        category = st.selectbox(
            "Expense Category",
            [
                "Food",
                "Travel",
                "Shopping",
                "Bills",
                "Education",
                "Medical",
                "Others"
            ]
        )

    # Integer Amount Input
    amount = int(st.number_input(
        "Enter Amount (₹)",
        min_value=1,
        step=1
    ))

    transaction_date = st.date_input(
        "Select Date",
        value=date.today()
    )

    description = st.text_area("Description")

    # Add Button
    if st.button("Add Transaction"):

        transaction = {
            "Type": transaction_type,
            "Category": category,
            "Amount": amount,
            "Date": transaction_date,
            "Description": description
        }

        # Add to session state
        st.session_state.transactions.append(transaction)

        # Save to CSV automatically
        df = pd.DataFrame(st.session_state.transactions)
        df.to_csv("transactions.csv", index=False)

        st.success("✅ Transaction Added Successfully!")

# -------------------------------
# View Transactions Page
# -------------------------------
elif page == "View Transactions":

    st.title("📜 Transaction History")

    if st.session_state.transactions:

        df = pd.DataFrame(st.session_state.transactions)

        st.dataframe(
            df,
            use_container_width=True
        )

        # Clear All Transactions
        if st.button("🗑️ Clear All Transactions"):

            st.session_state.transactions = []

            # Remove CSV data
            if os.path.exists("transactions.csv"):
                os.remove("transactions.csv")

            st.success("All transactions removed successfully!")

    else:
        st.warning("⚠️ No transactions available.")

# -------------------------------
# Summary Page
# -------------------------------
elif page == "Summary":

    st.title("📊 Financial Summary")

    if st.session_state.transactions:

        df = pd.DataFrame(st.session_state.transactions)

        # Separate Income and Expense
        income_df = df[df["Type"] == "Income"]
        expense_df = df[df["Type"] == "Expense"]

        # Calculations
        total_income = income_df["Amount"].sum()
        total_expenses = expense_df["Amount"].sum()

        balance = total_income - total_expenses

        # Summary Metrics
        col1, col2, col3 = st.columns(3)

        col1.metric("💵 Total Income", f"₹ {total_income}")
        col2.metric("💸 Total Expense", f"₹ {total_expenses}")
        col3.metric("💰 Balance", f"₹ {balance}")

        st.markdown("---")

        # Category-wise Expense Summary
        st.subheader("📌 Category-wise Expense Summary")

        if not expense_df.empty:

            category_summary = (
                expense_df.groupby("Category")["Amount"]
                .sum()
                .reset_index()
            )

            category_summary.columns = [
                "Category",
                "Total Spent (₹)"
            ]

            # Display Table
            st.table(category_summary)

            st.markdown("---")

            # Expense Analysis Chart
            st.subheader("📈 Expense Analysis Chart")

            chart_data = category_summary.set_index("Category")

            st.bar_chart(chart_data)

        else:
            st.info("No expense data available.")

    else:
        st.warning("⚠️ No transactions available.")