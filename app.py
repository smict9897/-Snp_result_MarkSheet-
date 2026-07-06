import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import os

st.set_page_config(page_title="School Portal", layout="centered")

file_name = 'student_data.xlsx'
CLASS_LIST = ['৬ষ্ঠ শ্রেণী', '৭ম শ্রেণী', '৮ম শ্রেণী']

# ---- session state ----
if "page" not in st.session_state:
    st.session_state.page = "home"
if "class_choice" not in st.session_state:
    st.session_state.class_choice = None
if "roll_input" not in st.session_state:
    st.session_state.roll_input = None


def go_home():
    st.session_state.page = "home"

def go_to_input():
    st.session_state.page = "input"

def go_to_result():
    st.session_state.page = "result"

def go_to_student_list():
    st.session_state.page = "student_list"


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
        .info-table td { padding: 6px 10px; }
        .grade-table th { background-color: #2d8659; color: white; padding: 8px; }
        .grade-table td { padding: 8px; border-bottom: 1px solid #ddd; }

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
        except Exception:
            continue
        if 'গ্রেড' not in df.columns:
            continue
        total += len(df)
        failed += df['গ্রেড'].astype(str).str.upper().eq('F').sum()
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
        ("👥", "Student List", go_to_student_list),
        ("🧑‍🏫", "Our Teachers", None),
        ("📄", "Verify Certificate", None),
        ("✅", "Attendance Sheet", None),
        ("⚡", "Result", go_to_input),
        ("🔔", "Exam Schedule", None),
        ("📚", "News", None),
        ("🅡", "Routine", None),
        ("🖼️", "Gallery", None),
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
                    st.info(f"'{label}' পেজটি এখনো তৈরি হয়নি।")


# ==================== PAGE: STUDENT LIST ====================
elif st.session_state.page == "student_list":
    st.button("⬅️ হোমে ফিরে যান", on_click=go_home)
    st.subheader("শ্রেণী অনুযায়ী শিক্ষার্থী তালিকা")

    for cls in CLASS_LIST:
        try:
            df = pd.read_excel(file_name, sheet_name=cls)
        except Exception as e:
            st.warning(f"{cls}: ডেটা পাওয়া যায়নি ({e})")
            continue

        with st.expander(f"📘 {cls} — {len(df)} জন শিক্ষার্থী", expanded=False):
            display_cols = [c for c in ['রোল নাম্বার', 'আইডি', 'নাম', 'গ্রেড', 'জিপিএ'] if c in df.columns]
            if display_cols:
                st.dataframe(
                    df[display_cols].sort_values(by='রোল নাম্বার') if 'রোল নাম্বার' in display_cols else df[display_cols],
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.dataframe(df, use_container_width=True, hide_index=True)


# ==================== PAGE: INPUT ====================
elif st.session_state.page == "input":
    st.button("⬅️ হোমে ফিরে যান", on_click=go_home)

    class_choice = st.selectbox("আপনার শ্রেণী নির্বাচন করুন:", CLASS_LIST)
    roll_input = st.number_input("রোল নম্বর লিখুন:", min_value=1, step=1)

    if st.button("ফলাফল দেখুন"):
        try:
            df = pd.read_excel(file_name, sheet_name=class_choice)
            student = df[df['রোল নাম্বার'].astype(str) == str(int(roll_input))]

            if not student.empty:
                st.session_state.class_choice = class_choice
                st.session_state.roll_input = roll_input
                go_to_result()
                st.rerun()
            else:
                st.warning("এই রোল নম্বরের তথ্য পাওয়া যায়নি।")
        except Exception as e:
            st.error(f"অ্যাপে সমস্যা হচ্ছে: {e}")


# ==================== PAGE: RESULT (Marksheet) ====================
elif st.session_state.page == "result":
    class_choice = st.session_state.class_choice
    roll_input = st.session_state.roll_input

    try:
        df = pd.read_excel(file_name, sheet_name=class_choice)
        student = df[df['রোল নাম্বার'].astype(str) == str(int(roll_input))]
        row = student.iloc[0]

        st.markdown(f"""
            <table class="info-table" style="width:100%; border-collapse:collapse; margin-bottom:15px;">
                <tr><td><b>Roll No</b></td><td>{roll_input}</td>
                    <td><b>Name</b></td><td>{row['নাম']}</td></tr>
                <tr><td><b>Class</b></td><td>{class_choice}</td>
                    <td><b>ID</b></td><td>{row.get('আইডি', '')}</td></tr>
            </table>
        """, unsafe_allow_html=True)

        skip_cols = {'রোল নাম্বার', 'নাম', 'আইডি', 'পাসওয়ার্ড', 'মোট নম্বর', 'জিপিএ', 'গ্রেড'}
        subject_cols = [c for c in df.columns if c not in skip_cols]

        rows_html = "".join(
            f"<tr><td>{subj}</td><td>{row[subj]}</td></tr>" for subj in subject_cols
        )

        st.markdown(f"""
            <table class="grade-table" style="width:100%; border-collapse:collapse;">
                <tr><th style="text-align:left;">Subject</th><th style="text-align:left;">Marks</th></tr>
                {rows_html}
                <tr><td><b>মোট নম্বর</b></td><td><b>{row.get('মোট নম্বর','')}</b></td></tr>
                <tr><td><b>জিপিএ</b></td><td><b>{row.get('জিপিএ','')}</b></td></tr>
                <tr><td><b>গ্রেড</b></td><td><b>{row.get('গ্রেড','')}</b></td></tr>
            </table>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("⬅️ ফিরে যান", on_click=go_to_input)
        with col2:
            st.button("🏠 হোম", on_click=go_home)
        with col3:
            components.html(
                """
                <div style="text-align:right;">
                    <button onclick="window.parent.print()"
                        style="padding:8px 16px; background:#2d8659; color:white;
                               border:none; border-radius:6px; cursor:pointer;">
                        🖨️ প্রিন্ট
                    </button>
                </div>
                """,
                height=50,
            )

        st.balloons()

    except Exception as e:
        st.error(f"অ্যাপে সমস্যা হচ্ছে: {e}")
        st.button("⬅️ ফিরে যান", on_click=go_to_input)
