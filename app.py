import streamlit as st
import pandas as pd

# অ্যাপের শিরোনাম
st.title("ছাত্র ফলাফল যাচাইকরণ সিস্টেম")

# ফাইল লোড করা
file_name = 'শিক্ষার্থীদের_তথ্যাবলী_৬_৭_৮_শ্রেণী.xlsx'

# শ্রেণী নির্বাচনের অপশন
class_choice = st.selectbox("আপনার শ্রেণী নির্বাচন করুন:", ['৬ষ্ঠ শ্রেণী', '৭ম শ্রেণী', '৮ম শ্রেণী'])

# রোল ইনপুট
roll_input = st.number_input("আপনার রোল নাম্বার লিখুন:", min_value=1, step=1)

# বাটন ক্লিক করলে ফলাফল দেখাবে
if st.button("ফলাফল দেখুন"):
    try:
        df = pd.read_excel(file_name, sheet_name=class_choice)
        student = df[df['রোল নাম্বার'] == roll_input]
        
        if not student.empty:
            st.success("ফলাফল পাওয়া গেছে!")
            st.table(student)
        else:
            st.error("দুঃখিত, এই রোল নাম্বারের কোনো শিক্ষার্থী পাওয়া যায়নি।")
    except Exception as e:
        st.error("ফাইলটি লোড করতে সমস্যা হচ্ছে।")
