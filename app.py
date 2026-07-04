import streamlit as st
import pandas as pd

# স্কুলের নাম ও হেডার
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>SHARAT CHANDRA NANDALAL PUBLIC SCHOOL AND COLLEGE</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>M A R K S H E E T</h3>", unsafe_allow_html=True)
st.markdown("---")

# ফাইল লোড করা
file_name = 'student_data.xlsx'

# শ্রেণী নির্বাচন
class_choice = st.selectbox("আপনার শ্রেণী নির্বাচন করুন:", ['৬ষ্ঠ শ্রেণী', '৭ম শ্রেণী', '৮ম শ্রেণী'])

# ডাটাফ্রেম লোড করা
try:
    df = pd.read_excel(file_name, sheet_name=class_choice)
    
    # রোল ইনপুট
    roll_input = st.number_input("আপনার রোল নাম্বার লিখুন:", min_value=1, step=1)
    
    if st.button("ফলাফল দেখুন"):
        # আপনার এক্সেল ফাইলের কলামের নাম যদি 'রোল নাম্বার' হয়, তবে এখানে সেটি লিখুন
        student = df[df['রোল নাম্বার'] == roll_input]
        
        if not student.empty:
            st.write(f"**Name:** {student['নাম'].values[0]}")
            st.write(f"**Class:** {class_choice}  |  **Roll:** {roll_input}")
            st.markdown("---")
            
            # বিষয়সমূহ (আপনার এক্সেলের কলামের নাম অনুযায়ী)
            subjects = ['বাংলা', 'ইংরেজি', 'গণিত', 'বিজ্ঞান'] 
            marks_data = []
            for sub in subjects:
                if sub in student.columns:
                    marks = student[sub].values[0]
                    marks_data.append({
                        "Subject": sub,
                        "Full Marks": 100,
                        "Obt. Marks": marks,
                        "Percent": f"{marks}%"
                    })
            
            marks_df = pd.DataFrame(marks_data)
            st.table(marks_df)
            
            total_obt = marks_df['Obt. Marks'].sum()
            st.write(f"### Total Obtained Marks: {total_obt} / {len(marks_df)*100}")
        else:
            st.warning("দুঃখিত, এই রোল নাম্বারের কোনো তথ্য পাওয়া যায়নি।")
            
except Exception as e:
    st.error(f"এরর দেখা দিয়েছে: {e}")
