import streamlit as st
from PIL import Image  
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",  
    "https://www.googleapis.com/auth/drive"  
]

# Load service account credentials and check API access
def connect_to_google_sheets():
    try:
        creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
        st.write("✅ Credentials are valid!")
    except Exception as e:
        st.error(f"❌ Failed to load credentials: {e}")
        return None

    # Check Google Drive API access
    try:
        drive_service = build("drive", "v3", credentials=creds)
        drive_service.files().list().execute()  # Test Drive API
        st.write("✅ Google Drive API is enabled and accessible!")
    except HttpError as e:
        st.error(f"❌ Google Drive API access failed: {e}")
        return None
    except Exception as e:
        st.error(f"❌ Google Drive API error: {e}")
        return None

    # Check Google Sheets API access
    try:
        client = gspread.authorize(creds)
        sheet = client.open("Expense-Tracker").sheet1  
        st.write("✅ Google Sheets API is enabled and accessible!")
        return sheet
    except gspread.exceptions.APIError as e:
        st.error(f"❌ Google Sheets API error: {e}")
        return None
    except gspread.exceptions.SpreadsheetNotFound:
        st.error("❌ Google Sheets API error: Spreadsheet not found. Check sharing settings!")
        return None
    except Exception as e:
        st.error(f"❌ Google Sheets API error: {e}")
        return None

def income_page():
    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    st.title("➕ Add Income")

    with st.form("income_form"):
        date = st.date_input("📅 Date", datetime.today())
        income_source = st.selectbox(
            "🏷️ Income Source",
            options=[
                "Salary",
                "Business/Side Hustle",
                "Investments",
                "Passive Income",
            ],
        )
        amount = st.number_input("💵 Amount", min_value=0.0, format="%.2f")
        submitted = st.form_submit_button("Add Income")

        if submitted:
            if amount <= 0:
                st.error("❌ Amount must be greater than 0.")
                return  

            if date > datetime.today().date():
                st.error("❌ Date cannot be in the future.")
                return  

            sheet = connect_to_google_sheets()
            if sheet is None:
                st.error("❌ Unable to connect to Google Sheets. Please check your credentials and API access.")
                return

            try:
                type_value = "income"  
                component = income_source  
                year = date.year  # Extract year from the date
                value = amount  

                sheet.append_row([type_value, component, date.strftime("%Y-%m-%d"), year, value])

                st.success("✅ Income added successfully! Click the back arrow (←) to return to the home page.")

            except Exception as e:
                st.error(f"❌ An error occurred while saving to Google Sheets: {e}")

def expense_page():
    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    st.title("➖ Add Expense")

    with st.form("expense_form"):
        date = st.date_input("📅 Date", datetime.today())
        expense_type = st.selectbox(
            "🏷️ Expense Type",
            options=[
                "Housing",
                "Food & Groceries",
                "Transportation",
                "Utilities",
                "Medical",
                "Education",
                "Shopping",
                "Subscriptions",
                "Loan & Debt Payments",
            ],
        )
        amount = st.number_input("💵 Amount", min_value=0.0, format="%.2f")
        submitted = st.form_submit_button("Add Expense")

        if submitted:
            if amount <= 0:
                st.error("❌ Amount must be greater than 0.")
                return  

            if date > datetime.today().date():
                st.error("❌ Date cannot be in the future.")
                return  

            sheet = connect_to_google_sheets()
            if sheet is None:
                st.error("❌ Unable to connect to Google Sheets. Please check your credentials and API access.")
                return

            try:
                type_value = "expense"  
                component = expense_type  
                year = date.year  
                value = amount  

                sheet.append_row([type_value, component, date.strftime("%Y-%m-%d"), year, value])

                st.success("✅ Expense added successfully! Click the back arrow (←) to return to the home page.")

            except Exception as e:
                st.error(f"❌ An error occurred while saving to Google Sheets: {e}")

