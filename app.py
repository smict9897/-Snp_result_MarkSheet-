import streamlit as st
import pandas as pd
import os

# প্রয়োজনীয় লাইব্রেরি: pip install pandas openpyxl

st.set_page_config(page_title="School Portal", layout="centered")

file_name = 'student_data.xlsx'
CLASS_LIST = ['৬ষ্ঠ শ্রেণী', '৭ম শ্রেণী', '৮ম শ্রেণী']

# ---- session state ----
if "page" not in st.session_state:
    st.session_state.page = "home"

def go_home():
    st.session_state.page = "home"

def go_to_entry():
    st.session_state.page = "entry"

def go_to_student_list():
    st.session_state.page = "student_list"

def go_to_input():
    st.session_state.page = "input"

# ---------------- SHARED STYLES ----------------
st.markdown("""
    <style>
        .school-header {
            background: linear-gradient(135deg, #1a5f3f, #2d8659);
            padding: 25px 20px;
            border-radius: 8px;
            text-align: center;
            color: white;
            margin-bottom: 20px;
        }
        .school-header h1 { margin: 0; font-size: 26px; }
        .school-header h3 { margin: 5px 0 0 0; font-weight: 400; letter-spacing: 3px; }
        .card-btn button {
            width: 100%;
            height: 120px;
            background: white;
            border: 1px solid #eee;
            border-radius: 14px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            font-size: 17px;
            font-weight: 600;
            color: #222;
        }
        .summary-box {
            display: flex;
            justify-content: space-around;
            background: white;
            border-radius: 14px;
            padding: 18px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            margin-bottom: 20px;
            text-align: center;
        }
        .summary-box .num { font-size: 24px; font-weight: 700; }
        .summary-box .label { font-size: 13px; color: #666; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="school-header">
        <h1>SHARAT CHANDRA NANDALAL PUBLIC SCHOOL AND COLLEGE</h1>
        <h3>SCHOOL PORTAL</h3>
    </div>
""", unsafe_allow_html=True)

def compute_summary():
    total, failed = 0, 0
    if not os.path.exists(file_name):
        return total, 0, 0
    for cls in CLASS_LIST:
        try:
            df = pd.read_excel(file_name, sheet_name=cls)
            if 'গ্রেড' in df.columns:
                total += len(df)
                failed += df['গ্রেড'].astype(str).str.upper().eq('F').sum()
        except:
            continue
    passed = total - failed
    return total, passed, failed

# ==================== PAGE: HOME ====================
if st.session_state.page == "home":
    total, passed, failed = compute_summary()
    pass_pct = round((passed / total) * 100, 1) if total else 0
    fail_pct = round((failed / total) * 100, 1) if total else 0

    st.markdown(f"""
        <div class="summary-box">
            <div><div class="num">{total}</div><div class="label">মোট শিক্ষার্থী</div></div>
            <div><div class="num" style="color:#2d8659;">{pass_pct}%</div><div class="label">পাস</div></div>
            <div><div class="num" style="color:#c0392b;">{fail_pct}%</div><div class="label">ফেল</div></div>
        </div>
    """, unsafe_allow_html=True)

    cards = [
        ("➕", "Data Entry", go_to_entry),
        ("👥", "Student List", go_to_student_list),
        ("⚡", "Result", go_to_input),
        ("🧑‍🏫", "Our Teachers", None),
        ("📄", "Verify Certificate", None),
        ("✅", "Attendance Sheet", None),
    ]

    for i in range(0, len(cards), 2):
        row = cards[i:i+2]
        cols = st.columns(len(row))
        for col, (icon, label, action) in zip(cols, row):
            with col:
                st.markdown('<div class="card-btn">', unsafe_allow_html=True)
                clicked = st.button(f"{icon}\n\n{label}", key=label)
                st.markdown('</div>', unsafe_allow_html=True)
                if clicked and action:
                    action()
                    st.rerun()
                elif clicked:
                    st.info(f"'{label}' পেজটি এখনো তৈরি হয়নি।")

# ==================== PAGE: DATA ENTRY ====================
elif st.session_state.page == "entry":
    st.subheader("নতুন শিক্ষার্থীর তথ্য যোগ করুন")
    
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            cls = st.selectbox("শ্রেণী নির্বাচন করুন", CLASS_LIST)
            name = st.text_input("শিক্ষার্থীর নাম")
        with col2:
            roll = st.number_input("রোল নম্বর", min_value=1, step=1)
            grade = st.text_input("গ্রেড (যেমন: A, A+, F)")
        
        submitted = st.form_submit_button("তথ্য সংরক্ষণ করুন")
        
        if submitted:
            if name and grade:
                new_data = pd.DataFrame({'নাম': [name], 'রোল': [roll], 'গ্রেড': [grade]})
                
                if os.path.exists(file_name):
                    try:
                        # এক্সেল ফাইল আপডেট করা
                        with pd.ExcelWriter(file_name, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                            df_existing = pd.read_excel(file_name, sheet_name=cls)
                            df_updated = pd.concat([df_existing, new_data], ignore_index=True)
                            df_updated.to_excel(writer, sheet_name=cls, index=False)
                        st.success(f"{name}-এর তথ্য {cls}-তে সফলভাবে যুক্ত হয়েছে!")
                    except Exception as e:
                        st.error(f"ভুল হয়েছে: {e}")
                else:
                    new_data.to_excel(file_name, sheet_name=cls, index=False)
                    st.success("নতুন এক্সেল ফাইল তৈরি করে ডেটা সেভ হয়েছে!")
            else:
                st.warning("দয়া করে সব তথ্য পূরণ করুন।")

    if st.button("⬅️ হোম পেজে ফিরে যান"):
        go_home()
        st.rerun()

elif st.session_state.page == "student_list":
    st.write("এটি স্টুডেন্ট লিস্ট পেজ।")
    if st.button("⬅️ হোম পেজে ফিরে যান"):
        go_home()
        st.rerun()

elif st.session_state.page == "input":
    st.write("এটি রেজাল্ট পেজ।")
    if st.button("⬅️ হোম পেজে ফিরে যান"):
        go_home()
        st.rerun()
    
