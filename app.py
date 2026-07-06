import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import os
import base64
import hashlib
from PIL import Image
import io

# ============ PAGE CONFIGURATION ============
st.set_page_config(
    page_title="School Portal - SCNPS",
    page_icon="🏫",
    layout="wide"
)

# ============ CONSTANTS ============
FILE_NAME = 'student_data.xlsx'
TEACHERS_FILE = 'teachers_data.xlsx'
CLASS_LIST = ['৬ষ্ঠ শ্রেণী', '৭ম শ্রেণী', '৮ম শ্রেণী']
SUBJECTS = ['বাংলা', 'ইংরেজি', 'গণিত', 'বিজ্ঞান', 'তথ্য ও যোগাযোগ প্রযুক্তি', 'কৃষি']

# ============ ADMIN CREDENTIALS ============
ADMIN_CREDENTIALS = {
    "admin": "admin123",
    "teacher": "teacher123",
    "principal": "principal123"
}

# ============ SESSION STATE ============
if "page" not in st.session_state:
    st.session_state.page = "home"
if "class_choice" not in st.session_state:
    st.session_state.class_choice = None
if "roll_input" not in st.session_state:
    st.session_state.roll_input = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "role" not in st.session_state:
    st.session_state.role = None
if "selected_teacher" not in st.session_state:
    st.session_state.selected_teacher = None

# ============ NAVIGATION FUNCTIONS ============
def go_home():
    st.session_state.page = "home"

def go_to_input():
    st.session_state.page = "input"

def go_to_result():
    st.session_state.page = "result"

def go_to_student_list():
    st.session_state.page = "student_list"

def go_to_teachers():
    st.session_state.page = "teachers"

def go_to_routine():
    st.session_state.page = "routine"

def go_to_data_entry():
    if st.session_state.logged_in:
        st.session_state.page = "data_entry"
    else:
        st.warning("⚠️ দয়া করে প্রথমে লগইন করুন!")
        st.session_state.page = "login"

def go_to_admin_panel():
    if st.session_state.logged_in:
        st.session_state.page = "admin_panel"
    else:
        st.warning("⚠️ দয়া করে প্রথমে লগইন করুন!")
        st.session_state.page = "login"

def go_to_login():
    st.session_state.page = "login"

def go_to_logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.page = "home"

def go_to_about():
    st.session_state.page = "about"

def go_to_teacher_entry():
    if st.session_state.logged_in:
        st.session_state.page = "teacher_entry"
    else:
        st.warning("⚠️ দয়া করে প্রথমে লগইন করুন!")
        st.session_state.page = "login"

def show_teacher_bio(teacher_name):
    st.session_state.selected_teacher = teacher_name
    st.session_state.page = "teacher_bio"

# ============ STYLES ============
def apply_styles():
    st.markdown("""
    <style>
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }
        
        .school-header {
            background: linear-gradient(135deg, #0d47a1, #1565c0);
            padding: 2rem 2rem;
            border-radius: 16px;
            text-align: center;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 8px 30px rgba(0,0,0,0.2);
            position: relative;
            overflow: hidden;
        }
        .school-header h1 {
            margin: 0;
            font-size: 2.2rem;
            font-weight: 700;
            letter-spacing: 2px;
            position: relative;
            z-index: 1;
            color: white !important;
        }
        .school-header h3 {
            margin: 0.5rem 0 0 0;
            font-weight: 400;
            letter-spacing: 4px;
            opacity: 0.9;
            position: relative;
            z-index: 1;
            color: white !important;
        }
        .school-header .sub-title {
            font-size: 0.9rem;
            letter-spacing: 2px;
            margin-top: 0.5rem;
            opacity: 0.8;
            position: relative;
            z-index: 1;
            color: white !important;
        }
        
        .card-btn {
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .card-btn:hover {
            transform: translateY(-5px);
        }
        .card-btn button {
            width: 100%;
            height: 130px;
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            font-size: 1rem;
            font-weight: 600;
            color: #1a1a1a;
            transition: all 0.3s ease;
            padding: 0.8rem;
            white-space: pre-line;
            line-height: 1.6;
        }
        .card-btn button:hover {
            border-color: #1565c0;
            box-shadow: 0 8px 25px rgba(21, 101, 192, 0.15);
            background: #f8faff;
        }
        
        .stat-card {
            background: white;
            padding: 1.5rem;
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            border: 1px solid #f0f0f0;
            transition: transform 0.3s ease;
        }
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        }
        .stat-card .number {
            font-size: 2.5rem;
            font-weight: 700;
            color: #0d47a1;
        }
        .stat-card .label {
            font-size: 0.9rem;
            color: #666;
            margin-top: 0.25rem;
        }
        
        .teacher-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #e8eef5;
            text-align: center;
            margin-bottom: 1rem;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        .teacher-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
            border-color: #0d47a1;
        }
        .teacher-card img {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid #0d47a1;
            margin-bottom: 0.5rem;
        }
        
        .bio-card {
            background: white;
            padding: 2rem;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border: 1px solid #e8eef5;
            margin: 1rem 0;
        }
        .bio-card img {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            object-fit: cover;
            border: 4px solid #0d47a1;
        }
        .bio-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            background: #f8faff;
            padding: 1.5rem;
            border-radius: 12px;
        }
        
        .section-title {
            font-size: 1.8rem;
            font-weight: 700;
            color: #0d47a1;
            margin: 2rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid #bbdefb;
        }
        .section-subtitle {
            font-size: 1.2rem;
            font-weight: 600;
            color: #1a1a1a;
            margin: 1.5rem 0 0.8rem 0;
        }
        
        .user-info {
            background: #e8f0fe;
            padding: 0.8rem 1.5rem;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 1.5rem;
            border: 1px solid #bbdefb;
        }
        .user-info span {
            font-weight: 600;
            color: #0d47a1;
        }
        
        .login-container {
            max-width: 450px;
            margin: 2rem auto;
            padding: 2.5rem;
            background: white;
            border-radius: 20px;
            box-shadow: 0 8px 40px rgba(0,0,0,0.08);
            border: 1px solid #e8eef5;
        }
        .login-container h2 {
            text-align: center;
            color: #0d47a1;
            margin-bottom: 1.5rem;
        }
        
        .grade-table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }
        .grade-table th {
            background: #0d47a1;
            color: white !important;
            padding: 1rem;
            text-align: left;
            font-weight: 600;
        }
        .grade-table td {
            padding: 0.8rem 1rem;
            border-bottom: 1px solid #f0f0f0;
            background: white;
            color: #1a1a1a !important;
        }
        .grade-table tr:last-child td {
            border-bottom: none;
        }
        .grade-table tr:nth-child(even) td {
            background: #f8faff;
        }
        
        @media (max-width: 768px) {
            .school-header h1 { font-size: 1.5rem; }
            .card-btn button { height: 100px; font-size: 0.9rem; }
            .bio-grid { grid-template-columns: 1fr; }
        }
        
        @media print {
            .no-print { display: none !important; }
            .school-header { background: #0d47a1 !important; -webkit-print-color-adjust: exact; }
            .grade-table th { background: #0d47a1 !important; -webkit-print-color-adjust: exact; }
        }
    </style>
    """, unsafe_allow_html=True)

