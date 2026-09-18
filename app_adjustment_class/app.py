import streamlit as st
import pandas as pd
from datetime import date

# --- Page Configuration ---
st.set_page_config(page_title="Period Cover App", page_icon="🏫", layout="wide")
# ... (rest of the code)
# --- In-Memory Database Initialization ---
if 'teachers' not in st.session_state:
    st.session_state.teachers = pd.DataFrame({
        'ID': [1, 2, 3, 4],
        'Name': ['Alice Smith', 'Bob Jones', 'Charlie Brown', 'Diana Prince'],
        'Subject': ['Mathematics', 'Science', 'English', 'History']
    })

if 'leaves' not in st.session_state:
    st.session_state.leaves = pd.DataFrame(
        columns=['Teacher ID', 'Teacher Name', 'Start Date', 'End Date', 'Status']
    )

if 'adjustments' not in st.session_state:
    st.session_state.adjustments = pd.DataFrame(
        columns=['Date', 'Period', 'Absent Teacher', 'Covering Teacher']
    )

# --- Helper Functions ---
def get_teacher_name(t_id):
    match = st.session_state.teachers[st.session_state.teachers['ID'] == t_id]
    return match['Name'].values[0] if not match.empty else "Unknown"

# --- Sidebar Navigation ---
st.sidebar.title("🏫 Period Cover")
page = st.sidebar.radio("Navigation", ["Dashboard", "Teachers", "Leaves", "Timetable Adjustments"])

# --- Views ---
if page == "Dashboard":
    st.title("Overview")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Staff", len(st.session_state.teachers))
    col2.metric("Recorded Leaves", len(st.session_state.leaves))
    col3.metric("Periods Covered", len(st.session_state.adjustments))
    
    st.subheader("Recent Adjustments")
    if st.session_state.adjustments.empty:
        st.info("No period covers assigned yet.")
    else:
        st.dataframe(st.session_state.adjustments, use_container_width=True, hide_index=True)

elif page == "Teachers":
    st.title("Teacher Directory")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.dataframe(st.session_state.teachers, use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("Add New Teacher")
        with st.form("add_teacher_form", clear_on_submit=True):
            new_id = st.session_state.teachers['ID'].max() + 1 if not st.session_state.teachers.empty else 1
            name = st.text_input("Full Name")
            subject = st.text_input("Primary Subject")
            
            if st.form_submit_button("Add Teacher"):
                if name and subject:
                    new_row = pd.DataFrame({'ID': [new_id], 'Name': [name], 'Subject': [subject]})
                    st.session_state.teachers = pd.concat([st.session_state.teachers, new_row], ignore_index=True)
                    st.rerun()
                else:
                    st.error("Please fill all fields.")

elif page == "Leaves":
    st.title("Leave Management")
    
    with st.expander("Record New Leave", expanded=True):
        with st.form("add_leave_form", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            teacher_id = col1.selectbox(
                "Select Teacher", 
                st.session_state.teachers['ID'], 
                format_func=get_teacher_name
            )
            start_date = col2.date_input("Start Date", date.today())
            end_date = col3.date_input("End Date", date.today())
            
            if st.form_submit_button("Submit Leave"):
                if end_date < start_date:
                    st.error("End date cannot be before start date.")
                else:
                    new_leave = pd.DataFrame({
                        'Teacher ID': [teacher_id], 
                        'Teacher Name': [get_teacher_name(teacher_id)],
                        'Start Date': [start_date], 
                        'End Date': [end_date], 
                        'Status': ['Approved']
                    })
                    st.session_state.leaves = pd.concat([st.session_state.leaves, new_leave], ignore_index=True)
                    st.success("Leave recorded successfully!")
                    st.rerun()
                    
    st.subheader("Leave History")
    st.dataframe(st.session_state.leaves, use_container_width=True, hide_index=True)

elif page == "Timetable Adjustments":
    st.title("Assign Period Coverage")
    
    with st.form("add_adjustment_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            date_val = st.date_input("Coverage Date", date.today())
            period = st.selectbox("Period Number", [1, 2, 3, 4, 5, 6, 7, 8])
            
        with col2:
            absent_id = st.selectbox("Absent Teacher", st.session_state.teachers['ID'], format_func=lambda x: f"{get_teacher_name(x)} (Absent)")
            cover_id = st.selectbox("Covering Teacher", st.session_state.teachers['ID'], format_func=lambda x: f"{get_teacher_name(x)} (Cover)")
        
        if st.form_submit_button("Assign Coverage"):
            if absent_id == cover_id:
                st.error("Covering teacher cannot be the same as the absent teacher.")
            else:
                new_adj = pd.DataFrame({
                    'Date': [date_val], 
                    'Period': [f"Period {period}"], 
                    'Absent Teacher': [get_teacher_name(absent_id)], 
                    'Covering Teacher': [get_teacher_name(cover_id)]
                })
                st.session_state.adjustments = pd.concat([st.session_state.adjustments, new_adj], ignore_index=True)
                st.success("Period covered successfully!")
                st.rerun()
                
    st.subheader("Coverage Log")
    st.dataframe(st.session_state.adjustments, use_container_width=True, hide_index=True)