import streamlit as st
import mysql.connector
import datetime
import matplotlib.pyplot as plt
import numpy as np
import altair as alt
import pandas as pd
import plotly.express as px
from mysql.connector import Error
from streamlit_option_menu import option_menu
from mysql.connector import Error
from matplotlib import rc

rc('font', family='Tahoma')


def db_con():
    try:
        connection = mysql.connector.connect(host="localhost",user="root",password="",database="jodwai")
        if connection.is_connected():
            return connection
    except Error as e:
        st.error("Error connecting to DB: %s" % e)
    return None
    
def wannee():
    date_today = datetime.date.today()
    return date_today

def login():
    st.title("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Don't Have an Account?",type="tertiary"):
        st.session_state["current_page"] = "Register"  

    if st.button("Login"):
        con = db_con()
        if con:
            cursor = con.cursor()
            try:
                cursor.execute("SELECT * FROM account WHERE email = %s AND password = %s", (email, password))
                user = cursor.fetchone()
                if user:
                    st.toast('Login สำเร็จ!', icon='✅')
                    st.session_state["logged_in"] = True
                    st.session_state["email"] = email
                    st.session_state["current_page"] = "Home"
                    st.session_state["user_data"] = {"email": user[1],"name": user[3],"lastname": user[4]}
                else:
                    st.toast('Email หรือ Password ไม่ถูกต้อง', icon='⛔')
            except Error as e:
                st.error("Error: %s" % e)
            finally:
                cursor.close()
                con.close()

def register():
    st.title("📝 Register")
    name = st.text_input("Name")
    lastname = st.text_input("Lastname")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    if st.button("already have an account?",type="tertiary"):
        st.session_state["current_page"] = "Login" 
    
    if st.button("Register"):
        if not name or not lastname or not email or not password or not confirm_password:
            st.toast('กรุณากรอกข้อมูลให้ครบทุกช่อง', icon='⚠️')
        elif password != confirm_password:
            st.toast('Password และ Confirm Password ไม่ตรงกัน', icon='⚠️')
        else:
            con = db_con()
            if con:
                cursor = con.cursor()
                try:
                    cursor.execute(
                        "INSERT INTO account (email, password, name, lastname) VALUES (%s, %s, %s, %s)",
                        (email, password, name, lastname),
                    )
                    con.commit()
                    st.toast('ลงทะเบียนสำเร็จ! กรุณาเข้าสู่ระบบ', icon='📝')
                    st.session_state["current_page"] = "Login" 
                except Error as e:
                    st.error("Error: %s" % e)
                finally:
                    cursor.close()
                    con.close()
import matplotlib.pyplot as plt

def home():
    st.title("🏠 Home")
    user_data = st.session_state.get("user_data", {})
    email = st.session_state["email"]
    
    st.subheader(f"Welcome K.{user_data.get('name')} {user_data.get('lastname')} to JodWai!")
    
    st.subheader("📅 เลือกช่วงวันที่")
    start_date = st.date_input("ตั้งแต่วันที่")
    end_date = st.date_input("ถึงวันที่")
    
    if start_date > end_date:
        st.toast('วันที่เริ่มต้นต้องน้อยกว่าหรือเท่ากับวันที่สิ้นสุด',icon='⚠️')
        return
    
    con = db_con()
    if con:
        cursor = con.cursor(dictionary=True)
        try:
            cursor.execute("""SELECT type, SUM(amount) AS total FROM expense WHERE email = %s AND date BETWEEN %s AND %s GROUP BY type""", (email, start_date, end_date))
            summary = cursor.fetchall()

            cursor.execute("""SELECT description, SUM(amount) AS total FROM expense WHERE email = %s AND type = 'expense' AND date BETWEEN %s AND %s GROUP BY description""", (email, start_date, end_date))
            expense_details = cursor.fetchall()
        except Error as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")
            return
        finally:
            cursor.close()
    
    income = next((item["total"] for item in summary if item["type"] == "income"), 0)
    expense = next((item["total"] for item in summary if item["type"] == "expense"), 0)
    
    if income == 0 and expense == 0:
        st.info("ไม่มีข้อมูลรายรับหรือรายจ่ายในช่วงวันที่ที่เลือก")
        return
    labels = ["รายรับ", "รายจ่าย"]
    values = [income, expense]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.bar(labels, values, color=['#28a745', '#dc3545'], edgecolor='black', linewidth=1.5)
    ax.set_ylabel('จำนวนเงิน (บาท)', fontsize=12)
    ax.set_title('รายรับและรายจ่าย\n', fontsize=14, fontweight='bold')
    ax.set_ylim(0, max(values) + 100)  # เพิ่มขอบเขตให้แสดงค่าได้ชัดเจน
    ax.bar_label(ax.containers[0], labels=[f'{v} ฿' for v in values], fontsize=12, padding=5)

    st.subheader("\n📊 แผนภูมิแท่งรายรับและรายจ่าย")
    st.pyplot(fig)

    if expense_details:
        expense_labels = [item["description"] for item in expense_details]
        expense_values = [item["total"] for item in expense_details]

        fig, ax = plt.subplots(figsize=(6, 6))
        wedges, texts, autotexts = ax.pie(expense_values, labels=expense_labels, autopct="%1.1f%%", startangle=90, colors=plt.cm.Paired.colors)
        ax.axis("equal")  

        for text in texts:
            text.set(fontsize=12, fontweight='bold', color='#333')  # ปรับขนาดและสีข้อความ
        for autotext in autotexts:
            autotext.set(fontsize=12, color='#fff')  # ปรับขนาดและสีข้อความเปอร์เซ็นต์

        st.subheader("🍴 สัดส่วนรายจ่ายแต่ละประเภท")
        st.pyplot(fig)

    else:
        st.info("ไม่มีข้อมูลรายจ่ายแยกประเภทในช่วงวันที่ที่เลือก")