def saving_page():
    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    st.title("💰 Add Saving")

    with st.form("saving_form"):
        date = st.date_input("📅 Date", datetime.today())
        saving_type = st.selectbox(
            "🏷️ Saving Type",
            options=[
                "Emergency Fund",
                "Fixed Deposits",
                "Liquid Cash",
                "Gold",
                "Property & Land",
                "Stocks & Shares",
                "Mutual Funds",
                "SIP",
            ],
        )
        amount = st.number_input("💵 Amount", min_value=0.0, format="%.2f")
        submitted = st.form_submit_button("Add Saving")

        if submitted:
            if amount <= 0:
                st.error("❌ Amount must be greater than 0.")
                return  
 
            if date > datetime.today().date():
                st.error("❌ Date cannot be in the future.")
                return  

            sheet = connect_to_google_sheets()
            if sheet is None:
                st.error("❌ Unable to connect to Google Sheets. Please check your credentials and API access.")
                return

            try:
                type_value = "saving"  
                component = saving_type  
                year = date.year  
                value = amount  
                sheet.append_row([type_value, component, date.strftime("%Y-%m-%d"), year, value])

                st.success("✅ Saving added successfully! Click the back arrow (←) to return to the home page.")

            except Exception as e:
                st.error(f"❌ An error occurred while saving to Google Sheets: {e}")

def home_page():
    st.title("💰 Personal Finance Tracker")

    st.write("Welcome to your personal finance tracker! Track your income, expenses, and savings effortlessly.")

    st.write("")  

    # Define the card layout
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            """
            <div class="card">
                <img src="https://media.istockphoto.com/id/2035474276/vector/vector-dollar-icon-set-dollar-value-vector-wallet-and-credit-card-money-spending-ideas.jpg?s=1024x1024&w=is&k=20&c=BxKkIJ0YYVG9jyAzuZOm-CEUX9us5L7r7EjQbTDtAFQ=" class="card-image">
                <p class="card-text">Income</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("➕ Add Income", key="income"):
            st.session_state.page = "income"
            st.rerun()

 
    with col2:
        st.markdown(
            """
            <div class="card">
                <img src="https://media.istockphoto.com/id/2184319854/vector/businessman-pushing-a-large-bag-of-money-filled-with-cash-and-coins-financial-growth-and.jpg?s=1024x1024&w=is&k=20&c=0yN-l6Pu-oxP1PK54Y0JjwJTYS9694-_1IdR2mR9iCc=" class="card-image">
                <p class="card-text">Expense</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("➖ Add Expense", key="expense"):
            st.session_state.page = "expense"
            st.rerun()

    with col3:
        st.markdown(
            """
            <div class="card">
                <img src="https://media.istockphoto.com/id/1363836156/vector/piggy-bank-and-gold-coin-vector-icon-pig-in-flat-style.jpg?s=612x612&w=0&k=20&c=mMyviBlK9aN167IeWSJ5RLG26PA9JF6cjhM2LcgZ9rw=" class="card-image">
                <p class="card-text">Savings</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("🪙 Add Savings", key="saving"):
            st.session_state.page = "saving"
            st.rerun()

    with col4:
        st.markdown(
            """
            <div class="card">
                <img src="https://media.istockphoto.com/id/1256810292/vector/business-people-increasing-capital-and-profits.jpg?s=1024x1024&w=is&k=20&c=q7A-J5s_oolDfPFC9ULklg7CMUjzJlCFJx_lSauhbTo=" class="card-image">
                <p class="card-text">Dashboard</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        if st.button("📊 View Dashboard", key="dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()

# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "income":
    income_page()  
elif st.session_state.page == "expense":
    expense_page()  
elif st.session_state.page == "saving":
    saving_page()    
elif st.session_state.page == "dashboard":
    st.markdown(
        """
        <a href="https://app.powerbi.com/groups/me/reports/a37762e5-254f-49e8-bc4c-5a7768de2775/bb8aa83b47656f5388c5?experience=power-bi" target="_blank">
            <img src="https://www.projectmanager.com/wp-content/uploads/2023/10/Project-Dashboard-Template-Excel-image.png" style="width:600px;height:300px;">
            <br><br>
            <button style="background-color:rgb(179, 34, 26);font-size:18px;font-weight:bold; color: white; padding: 10px 10px; border: none; border-radius: 5px; cursor: pointer;">
                📊 View Power-BI Dashboard
            </button>
        </a>
        """,
        unsafe_allow_html=True,
    )