apply_styles()

# ============ HEADER ============
st.markdown("""
    <div class="school-header">
        <h1>🏫 SHARAT CHANDRA NANDALAL</h1>
        <h3>PUBLIC SCHOOL AND COLLEGE</h3>
        <div class="sub-title">📚 SCHOOL PORTAL</div>
    </div>
""", unsafe_allow_html=True)

# ============ USER INFO BAR ============
if st.session_state.logged_in:
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        st.markdown(f"""
            <div class="user-info">
                👋 স্বাগতম, <span>{st.session_state.username}</span> ({st.session_state.role})
            </div>
        """, unsafe_allow_html=True)
    with col3:
        if st.button("🚪 লগআউট", use_container_width=True, key="logout_btn"):
            go_to_logout()
            st.rerun()

# ============ HELPER FUNCTIONS ============
def compute_summary():
    total, failed = 0, 0
    if not os.path.exists(FILE_NAME):
        return total, 0, 0
    
    for cls in CLASS_LIST:
        try:
            df = pd.read_excel(FILE_NAME, sheet_name=cls)
        except Exception:
            continue
        if 'গ্রেড' not in df.columns:
            continue
        total += len(df)
        failed += df['গ্রেড'].astype(str).str.upper().eq('F').sum()
    
    passed = total - failed
    return total, passed, failed

def load_student_data(class_name, roll_no):
    try:
        df = pd.read_excel(FILE_NAME, sheet_name=class_name)
        student = df[df['রোল নাম্বার'].astype(str) == str(int(roll_no))]
        return student if not student.empty else None
    except Exception:
        return None

def get_class_students(class_name):
    try:
        df = pd.read_excel(FILE_NAME, sheet_name=class_name)
        return df
    except Exception:
        return None

def load_teachers_data():
    if os.path.exists(TEACHERS_FILE):
        try:
            df = pd.read_excel(TEACHERS_FILE, sheet_name='Teachers')
            return df
        except Exception:
            return None
    else:
        return None