def jodwai():
    st.title("💰 บันทึกรายรับรายจ่าย")
    email = st.session_state["email"]    
    con = db_con()

    with st.form("form"):
        st.write("เพิ่มรายการใหม่")
        date = wannee()
        amount = st.number_input("จำนวนเงิน", min_value=0.0, step=0.01)
        selected_type = st.selectbox("ประเภท", ["รายรับ", "รายจ่าย"])
        expense_type = "income" if selected_type == "รายรับ" else "expense"

        if expense_type == "expense":
            description = st.selectbox("รายละเอียด", ["ค่าอาหาร", "ค่าที่พัก", "ค่าเดินทาง", "อื่น ๆ"]
            )
        else:
            description = ""

        submitted = st.form_submit_button("บันทึก")

        if submitted:
            if amount <= 0 or (expense_type == "expense" and not description.strip()):
                st.toast('กรุณากรอกข้อมูลให้ครบถ้วน',icon='✏️')
            else:
                try:
                    cursor = con.cursor()
                    cursor.execute(
                        "INSERT INTO expense (email, amount, type, description, date) VALUES (%s, %s, %s, %s, %s)",
                        (email, amount, expense_type, description, date),
                    )
                    con.commit()
                    st.toast('บันทึกรายการสำเร็จ!', icon='📋')
                except Error as e:
                    st.toast(f"เกิดข้อผิดพลาด: {e}")
                finally:
                    cursor.close()

def hantao():
    st.title("🍵 Hantao")
    st.subheader("เพิ่มค่าใช้จ่ายและดูรายงานเพื่อนร่วมทริป")

    email = st.session_state["email"]

    with st.form("add_expense_form"):
        description = st.text_area("ชื่อทริป")
        num_friends = st.number_input("จำนวนเพื่อน", min_value=1, step=1)
        
        friend_names = []
        for i in range(num_friends):
            friend_name = st.text_input(f"ชื่อเพื่อนคนที่ {i + 1}")
            friend_names.append(friend_name)

        amount = st.number_input("เงินที่ใช้จ่าย (รวมทั้งหมด)", min_value=0.0, step=0.01)
        if amount > 0 and num_friends > 0:
            per_person = amount / (num_friends + 1)
            st.info(f"ค่าใช้จ่ายทั้งหมดของทริปนี้: {amount:.2f} บาท\nแต่ละคนต้องจ่าย: {per_person:.2f} บาท")

        submitted = st.form_submit_button("บันทึก")

        if submitted:
            if all(friend_names) and amount > 0:
                con = db_con()
                if con:
                    cursor = con.cursor()
                    try:
                        for friend_name in friend_names:
                            cursor.execute("""
                                INSERT INTO hantao_friend (email, friend_name, amount, activity)VALUES (%s, %s, %s, %s)""", (email, friend_name, per_person, description))
                        con.commit()
                        st.toast("บันทึกค่าใช้จ่ายเรียบร้อยแล้ว!", icon="📋")
                    except Error as e:
                        st.error(f"เกิดข้อผิดพลาด: {e}")
                    finally:
                        cursor.close()
            else:
                st.toast("กรุณากรอกข้อมูลให้ครบถ้วน", icon="✏️")

    st.subheader("ดูรายงานเพื่อนร่วมทริป")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("วันที่เริ่มต้น")
    with col2:
        end_date = st.date_input("วันที่สิ้นสุด")

    if st.button("แสดงรายงาน"):
        if start_date > end_date:
            st.error("กรุณาเลือกช่วงวันที่ให้ถูกต้อง")
        else:
            con = db_con()
            if con:
                cursor = con.cursor(dictionary=True)
                try:
                    query = """SELECT friend_name, SUM(amount) AS total_amount FROM hantao_friend WHERE email = %s AND date BETWEEN %s AND %s GROUP BY friend_name"""
                    cursor.execute(query, (email, start_date, end_date))
                    res = cursor.fetchall()

                    if res:
                        df = pd.DataFrame(res)
                        
                        fig = px.bar(df, x="friend_name", y="total_amount", text="total_amount", title="เพื่อนที่พาคุณเสียเงินมากที่สุด")
                        fig.update_traces(texttemplate="%{text:.2f} บาท", textposition="outside")
                        fig.update_layout(yaxis_title="จำนวนเงิน (บาท)", xaxis_title="ชื่อเพื่อน")

                        st.plotly_chart(fig)
                    else:
                        st.info("ไม่มีข้อมูลในช่วงวันที่ที่เลือก")
                except Error as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
                finally:
                    cursor.close()


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    with st.sidebar:
        selected = option_menu("Main Menu",["Home", "Income,Expense","Han Tao!", "Logout"],
            icons=["house", "book" ,"cash", "box-arrow-right"],
            menu_icon="cast",
            default_index=0,)
        
    if selected == "Home":
        home()
    elif selected == "Income,Expense":
        jodwai()
    elif selected == "Han Tao!":
        hantao()
    elif selected == "Logout":
        st.session_state["logged_in"] = False
        st.session_state["current_page"] = "Login" 
else:
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Login"
    
    if st.session_state["current_page"] == "Login":
        login()
    elif st.session_state["current_page"] == "Register":
        register()
