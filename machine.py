import streamlit as st
import json
import requests
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from streamlit_lottie import st_lottie
from sqlalchemy import create_engine

st.set_page_config(
    page_title="Dashboard",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

with open('style2.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Define the database URL
DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"

# Create the SQLAlchemy engine+
engine = create_engine(DATABASE_URL)

conn = engine.connect()

machine_data_table = pd.read_sql_table("machinedata", conn,index_col='id')

@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    data['Date'] = pd.to_datetime(data['Date']) 
    return data

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

lt_login = load_lottiefile(r"C:\Users\user\source\repos\rps_game\dash\image\login.json")

csv_file = r"D:\Machine12.csv"  
machine_data = load_data(csv_file)


users = {
    "user1": "password1",
    "user2": "password2"
}


def check_login(username, password):
    return users.get(username) == password


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""


st.sidebar.title("Menu")
if st.session_state.logged_in:
    menu = st.sidebar.selectbox(
        "Navigation",
        ["Dashboard", "Add Device", "Management", "Reports", "Support", "Logout"]
    )
else:
    menu = "Login"

col5, col6 = st.columns(2)



if menu == "Login" and not st.session_state.logged_in:
    with col5:
        st.title("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if check_login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome, {username}!")
                st.experimental_rerun()
                st.stop()
            else:
                st.error("Incorrect username or password")
    with col6:
        st.markdown(
        """
        <div style="display: flex; justify-content: center;">
            <div id="lottie-container"></div>
        </div>
        """,
        unsafe_allow_html=True
    )
        st_lottie(
            lt_login,
            loop= False,
            
            height=160,
            width=425
        )

elif st.session_state.logged_in and menu == "Dashboard":
    st.title("📈 Dashboard")

    
    col1, col2, col3, col4 = st.columns([2,2,2,2])
    
    with col1:
        st.metric(label="🌡️ Temperature", value=f"{machine_data['Tempature'].iloc[-1]} °C")
    
    with col2:
        st.metric(label="⚙️ RPM", value=f"{machine_data['RPM'].iloc[-1]}")
    
    with col3:
        st.metric(label="🎚️ Size", value=f"{machine_data['Size'].iloc[-1]}")
    
    with col4:
        st.metric(label="⏲️ Running HRS", value=f"{machine_data['Running Hours'].iloc[-1]}")

    
    st.subheader("RPM vs Temperature")
    rpm_temp_graph = go.Figure()
    #rpm_temp_graph.add_trace(go.Scatter(
       # x=machine_data_table['time'],
       # y=machine_data_table['rpm'],
       # mode='lines+markers',
       # name='RPM'
    #))
    rpm_temp_graph.add_trace(go.Scatter(
        x=machine_data_table['time'],
        y=machine_data_table['temperature'],
        mode='lines+markers',
        name='Temperature'
    ))
    st.plotly_chart(rpm_temp_graph)

   
    col1, col2 = st.columns(2)

    
    with col1:
        st.subheader("Average Metrics")
        averages = {
            'Average RPM': machine_data['RPM'].mean(),
            'Average Size': machine_data['Size'].mean(),
            'Average Hours': machine_data['Running Hours'].mean(),
            'Average Temperature': machine_data['Tempature'].mean(),
        }
        pie_chart = go.Figure(go.Pie(labels=list(averages.keys()), values=list(averages.values())))
        st.plotly_chart(pie_chart)

    with col2:
        st.subheader("Time vs Size")
        size_graph = px.line(machine_data, x='Time', y='Size', title="Size Over Time")
        st.plotly_chart(size_graph)

    
    st.subheader("Data Table")
    search_term = st.text_input("Search", "")
    if search_term:
        filtered_data = machine_data_table[machine_data_table.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
    else:
        filtered_data = machine_data_table
    st.dataframe(filtered_data, use_container_width=True)

elif st.session_state.logged_in and menu == "Add Device":
    st.title("Add Device")
    st.write("Functionality to add a new device here.")

elif st.session_state.logged_in and menu == "Management":
    st.title("Management")
    st.write("Device management functionality here.")

elif st.session_state.logged_in and menu == "Reports":
    st.title("Reports")
    st.write("Reports and analytics here.")

elif st.session_state.logged_in and menu == "Support":
    st.title("Support")
    st.write("Support page here.")

elif st.session_state.logged_in and menu == "Logout":
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.success("You have been logged out.")
    st.experimental_rerun()


elif not st.session_state.logged_in and menu != "Login":
    st.warning("Please log in to access this content.")

