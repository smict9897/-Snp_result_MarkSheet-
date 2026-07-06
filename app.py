import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(page_title="Marksheet", layout="centered")

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
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="school-header">
        <h1>SHARAT CHANDRA NANDALAL PUBLIC SCHOOL AND COLLEGE</h1>
        <h3>MARKSHEET</h3>
    </div>
""", unsafe_allow_html=True)

file_name = 'student_data.xlsx'
class_choice = st.selectbox("আপনার শ্রেণী নির্বাচন করুন:", ['৬ষ্ঠ শ্রেণী', '৭ম শ্রেণী', '৮ম শ্রেণী'])

try:
    df = pd.read_excel(file_name, sheet_name=class_choice)
    roll_input = st.number_input("রোল নম্বর লিখুন:", min_value=1, step=1)

    if st.button("ফলাফল দেখুন"):
        student = df[df['রোল নাম্বার'].astype(str) == str(int(roll_input))]

        if not student.empty:
            row = student.iloc[0]

            # Top info block, similar spirit to the board format but clearly school-branded
            st.markdown(f"""
                <table class="info-table" style="width:100%; border-collapse:collapse; margin-bottom:15px;">
                    <tr><td><b>Roll No</b></td><td>{roll_input}</td>
                        <td><b>Name</b></td><td>{row['নাম']}</td></tr>
                    <tr><td><b>Class</b></td><td>{class_choice}</td>
                        <td><b>ID</b></td><td>{row.get('আইডি', '')}</td></tr>
                </table>
            """, unsafe_allow_html=True)

            # Subject/marks as a "Grade Sheet" style table
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

            # Working print button (real JS, runs in browser)
            components.html(
                """
                <div style="text-align:right; margin-top:15px;">
                    <button onclick="window.parent.print()"
                        style="padding:8px 16px; background:#2d8659; color:white;
                               border:none; border-radius:6px; cursor:pointer;">
                        🖨️ প্রিন্ট করুন
                    </button>
                </div>
                """,
                height=60,
            )

            st.balloons()
        else:
            st.warning("এই রোল নম্বরের তথ্য পাওয়া যায়নি।")
except Exception as e:
    st.error(f"অ্যাপে সমস্যা হচ্ছে: {e}")            # টেবিল ফরম্যাট
            result_table = student.T.rename(columns={student.index[0]: 'মান'})
            st.table(result_table)
            
            # প্রিন্ট বাটন (ব্রাউজারের প্রিন্ট অপশন খুলবে)
            st.markdown("<div class='print-btn'>", unsafe_allow_html=True)
            st.button("🖨️ প্রিন্ট করুন", on_click=lambda: st.write('<script>window.print()</script>', unsafe_allow_html=True))
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            st.balloons()
        else:
            st.warning("এই রোল নম্বরের তথ্য পাওয়া যায়নি।")
except Exception as e:
    st.error(f"অ্যাপে সমস্যা হচ্ছে: {e}")