def save_teachers_data(df):
    try:
        with pd.ExcelWriter(TEACHERS_FILE, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Teachers', index=False)
        return True
    except Exception:
        return False

def calculate_gpa_and_grade(marks):
    gpa_points = []
    for mark in marks:
        if mark >= 80: gpa_points.append(5.00)
        elif mark >= 70: gpa_points.append(4.00)
        elif mark >= 60: gpa_points.append(3.50)
        elif mark >= 50: gpa_points.append(3.00)
        elif mark >= 40: gpa_points.append(2.00)
        elif mark >= 33: gpa_points.append(1.00)
        else: gpa_points.append(0.00)
    
    gpa = sum(gpa_points) / len(gpa_points) if gpa_points else 0
    
    if gpa >= 5.00: grade = "A+"
    elif gpa >= 4.00: grade = "A"
    elif gpa >= 3.50: grade = "A-"
    elif gpa >= 3.00: grade = "B"
    elif gpa >= 2.00: grade = "C"
    elif gpa >= 1.00: grade = "D"
    else: grade = "F"
    
    return round(gpa, 2), grade

def create_printable_html(student_data, class_name, roll_no):
    row = student_data.iloc[0]
    skip_cols = {'রোল নাম্বার', 'নাম', 'আইডি', 'পাসওয়ার্ড', 'মোট নম্বর', 'জিপিএ', 'গ্রেড', 'আইডি'}
    subject_cols = [c for c in student_data.columns if c not in skip_cols]
    
    marks_rows = ""
    for subj in subject_cols:
        marks_rows += f"""
            <tr>
                <td style="padding: 10px 15px; border-bottom: 1px solid #e0e0e0;">{subj}</td>
                <td style="padding: 10px 15px; border-bottom: 1px solid #e0e0e0; text-align: center;">{row[subj]}</td>
            </tr>
        """
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>মার্কশীট - {row['নাম']}</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Arial', 'Times New Roman', sans-serif;
                padding: 40px;
                background: #f5f7fa;
                color: #1a1a1a;
            }}
            .container {{
                max-width: 900px;
                margin: 0 auto;
                background: white;
                padding: 40px;
                border-radius: 16px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.08);
            }}
            .header {{
                background: linear-gradient(135deg, #0d47a1, #1565c0);
                padding: 30px;
                text-align: center;
                border-radius: 12px;
                margin-bottom: 30px;
                color: white;
            }}
            .header h1 {{ color: white !important; font-size: 26px; letter-spacing: 2px; }}
            .header h3 {{ color: white !important; font-size: 16px; font-weight: 400; letter-spacing: 3px; opacity: 0.9; }}
            .header .sub {{ color: white !important; font-size: 14px; margin-top: 5px; opacity: 0.8; }}
            
            .print-date {{
                text-align: right;
                font-size: 12px;
                color: #666;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 2px solid #e8eef5;
            }}
            
            .info-table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                background: #f8faff;
                border-radius: 10px;
                overflow: hidden;
            }}
            .info-table td {{
                padding: 12px 18px;
                border-bottom: 1px solid #e8eef5;
            }}
            .info-table .label {{
                font-weight: 600;
                background: #e8f0fe;
                width: 25%;
            }}
            
            .marks-table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            }}
            .marks-table th {{
                background: #0d47a1;
                color: white !important;
                padding: 12px 18px;
                text-align: left;
                font-weight: 600;
            }}
            .marks-table td {{
                padding: 10px 18px;
                border-bottom: 1px solid #e8eef5;
                background: white;
            }}
            .marks-table tr:nth-child(even) td {{
                background: #f8faff;
            }}
            .marks-table tr:last-child td {{
                border-bottom: none;
            }}
            
            .highlight {{
                background: #e8f0fe !important;
                font-weight: 700;
            }}
            .highlight td {{
                font-weight: 700;
                background: #e8f0fe !important;
            }}
            
            .footer {{
                text-align: center;
                margin-top: 30px;
                padding-top: 20px;
                border-top: 2px solid #e8eef5;
                font-size: 12px;
                color: #888;
            }}
            .footer p {{ margin: 3px 0; }}
            
            @media print {{
                body {{ padding: 20px; background: white; }}
                .container {{ box-shadow: none; padding: 20px; }}
                .header {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
                .marks-table th {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
                .highlight {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
                .info-table .label {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏫 SHARAT CHANDRA NANDALAL</h1>
                <h3>PUBLIC SCHOOL AND COLLEGE</h3>
                <div class="sub">🎓 MARKSHEET</div>
            </div>
            
            <div class="print-date">📅 {pd.Timestamp.now().strftime('%d/%m/%Y %I:%M %p')}</div>
            
            <table class="info-table">
                <tr>
                    <td class="label">🎯 রোল নম্বর</td>
                    <td>{roll_no}</td>
                    <td class="label">👤 নাম</td>
                    <td>{row['নাম']}</td>
                </tr>
                <tr>
                    <td class="label">📚 শ্রেণী</td>
                    <td>{class_name}</td>
                    <td class="label">🆔 আইডি</td>
                    <td>{row.get('আইডি', '')}</td>
                </tr>
            </table>
            
            <table class="marks-table">
                <tr>
                    <th style="width:70%;">📖 বিষয়</th>
                    <th style="width:30%; text-align:center;">📊 প্রাপ্ত নম্বর</th>
                </tr>
                {marks_rows}
                <tr class="highlight">
                    <td>📈 মোট নম্বর</td>
                    <td style="text-align:center;">{row.get('মোট নম্বর', '')}</td>
                </tr>
                <tr class="highlight">
                    <td>⭐ জিপিএ</td>
                    <td style="text-align:center;">{row.get('জিপিএ', '')}</td>
                </tr>
                <tr class="highlight">
                    <td>🏅 গ্রেড</td>
                    <td style="text-align:center;">{row.get('গ্রেড', '')}</td>
                </tr>
            </table>
            
            <div class="footer">
                <p>© 2026 Sharat Chandra Nandalal Public School and College</p>
                <p>This is a system generated marksheet. No signature required.</p>
            </div>
        </div>
    </body>
    </html>
    """

# ============ PAGE: HOME ============
if st.session_state.page == "home":
    total, passed, failed = compute_summary()
    pass_pct = round((passed / total) * 100, 1) if total > 0 else 0
    fail_pct = round((failed / total) * 100, 1) if total > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div class="stat-card">
                <div class="number">{total}</div>
                <div class="label">📊 মোট শিক্ষার্থী</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="stat-card">
                <div class="number" style="color:#2e7d32;">{pass_pct}%</div>
                <div class="label">✅ পাস</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="stat-card">
                <div class="number" style="color:#c62828;">{fail_pct}%</div>
                <div class="label">❌ ফেল</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    cards = [
        ("👥", "Student List", go_to_student_list),
        ("🧑‍🏫", "Our Teachers", go_to_teachers),
        ("📝", "Student Entry", go_to_data_entry),
        ("👨‍🏫", "Teacher Entry", go_to_teacher_entry),
        ("⚡", "Result", go_to_input),
        ("🅡", "Class Routine", go_to_routine),
        ("🔐", "Admin Panel", go_to_admin_panel),
        ("🔑", "Login", go_to_login),
        ("ℹ️", "About Us", go_to_about),
    ]

    for i in range(0, len(cards), 3):
        row = cards[i:i+3]
        cols = st.columns(len(row))
        for col, (icon, label, action) in zip(cols, row):
            with col:
                st.markdown('<div class="card-btn">', unsafe_allow_html=True)
                clicked = st.button(f"{icon}\n\n{label}", key=label, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                if clicked:
                    if action:
                        action()
                        st.rerun()
                    else:
                        st.info(f"ℹ️ '{label}' পেজটি এখনো তৈরি হয়নি।")

# ============ PAGE: DATA ENTRY (UPDATED WITH DELETE) ============
elif st.session_state.page == "data_entry":
    if not st.session_state.logged_in:
        st.warning("⚠️ ডেটা এন্ট্রি করতে হলে লগইন করতে হবে!")
        st.button("🔑 লগইন করুন", on_click=go_to_login)
    else:
        st.button("⬅️ হোমে ফিরে যান", on_click=go_home, use_container_width=False)
        st.markdown('<div class="section-title">📝 ডেটা এন্ট্রি</div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["➕ নতুন শিক্ষার্থী", "📊 সব শিক্ষার্থী", "🗑️ ডেটা ডিলিট"])
        
        # ========== TAB 1: ADD STUDENT ==========
        with tab1:
            with st.form("entry_form"):
                st.markdown('<div class="section-subtitle">শিক্ষার্থীর তথ্য দিন</div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    class_name = st.selectbox("শ্রেণী", CLASS_LIST)
                    roll = st.number_input("রোল নাম্বার", min_value=1, step=1)
                    name = st.text_input("শিক্ষার্থীর নাম")
                    student_id = st.text_input("🆔 আইডি (ঐচ্ছিক)")
                
                with col2:
                    st.markdown("**📖 বিষয়ভিত্তিক নম্বর**")
                    subject_marks = {}
                    cols = st.columns(2)
                    for i, subject in enumerate(SUBJECTS):
                        with cols[i % 2]:
                            subject_marks[subject] = st.number_input(
                                subject, 
                                min_value=0, 
                                max_value=100, 
                                step=1,
                                key=f"mark_{subject}"
                            )
                
                submitted = st.form_submit_button("💾 ডেটা সংরক্ষণ করুন", use_container_width=True)
                
                if submitted:
                    if name and roll:
                        marks = list(subject_marks.values())
                        total = sum(marks)
                        gpa, grade = calculate_gpa_and_grade(marks)
                        
                        data = {
                            'রোল নাম্বার': [roll],
                            'নাম': [name],
                            'আইডি': [student_id if student_id else ''],
                            **{subj: [subject_marks[subj]] for subj in SUBJECTS},
                            'মোট নম্বর': [total],
                            'জিপিএ': [gpa],
                            'গ্রেড': [grade]
                        }
                        new_data = pd.DataFrame(data)
                        
                        try:
                            if os.path.exists(FILE_NAME):
                                existing = pd.read_excel(FILE_NAME, sheet_name=class_name)
                                updated = pd.concat([existing, new_data], ignore_index=True)
                                with pd.ExcelWriter(FILE_NAME, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                                    updated.to_excel(writer, sheet_name=class_name, index=False)
                            else:
                                with pd.ExcelWriter(FILE_NAME, engine='openpyxl') as writer:
                                    new_data.to_excel(writer, sheet_name=class_name, index=False)
                            
                            st.success(f"✅ {name} এর ডেটা সফলভাবে সংরক্ষণ করা হয়েছে!")
                            st.balloons()
                        except Exception as e:
                            st.error(f"❌ ডেটা সংরক্ষণে সমস্যা: {str(e)}")
                    else:
                        st.warning("⚠️ দয়া করে নাম এবং রোল নাম্বার দিন!")
        
        # ========== TAB 2: VIEW ALL STUDENTS ==========
        with tab2:
            st.markdown('<div class="section-subtitle">সব শিক্ষার্থীর ডেটা</div>', unsafe_allow_html=True)
            if os.path.exists(FILE_NAME):
                for cls in CLASS_LIST:
                    try:
                        df = pd.read_excel(FILE_NAME, sheet_name=cls)
                        if not df.empty:
                            st.write(f"### {cls} - {len(df)} জন")
                            st.dataframe(df, use_container_width=True, hide_index=True)
                            st.write("---")
                    except:
                        pass
            else:
                st.info("📭 এখনো কোনো ডেটা নেই।")
        
        # ========== TAB 3: DELETE STUDENTS ==========
        with tab3:
            st.markdown('<div class="section-subtitle">🗑️ শিক্ষার্থী ডিলিট করুন</div>', unsafe_allow_html=True)
            
            # Check if file exists
            if not os.path.exists(FILE_NAME):
                st.warning("⚠️ কোনো ডেটা ফাইল পাওয়া যায়নি।")
            else:
                # Show current data summary
                total_students = 0
                class_counts = {}
                for cls in CLASS_LIST:
                    try:
                        df = pd.read_excel(FILE_NAME, sheet_name=cls)
                        count = len(df)
                        class_counts[cls] = count
                        total_students += count
                    except:
                        class_counts[cls] = 0
                
                st.info(f"📊 মোট {total_students} জন শিক্ষার্থীর ডেটা রয়েছে।")
                
                # Show class wise count
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("৬ষ্ঠ শ্রেণী", class_counts.get('৬ষ্ঠ শ্রেণী', 0))
                with col2:
                    st.metric("৭ম শ্রেণী", class_counts.get('৭ম শ্রেণী', 0))
                with col3:
                    st.metric("৮ম শ্রেণী", class_counts.get('৮ম শ্রেণী', 0))
                
                st.markdown("---")
                
                # ===== DELETE OPTION 1: Single Student Delete =====
                st.markdown("#### 1️⃣ একক শিক্ষার্থী ডিলিট")
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    delete_class = st.selectbox(
                        "শ্রেণী নির্বাচন করুন",
                        CLASS_LIST,
                        key="delete_class_select"
                    )
                
                # Get students from selected class
                try:
                    df_students = pd.read_excel(FILE_NAME, sheet_name=delete_class)
                    if not df_students.empty:
                        student_list = df_students['নাম'].tolist()
                        roll_list = df_students['রোল নাম্বার'].tolist()
                        student_options = [f"{roll} - {name}" for roll, name in zip(roll_list, student_list)]
                        
                        with col2:
                            selected_student = st.selectbox(
                                "শিক্ষার্থী নির্বাচন করুন",
                                student_options,
                                key="delete_student_select"
                            )
                        
                        if selected_student:
                            selected_roll = int(selected_student.split(" - ")[0])
                            selected_name = selected_student.split(" - ")[1]
                            
                            st.warning(f"⚠️ আপনি **{selected_name}** (রোল: {selected_roll}) কে ডিলিট করতে যাচ্ছেন।")
                            
                            col1, col2, col3 = st.columns([1, 1, 2])
                            with col1:
                                if st.button("🗑️ ডিলিট করুন", type="primary", key="delete_single_btn"):
                                    try:
                                        # Remove the student
                                        updated_df = df_students[df_students['রোল নাম্বার'] != selected_roll]
                                        
                                        # Save updated data
                                        with pd.ExcelWriter(FILE_NAME, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                                            updated_df.to_excel(writer, sheet_name=delete_class, index=False)
                                        
                                        st.success(f"✅ {selected_name} এর ডেটা ডিলিট করা হয়েছে!")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"❌ ডিলিট করতে সমস্যা: {str(e)}")
                    else:
                        st.info(f"📭 {delete_class} এ কোনো শিক্ষার্থী নেই।")
                except Exception as e:
                    st.info(f"📭 {delete_class} এ কোনো শিক্ষার্থী নেই।")
                
                st.markdown("---")
                
                # ===== DELETE OPTION 2: Delete All Students =====
                st.markdown("#### 2️⃣ সব শিক্ষার্থী ডিলিট")
                st.warning("⚠️ **সতর্কতা:** এই অপশনটি ব্যবহার করলে নির্বাচিত শ্রেণীর **সব** শিক্ষার্থীর ডেটা মুছে যাবে!")
                
                delete_all_class = st.selectbox(
                    "শ্রেণী নির্বাচন করুন (সব ডেটা ডিলিটের জন্য)",
                    CLASS_LIST,
                    key="delete_all_class_select"
                )
                
                # Show how many students will be deleted
                try:
                    df_to_delete = pd.read_excel(FILE_NAME, sheet_name=delete_all_class)
                    student_count = len(df_to_delete)
                    
                    if student_count > 0:
                        st.error(f"⚠️ {delete_all_class} এ **{student_count}** জন শিক্ষার্থীর ডেটা ডিলিট হবে!")
                        
                        # Confirmation checkbox
                        confirm_delete_all = st.checkbox(
                            f"✅ আমি নিশ্চিত যে {delete_all_class} এর সব ডেটা ডিলিট করতে চাই",
                            key="confirm_delete_all"
                        )
                        
                        if confirm_delete_all:
                            if st.button("🗑️ সব ডেটা ডিলিট করুন", type="primary", key="delete_all_btn"):
                                try:
                                    # Create empty dataframe with same columns
                                    empty_df = pd.DataFrame(columns=df_to_delete.columns)
                                    
                                    # Save empty dataframe
                                    with pd.ExcelWriter(FILE_NAME, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                                        empty_df.to_excel(writer, sheet_name=delete_all_class, index=False)
                                    
                                    st.success(f"✅ {delete_all_class} এর সব ডেটা ডিলিট করা হয়েছে!")
                                    st.balloons()
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ ডেটা ডিলিট করতে সমস্যা: {str(e)}")
                    else:
                        st.info(f"📭 {delete_all_class} এ কোনো শিক্ষার্থী নেই।")
                except Exception as e:
                    st.info(f"📭 {delete_all_class} এ কোনো শিক্ষার্থী নেই।")
                
                st.markdown("---")
                
                # ===== DELETE OPTION 3: Delete Entire File =====
                st.markdown("#### 3️⃣ সম্পূর্ণ ফাইল ডিলিট")
                st.error("⚠️ **সতর্কতা:** এই অপশনটি ব্যবহার করলে **সব শ্রেণীর** সব ডেটা মুছে যাবে!")
                
                confirm_delete_file = st.checkbox(
                    "✅ আমি নিশ্চিত যে সমস্ত ডেটা ডিলিট করতে চাই",
                    key="confirm_delete_file"
                )
                
                if confirm_delete_file:
                    if st.button("🗑️ সম্পূর্ণ ডেটাবেস ডিলিট করুন", type="primary", key="delete_file_btn"):
                        try:
                            if os.path.exists(FILE_NAME):
                                os.remove(FILE_NAME)
                                st.success("✅ সম্পূর্ণ ডেটাবেস ডিলিট করা হয়েছে!")
                                st.balloons()
                                st.rerun()
                            else:
                                st.warning("⚠️ কোনো ডেটা ফাইল পাওয়া যায়নি।")
                        except Exception as e:
                            st.error(f"❌ ডেটা ডিলিট করতে সমস্যা: {str(e)}")

# ============ PAGE: TEACHER ENTRY ============
elif st.session_state.page == "teacher_entry":
    if not st.session_state.logged_in:
        st.warning("⚠️ শিক্ষক এন্ট্রি করতে হলে লগইন করতে হবে!")
        st.button("🔑 লগইন করুন", on_click=go_to_login)
    else:
        st.button("⬅️ হোমে ফিরে যান", on_click=go_home, use_container_width=False)
        st.markdown('<div class="section-title">👨‍🏫 শিক্ষক এন্ট্রি</div>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["➕ নতুন শিক্ষক যোগ করুন", "📊 সব শিক্ষকের তালিকা"])
        
        with tab1:
            with st.form("teacher_entry_form", clear_on_submit=True):
                st.markdown('<div class="section-subtitle">শিক্ষকের তথ্য দিন</div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("👤 শিক্ষকের নাম *", placeholder="ড. মোঃ রহিম উদ্দিন")
                    position = st.text_input("📌 পদবি *", placeholder="অধ্যক্ষ")
                    subject = st.text_input("📖 বিষয় *", placeholder="গণিত")
                    mobile = st.text_input("📞 মোবাইল নম্বর", placeholder="০১৭১২-৩৪৫৬৭৮")
                    email = st.text_input("📧 ইমেইল", placeholder="principal@school.com")
                
                with col2:
                    qualification = st.text_area("🎓 শিক্ষাগত যোগ্যতা", placeholder="পিএইচডি (গণিত), এমএসসি (গণিত)")
                    experience = st.text_input("💼 অভিজ্ঞতা", placeholder="২৫ বছর")
                    joining_date = st.date_input("📅 জয়েনিং তারিখ")
                    address = st.text_area("📍 ঠিকানা", placeholder="ঢাকা, বাংলাদেশ")
                    
                    uploaded_file = st.file_uploader(
                        "📸 শিক্ষকের ছবি আপলোড করুন (JPG, PNG)",
                        type=['jpg', 'jpeg', 'png'],
                        help="শিক্ষকের পাসপোর্ট সাইজ ছবি আপলোড করুন"
                    )
                
                submitted = st.form_submit_button("💾 শিক্ষক সংরক্ষণ করুন", use_container_width=True)
                
                if submitted:
                    if name and position and subject:
                        df = load_teachers_data()
                        
                        if df is None:
                            df = pd.DataFrame(columns=[
                                'নাম', 'পদবি', 'বিষয়', 'মোবাইল', 'ইমেইল',
                                'শিক্ষাগত যোগ্যতা', 'অভিজ্ঞতা', 'জয়েনিং তারিখ', 'ঠিকানা', 'ছবি'
                            ])
                        
                        photo_data = ""
                        if uploaded_file is not None:
                            image = Image.open(uploaded_file)
                            image = image.resize((200, 200))
                            buffered = io.BytesIO()
                            image.save(buffered, format="JPEG", quality=80)
                            img_str = base64.b64encode(buffered.getvalue()).decode()
                            photo_data = f"data:image/jpeg;base64,{img_str}"
                        
                        new_teacher = pd.DataFrame({
                            'নাম': [name],
                            'পদবি': [position],
                            'বিষয়': [subject],
                            'মোবাইল': [mobile],
                            'ইমেইল': [email],
                            'শিক্ষাগত যোগ্যতা': [qualification],
                            'অভিজ্ঞতা': [experience],
                            'জয়েনিং তারিখ': [joining_date.strftime('%d/%m/%Y')],
                            'ঠিকানা': [address],
                            'ছবি': [photo_data]
                        })
                        
                        updated_df = pd.concat([df, new_teacher], ignore_index=True)
                        
                        if save_teachers_data(updated_df):
                            st.success(f"✅ {name} এর তথ্য সফলভাবে সংরক্ষণ করা হয়েছে!")
                            st.balloons()
                    else:
                        st.warning("⚠️ দয়া করে নাম, পদবি এবং বিষয় দিন!")
        
        with tab2:
            st.markdown('<div class="section-subtitle">সব শিক্ষকের তালিকা</div>', unsafe_allow_html=True)
            df = load_teachers_data()
            
            if df is not None and not df.empty:
                st.write(f"**মোট শিক্ষক:** {len(df)} জন")
                display_df = df.copy()
                if 'ছবি' in display_df.columns:
                    display_df = display_df.drop(columns=['ছবি'])
                st.dataframe(display_df, use_container_width=True, hide_index=True)
                
                st.markdown("---")
                st.subheader("🗑️ শিক্ষক ডিলিট করুন")
                
                teacher_to_delete = st.selectbox(
                    "ডিলিট করতে শিক্ষকের নাম নির্বাচন করুন",
                    df['নাম'].tolist() if not df.empty else []
                )
                
                if st.button("🗑️ ডিলিট করুন", type="primary", use_container_width=True):
                    if teacher_to_delete:
                        updated_df = df[df['নাম'] != teacher_to_delete]
                        if save_teachers_data(updated_df):
                            st.success(f"✅ {teacher_to_delete} এর তথ্য ডিলিট করা হয়েছে!")
                            st.rerun()
            else:
                st.info("📭 এখনো কোনো শিক্ষকের তথ্য নেই। উপরের ফর্ম ব্যবহার করে যোগ করুন।")

# ============ PAGE: TEACHERS ============
elif st.session_state.page == "teachers":
    st.button("⬅️ হোমে ফিরে যান", on_click=go_home, use_container_width=False)
    st.markdown('<div class="section-title">🧑‍🏫 আমাদের শিক্ষকবৃন্দ</div>', unsafe_allow_html=True)
    
    df_teachers = load_teachers_data()
    
    if df_teachers is not None and not df_teachers.empty:
        st.info("💡 **শিক্ষকের কার্ডে ক্লিক করে বিস্তারিত তথ্য দেখুন।**")
        
        cols = st.columns(3)
        for idx, (_, teacher) in enumerate(df_teachers.iterrows()):
            with cols[idx % 3]:
                if 'ছবি' in teacher and pd.notna(teacher['ছবি']) and teacher['ছবি']:
                    img_html = f'<img src="{teacher["ছবি"]}" alt="{teacher["নাম"]}" style="width:100px;height:100px;border-radius:50%;object-fit:cover;border:3px solid #0d47a1;margin-bottom:0.5rem;">'
                else:
                    img_html = f'''
                        <div style="width:100px;height:100px;background:#0d47a1;border-radius:50%;margin:0 auto 0.5rem auto;display:flex;align-items:center;justify-content:center;color:white;font-size:2.5rem;font-weight:700;border:3px solid #0d47a1;">
                            {teacher['নাম'][0]}
                        </div>
                    '''
                
                st.markdown(f"""
                    <div class="teacher-card">
                        {img_html}
                        <h4 style="margin: 0.5rem 0 0 0; color: #0d47a1;">{teacher['নাম']}</h4>
                        <p style="margin: 0.25rem 0; color: #666; font-size: 0.9rem;">
                            {teacher['পদবি']}
                        </p>
                        <p style="margin: 0; color: #888; font-size: 0.85rem;">
                            📖 {teacher['বিষয়']}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"📋 বিস্তারিত দেখুন", key=f"bio_{teacher['নাম']}", use_container_width=True):
                    show_teacher_bio(teacher['নাম'])
                    st.rerun()
    else:
        st.warning("⚠️ শিক্ষকদের ডেটাবেস পাওয়া যায়নি।")

# ============ PAGE: TEACHER BIO ============
elif st.session_state.page == "teacher_bio":
    st.button("⬅️ শিক্ষকদের পৃষ্ঠায় ফিরে যান", on_click=go_to_teachers, use_container_width=False)
    
    teacher_name = st.session_state.selected_teacher
    df_teachers = load_teachers_data()
    
    if df_teachers is not None and not df_teachers.empty:
        teacher = df_teachers[df_teachers['নাম'] == teacher_name]
        
        if not teacher.empty:
            row = teacher.iloc[0]
            
            if 'ছবি' in row and pd.notna(row['ছবি']) and row['ছবি']:
                img_html = f'<img src="{row["ছবি"]}" alt="{row["নাম"]}" style="width:150px;height:150px;border-radius:50%;object-fit:cover;border:4px solid #0d47a1;">'
            else:
                img_html = f'''
                    <div style="width:150px;height:150px;background:#0d47a1;border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;font-size:4rem;font-weight:700;border:4px solid #0d47a1;">
                        {row['নাম'][0]}
                    </div>
                '''
            
            st.markdown(f"""
                <div class="bio-card">
                    <div style="display: flex; align-items: center; gap: 2rem; margin-bottom: 1.5rem; flex-wrap: wrap;">
                        {img_html}
                        <div>
                            <h2 style="margin: 0; color: #0d47a1;">{row['নাম']}</h2>
                            <p style="margin: 0; color: #666; font-size: 1.1rem;">
                                {row['পদবি']} | {row['বিষয়']}
                            </p>
                        </div>
                    </div>
                    
                    <div class="bio-grid">
                        <div><b>📞 মোবাইল:</b> {row.get('মোবাইল', 'N/A')}</div>
                        <div><b>📧 ইমেইল:</b> {row.get('ইমেইল', 'N/A')}</div>
                        <div><b>🎓 শিক্ষাগত যোগ্যতা:</b> {row.get('শিক্ষাগত যোগ্যতা', 'N/A')}</div>
                        <div><b>💼 অভিজ্ঞতা:</b> {row.get('অভিজ্ঞতা', 'N/A')}</div>
                        <div><b>📅 জয়েনিং তারিখ:</b> {row.get('জয়েনিং তারিখ', 'N/A')}</div>
                        <div><b>📍 ঠিকানা:</b> {row.get('ঠিকানা', 'N/A')}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error("❌ শিক্ষকের তথ্য পাওয়া যায়নি।")
    else:
        st.warning("⚠️ শিক্ষকদের ডেটাবেস পাওয়া যায়নি।")

# ============ PAGE: ABOUT ============
elif st.session_state.page == "about":
    st.button("⬅️ হোমে ফিরে যান", on_click=go_home, use_container_width=False)
    st.markdown('<div class="section-title">🏫 প্রতিষ্ঠান সম্পর্কে</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div style="background: #f8faff; padding: 2rem; border-radius: 16px; border: 1px solid #e8eef5;">
            <p style="font-size: 1.05rem; line-height: 1.8;">
                <b>Sharat Chandra Nandalal Public School and College</b> এর অতীত গৌরবোজ্জ্বল 
                বর্তমান প্রশংসনীয়। ২০২৩ ইংরেজীর ২০ শে জানুয়ারী প্রতিষ্ঠিত এই শিক্ষাপ্রতিষ্ঠানটি 
                স্থানীয় ম্যাজিষ্ট্রেট অফিসের তৎকালীন প্রধান কার্যনির্বাহী কর্তৃক প্রতিষ্ঠিত হয়।
            </p>
        </div>
    """, unsafe_allow_html=True)

# ============ PAGE: STUDENT LIST ============
elif st.session_state.page == "student_list":
    st.button("⬅️ হোমে ফিরে যান", on_click=go_home, use_container_width=False)
    st.markdown('<div class="section-title">📋 শিক্ষার্থী তালিকা</div>', unsafe_allow_html=True)

    if not os.path.exists(FILE_NAME):
        st.warning("⚠️ ডেটা ফাইল পাওয়া যায়নি।")
    else:
        for cls in CLASS_LIST:
            df = get_class_students(cls)
            if df is None:
                st.warning(f"{cls}: ডেটা পাওয়া যায়নি")
                continue

            with st.expander(f"📘 {cls} — {len(df)} জন শিক্ষার্থী", expanded=False):
                display_cols = [c for c in ['রোল নাম্বার', 'আইডি', 'নাম', 'গ্রেড', 'জিপিএ'] if c in df.columns]
                if display_cols:
                    sorted_df = df[display_cols].sort_values(by='রোল নাম্বার') if 'রোল নাম্বার' in display_cols else df[display_cols]
                    st.dataframe(sorted_df, use_container_width=True, hide_index=True, height=300)
                else:
                    st.dataframe(df, use_container_width=True, hide_index=True)

# ============ PAGE: LOGIN ============
elif st.session_state.page == "login":
    st.markdown("""
        <div class="login-container">
            <h2>🔐 অ্যাডমিন লগইন</h2>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("👤 ইউজারনেম", placeholder="Enter username")
        password = st.text_input("🔑 পাসওয়ার্ড", type="password", placeholder="Enter password")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            login_btn = st.form_submit_button("🔓 লগইন করুন", use_container_width=True)
        with col2:
            if st.form_submit_button("🏠 হোম", use_container_width=True):
                go_home()
                st.rerun()
        
        if login_btn:
            if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                if username == "admin":
                    st.session_state.role = "অ্যাডমিন"
                elif username == "teacher":
                    st.session_state.role = "শিক্ষক"
                elif username == "principal":
                    st.session_state.role = "প্রধান শিক্ষক"
                else:
                    st.session_state.role = "ইউজার"
                go_home()
                st.rerun()
            else:
                st.error("❌ ভুল ইউজারনেম বা পাসওয়ার্ড!")
    
    st.markdown("""
        <div style="text-align: center; margin-top: 20px; padding: 15px; background: #f5f7fa; border-radius: 10px;">
            <p style="font-size: 14px; color: #666;">📌 ডেমো অ্যাকাউন্ট:</p>
            <p style="font-size: 13px; color: #333;">
                <b>অ্যাডমিন:</b> admin / admin123<br>
                <b>শিক্ষক:</b> teacher / teacher123
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============ PAGE: ROUTINE ============
elif st.session_state.page == "routine":
    st.button("⬅️ হোমে ফিরে যান", on_click=go_home, use_container_width=False)
    st.markdown('<div class="section-title">🅡 ক্লাস রুটিন</div>', unsafe_allow_html=True)
    
    routine_data = {
        "দিন": ["শনিবার", "রবিবার", "সোমবার", "মঙ্গলবার", "বুধবার", "বৃহস্পতিবার"],
        "১ম পিরিয়ড": ["বাংলা", "গণিত", "ইংরেজি", "বাংলা", "গণিত", "ইংরেজি"],
        "২য় পিরিয়ড": ["গণিত", "ইংরেজি", "বাংলা", "গণিত", "ইংরেজি", "বাংলা"],
        "৩য় পিরিয়ড": ["ইংরেজি", "বাংলা", "গণিত", "ইংরেজি", "বাংলা", "গণিত"],
        "৪র্থ পিরিয়ড": ["বিজ্ঞান", "বাংলা", "গণিত", "বিজ্ঞান", "বাংলা", "গণিত"],
    }
    df_routine = pd.DataFrame(routine_data)
    st.dataframe(df_routine, use_container_width=True, hide_index=True)

# ============ PAGE: ADMIN PANEL ============
elif st.session_state.page == "admin_panel":
    if not st.session_state.logged_in:
        st.warning("⚠️ দয়া করে প্রথমে লগইন করুন!")
        st.button("🔑 লগইন করুন", on_click=go_to_login)
    else:
        st.button("⬅️ হোমে ফিরে যান", on_click=go_home, use_container_width=False)
        st.markdown('<div class="section-title">🔐 অ্যাডমিন প্যানেল</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="user-info">
                👋 স্বাগতম, <span>{st.session_state.username}</span> ({st.session_state.role})
            </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["📊 ড্যাশবোর্ড", "👥 ইউজার ম্যানেজ", "⚙️ সেটিংস"])
        
        with tab1:
            st.markdown('<div class="section-subtitle">📊 ড্যাশবোর্ড</div>', unsafe_allow_html=True)
            
            total_students = 0
            for cls in CLASS_LIST:
                try:
                    df = pd.read_excel(FILE_NAME, sheet_name=cls)
                    total_students += len(df)
                except:
                    pass
            
            df_teachers = load_teachers_data()
            total_teachers = len(df_teachers) if df_teachers is not None else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📚 মোট শ্রেণী", len(CLASS_LIST))
            with col2:
                st.metric("👨‍🎓 মোট শিক্ষার্থী", total_students)
            with col3:
                st.metric("👨‍🏫 মোট শিক্ষক", total_teachers)
        
        with tab2:
            st.markdown('<div class="section-subtitle">👥 ইউজার ম্যানেজমেন্ট</div>', unsafe_allow_html=True)
            user_data = pd.DataFrame({
                "ইউজারনেম": list(ADMIN_CREDENTIALS.keys()),
                "পাসওয়ার্ড": ["••••••••"] * len(ADMIN_CREDENTIALS)
            })
            st.dataframe(user_data, use_container_width=True, hide_index=True)
        
        with tab3:
            st.markdown('<div class="section-subtitle">⚙️ সেটিংস</div>', unsafe_allow_html=True)
            if os.path.exists(FILE_NAME):
                file_size = os.path.getsize(FILE_NAME)
                st.success(f"✅ ডেটা ফাইল পাওয়া গেছে! ({file_size / 1024:.2f} KB)")
            else:
                st.error("❌ ডেটা ফাইল পাওয়া যায়নি!")

# ============ PAGE: INPUT ============
elif st.session_state.page == "input":
    col1, col2 = st.columns([3, 1])
    with col1:
        st.button("⬅️ হোমে ফিরে যান", on_click=go_home, use_container_width=False)
    
    st.markdown('<div class="section-title">🔍 ফলাফল দেখুন</div>', unsafe_allow_html=True)
    
    if not os.path.exists(FILE_NAME):
        st.error("❌ ডেটা ফাইল পাওয়া যায়নি।")
    else:
        col1, col2 = st.columns([1, 1])
        with col1:
            class_choice = st.selectbox("শ্রেণী নির্বাচন করুন:", CLASS_LIST, key="class_select")
        with col2:
            roll_input = st.number_input("রোল নম্বর লিখুন:", min_value=1, step=1, key="roll_input_field")
        
        if st.button("🔍 ফলাফল দেখুন", use_container_width=True):
            try:
                roll_number = int(roll_input)
                student = load_student_data(class_choice, roll_number)
                if student is not None:
                    st.session_state.class_choice = class_choice
                    st.session_state.roll_input = roll_number
                    go_to_result()
                    st.rerun()
                else:
                    st.warning("⚠️ এই রোল নম্বরের তথ্য পাওয়া যায়নি।")
            except ValueError:
                st.error("❌ দয়া করে একটি বৈধ রোল নম্বর দিন।")

# ============ PAGE: RESULT ============
elif st.session_state.page == "result":
    if st.session_state.class_choice is None or st.session_state.roll_input is None:
        st.error("❌ তথ্য পাওয়া যায়নি।")
        if st.button("⬅️ ফিরে যান", on_click=go_to_input):
            st.rerun()
    else:
        class_choice = st.session_state.class_choice
        roll_input = st.session_state.roll_input
        
        try:
            if not os.path.exists(FILE_NAME):
                st.error("❌ ডেটা ফাইল পাওয়া যায়নি।")
                st.button("⬅️ ফিরে যান", on_click=go_to_input)
            else:
                df = pd.read_excel(FILE_NAME, sheet_name=class_choice)
                student = df[df['রোল নাম্বার'].astype(str) == str(int(roll_input))]
                
                if student.empty:
                    st.error("❌ তথ্য পাওয়া যায়নি।")
                    st.button("⬅️ ফিরে যান", on_click=go_to_input)
                else:
                    row = student.iloc[0]
                    
                    st.markdown(f"""
                        <div style="background: #f8faff; padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; border: 1px solid #e8eef5;">
                            <table style="width:100%; border-collapse:collapse;">
                                <tr>
                                    <td><b>🎯 রোল নম্বর</b></td>
                                    <td>{roll_input}</td>
                                    <td><b>👤 নাম</b></td>
                                    <td>{row['নাম']}</td>
                                </tr>
                                <tr>
                                    <td><b>📚 শ্রেণী</b></td>
                                    <td>{class_choice}</td>
                                    <td><b>🆔 আইডি</b></td>
                                    <td>{row.get('আইডি', '')}</td>
                                </tr>
                            </table>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    skip_cols = {'রোল নাম্বার', 'নাম', 'আইডি', 'পাসওয়ার্ড', 'মোট নম্বর', 'জিপিএ', 'গ্রেড', 'আইডি'}
                    subject_cols = [c for c in df.columns if c not in skip_cols]
                    
                    marks_html = ""
                    for subj in subject_cols:
                        marks_html += f"<tr><td>{subj}</td><td>{row[subj]}</td></tr>"
                    
                    st.markdown(f"""
                        <table class="grade-table">
                            <tr><th>📖 বিষয়</th><th>📊 প্রাপ্ত নম্বর</th></tr>
                            {marks_html}
                            <tr style="font-weight: 700; background: #e8f0fe;">
                                <td>📈 মোট নম্বর</td>
                                <td>{row.get('মোট নম্বর', '')}</td>
                            </tr>
                            <tr style="font-weight: 700; background: #e8f0fe;">
                                <td>⭐ জিপিএ</td>
                                <td>{row.get('জিপিএ', '')}</td>
                            </tr>
                            <tr style="font-weight: 700; background: #e8f0fe;">
                                <td>🏅 গ্রেড</td>
                                <td>{row.get('গ্রেড', '')}</td>
                            </tr>
                        </table>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                    st.markdown('<div class="section-subtitle">🖨️ প্রিন্ট অপশন</div>', unsafe_allow_html=True)
                    
                    print_html = create_printable_html(student, class_choice, roll_input)
                    b64 = base64.b64encode(print_html.encode()).decode()
                    href = f'data:text/html;base64,{b64}'
                    
                    col1, col2, col3 = st.columns([1, 1, 1])
                    
                    with col1:
                        components.html(
                            """
                            <div style="text-align:center;">
                                <button onclick="window.print()"
                                    style="width:100%; padding: 12px; background: #0d47a1; 
                                           color: white; border: none; border-radius: 10px; 
                                           cursor: pointer; font-size: 16px; font-weight: 600;
                                           box-shadow: 0 4px 15px rgba(13, 71, 161, 0.3);">
                                    🖨️ ডাইরেক্ট প্রিন্ট
                                </button>
                            </div>
                            """,
                            height=60,
                        )
                    
                    with col2:
                        st.markdown(f"""
                            <div style="text-align:center;">
                                <a href="{href}" target="_blank"
                                    style="display: inline-block; width: 100%; padding: 12px; 
                                           background: #1565c0; color: white; border: none; 
                                           border-radius: 10px; cursor: pointer; font-size: 16px; 
                                           font-weight: 600; text-decoration: none; text-align: center;
                                           box-shadow: 0 4px 15px rgba(21, 101, 192, 0.3);">
                                    📄 নতুন উইন্ডোতে প্রিন্ট
                                </a>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        st.download_button(
                            label="📥 PDF ডাউনলোড",
                            data=print_html,
                            file_name=f"marksheet_{row['নাম']}_{roll_input}.html",
                            mime="text/html",
                            use_container_width=True,
                        )
                    
                    st.info("💡 **টিপ:** 'ডাইরেক্ট প্রিন্ট' বাটনে ক্লিক করুন অথবা Ctrl+P (Windows) / Cmd+P (Mac) চাপুন।")
                    
                    st.markdown("---")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("⬅️ ফিরে যান", use_container_width=True):
                            go_to_input()
                            st.rerun()
                    with col2:
                        if st.button("🏠 হোম", use_container_width=True):
                            go_home()
                            st.rerun()
                    with col3:
                        if st.button("🔄 নতুন অনুসন্ধান", use_container_width=True):
                            go_to_input()
                            st.rerun()
                    
                    st.balloons()
                    
        except Exception as e:
            st.error(f"❌ সমস্যা: {str(e)}")
            st.button("⬅️ ফিরে যান", on_click=go_to_input, use_container_width=True)

# ============ FOOTER ============
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; font-size: 13px; padding: 1rem;">
        © 2026 Sharat Chandra Nandalal Public School and College
    </div>
""", unsafe_allow_html=True)
