import streamlit as st
import pandas as pd

# ১. স্কুলের নাম ও হেডার
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>SHARAT CHANDRA NANDALAL PUBLIC SCHOOL AND COLLEGE</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>M A R K S H E E T</h3>", unsafe_allow_html=True)
st.markdown("---")

# ২. ফাইল লোড করা
file_name = 'student_data.xlsx'

# ৩. শ্রেণী নির্বাচন
class_choice = st.selectbox("আপনার শ্রেণী নির্বাচন করুন:", ['৬ষ্ঠ শ্রেণী', '৭ম শ্রেণী', '৮ম শ্রেণী'])

# ৪. ডাটাফ্রেম লোড ও রেজাল্ট প্রদর্শন
try:
    df = pd.read_excel(file_name, sheet_name=class_choice)
    
    # রোল ইনপুট
    roll_input = st.number_input("আপনার রোল নাম্বার লিখুন:", min_value=1, step=1)
    
    if st.button("ফলাফল দেখুন"):
        # আপনার এক্সেল ফাইলের কলামের নাম যদি 'রোল নাম্বার' হয়, তবে এটি ঠিক আছে
        student = df[df['রোল নাম্বার'] == roll_input]
        
        if not student.empty:
            st.write(f"**নাম:** {student['নাম'].values[0]}")
            st.write(f"**ক্লাস:** {class_choice}")
            st.write(f"**রোল:** {roll_input}")
            st.markdown("---")
            
            # সব কলামের তথ্য টেবিল আকারে দেখানো
            # এটি আপনার এক্সেলের সব বিষয় অটোমেটিক নিয়ে নেবে
            st.table(student.T.rename(columns={student.index[0]: 'ফলাফল'}))
            
            st.balloons()
        else:
            st.warning("দুঃখিত, এই রোল নাম্বারের কোনো তথ্য পাওয়া যায়নি।")
            
except Exception as e:
    st.error(f"অ্যাপে সমস্যা হচ্ছে: {e}. নিশ্চিত করুন যে আপনার এক্সেল ফাইলে 'রোল নাম্বার' এবং 'নাম' কলামটি আছে।")
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
