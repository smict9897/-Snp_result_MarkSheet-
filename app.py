import streamlit as st
import pandas as pd
import os

# কোডের শুরুতে বর্তমান ডিরেক্টরি চেক করা
current_path = os.getcwd()

# ফাইল লোড করার লাইনটি এভাবে লিখুন:
file_name = 'student_data.xlsx'

if os.path.exists(file_name):
    try:
        # এখানে আপনার শিটের নাম অনুযায়ী ড্রপডাউন কাজ করবে
        class_choice = st.selectbox("আপনার শ্রেণী নির্বাচন করুন:", ['৬ষ্ঠ শ্রেণী', '৭ম শ্রেণী', '৮ম শ্রেণী'])
        df = pd.read_excel(file_name, sheet_name=class_choice)
        
        roll_input = st.number_input("আপনার রোল নাম্বার লিখুন:", min_value=1, step=1)
        
        if st.button("ফলাফল দেখুন"):
            # কলামের নাম যেন আপনার এক্সেল ফাইলের সাথে হুবহু মিলে (যেমন: 'রোল')
            student = df[df['রোল নাম্বার'] == roll_input]
            if not student.empty:
                st.table(student)
            else:
                st.error("শিক্ষার্থী পাওয়া যায়নি।")
    except Exception as e:
        st.error(f"শিট বা কলামের নামে সমস্যা আছে: {e}")
else:
    st.error(f"ফাইলটি খুঁজে পাওয়া যাচ্ছে না। ফাইলটি সঠিক ফোল্ডারে আপলোড হয়েছে কি না নিশ্চিত করুন।")
