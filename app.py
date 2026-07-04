if st.button("ফলাফল দেখুন"):
    student = df[df['রোল নাম্বার'] == roll_input]
    
    if not student.empty:
        # স্কুলের নাম পরিবর্তন করা হয়েছে
        st.markdown("<h1 style='text-align: center; color: #2E86C1;'>SHARAT CHANDRA NANDALAL PUBLIC SCHOOL AND COLLEGE</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>M A R K S H E E T</h3>", unsafe_allow_html=True)
        st.markdown("---")
        
        # ব্যক্তিগত তথ্য
        st.write(f"**Name:** {student['নাম'].values[0]}")
        st.write(f"**Class:** {class_choice}  |  **Roll:** {roll_input}")
        st.markdown("---")
        
        # মার্কশিট টেবিল ডেটা (আপনার এক্সেল ফাইলের সব বিষয় এখানে লিখুন)
        # যেমন: 'বাংলা', 'ইংরেজি', 'গণিত', 'বিজ্ঞান', 'আইসিটি' ইত্যাদি
        subjects = ['বাংলা', 'ইংরেজি', 'গণিত', 'বিজ্ঞান', 'আইসিটি'] 
        
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
        
        # মোট নম্বর গণনা
        total_obt = marks_df['Obt. Marks'].sum()
        st.write(f"### Total Obtained Marks: {total_obt} / {len(marks_df)*100}")
        
    else:
        st.warning("দুঃখিত, কোনো তথ্য পাওয়া যায়নি।")
