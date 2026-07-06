import streamlit as st
import pandas as pd

# ১. পেজ কনফিগারেশন
st.set_page_config(page_title="Result Sheet", layout="centered")

# ২. স্টাইল (সরকারি রেজাল্ট সাইটের লুক দেওয়ার জন্য)
st.markdown("""
    <style>
        .result-box { border: 2px solid #28a745; padding: 20px; border-radius: 10px; background-color: #f9f9f9; }
        .header { text-align: center; color: #28a745; font-weight: bold; }
        .print-btn { text-align: right; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# ৩. অ্যাপের মূল অংশ
st.markdown("<h2 class='header'>Ministry of Education</h2>", unsafe_allow_html=True)
st.markdown("<h3 class='header'>Intermediate and Secondary Education Boards Bangladesh</h3>", unsafe_allow_html=True)

file_name = 'student_data.xlsx'
class_choice = st.selectbox("শ্রেণী নির্বাচন করুন:", ['৬ষ্ঠ শ্রেণী', '৭ম শ্রেণী', '৮ম শ্রেণী'])

try:
    df = pd.read_excel(file_name, sheet_name=class_choice)
    roll_input = st.number_input("রোল নম্বর লিখুন:", min_value=1, step=1)

    if st.button("ফলাফল দেখুন"):
        student = df[df['রোল নাম্বার'] == roll_input]
        
        if not student.empty:
            # রেজাল্ট প্রদর্শনের বক্স
            st.markdown("<div class='result-box'>", unsafe_allow_html=True)
            st.write(f"**নাম:** {student['নাম'].values[0]}")
            st.write(f"**রোল:** {roll_input} | **শ্রেণী:** {class_choice}")
            st.markdown("---")
            
            # টেবিল ফরম্যাট
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
