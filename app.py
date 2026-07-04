import streamlit as st
import pandas as pd

# স্কুলের নাম
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>SHARAT CHANDRA NANDALAL PUBLIC SCHOOL AND COLLEGE</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>M A R K S H E E T</h3>", unsafe_allow_html=True)
st.markdown("---")

file_name = 'student_data.xlsx'
class_choice = st.selectbox("আপনার শ্রেণী নির্বাচন করুন:", ['৬ষ্ঠ শ্রেণী', '৭ম শ্রেণী', '৮ম শ্রেণী'])

try:
    df = pd.read_excel(file_name, sheet_name=class_choice)
    roll_input = st.number_input("আপনার রোল নাম্বার লিখুন:", min_value=1, step=1)
    
    if st.button("ফলাফল দেখুন"):
        # আপনার এক্সেল ফাইলের রোল কলামের নাম যদি অন্য কিছু হয়, তবে তা এখানে লিখুন
        student = df[df['রোল নাম্বার'] == roll_input]
        
        if not student.empty:
            st.write(f"**নাম:** {student['নাম'].values[0]}")
            st.markdown("---")
            
            # সব কলামের তথ্য একসাথে দেখানো
            st.table(student.T.rename(columns={student.index[0]: 'তথ্য'}))
            st.balloons()
        else:
            st.warning("এই রোল নাম্বারের কোনো তথ্য পাওয়া যায়নি।")
            
except Exception as e:
    st.error(f"কলামের নাম বা ফাইলে সমস্যা আছে: {e}")
except Exception as e:
    st.error(f"ফাইল বা কলামের নামে সমস্যা আছে: {e}")
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
