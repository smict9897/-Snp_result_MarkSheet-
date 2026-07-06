import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import os
import base64
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="School Portal - SCNPS",
    page_icon="🏫",
    layout="centered"
)

# Constants
FILE_NAME = 'student_data.xlsx'
CLASS_LIST = ['৬ষ্ঠ শ্রেণী', '৭ম শ্রেণী', '৮ম শ্রেণী']

# Session state initialization
if "page" not in st.session_state:
    st.session_state.page = "home"
if "class_choice" not in st.session_state:
    st.session_state.class_choice = None
if "roll_input" not in st.session_state:
    st.session_state.roll_input = None

# Navigation functions
def go_home():
    st.session_state.page = "home"

def go_to_input():
    st.session_state.page = "input"

def go_to_result():
    st.session_state.page = "result"

def go_to_student_list():
    st.session_state.page = "student_list"

def go_to_teachers():
    st.session_state.page = "teachers"

def go_to_routine():
    st.session_state.page = "routine"

# ---------------- SHARED STYLES ----------------
def apply_styles():
    st.markdown("""
        <style>
            /* Main header */
            .school-header {
                background: linear-gradient(135deg, #1a5f3f, #2d8659);
                padding: 25px 20px;
                border-radius: 12px;
                text-align: center;
                color: white;
                margin-bottom: 25px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            }
            .school-header h1 { 
                margin: 0; 
                font-size: 24px;
                font-weight: 700;
                letter-spacing: 1px;
                color: white !important;
            }
            .school-header h3 { 
                margin: 8px 0 0 0; 
                font-weight: 400; 
                letter-spacing: 3px;
                opacity: 0.9;
                color: white !important;
            }
            
            /* Cards */
            .card-btn button {
                width: 100%;
                height: 120px;
                background: white;
                border: 1px solid #e8e8e8;
                border-radius: 14px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.06);
                font-size: 16px;
                font-weight: 600;
                color: #1a1a1a;
                transition: all 0.3s ease;
                padding: 10px;
                white-space: pre-line;
                line-height: 1.5;
            }
            .card-btn button:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 20px rgba(0,0,0,0.1);
                border-color: #2d8659;
                background: #f8fcf9;
            }
            
            /* Summary box */
            .summary-box {
                display: flex;
                justify-content: space-around;
                background: white;
                border-radius: 14px;
                padding: 20px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.06);
                margin-bottom: 25px;
                border: 1px solid #e8e8e8;
            }
            .summary-box .num { 
                font-size: 28px; 
                font-weight: 700; 
                color: #1a1a1a !important;
            }
            .summary-box .label { 
                font-size: 13px; 
                color: #666;
                margin-top: 4px;
            }
            
            /* Tables */
            .info-table td { 
                padding: 8px 12px; 
                border-bottom: 1px solid #f0f0f0;
                color: #1a1a1a !important;
            }
            .grade-table {
                width: 100%;
                border-collapse: collapse;
                margin: 15px 0;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            }
            .grade-table th { 
                background: #2d8659; 
                color: white !important; 
                padding: 12px;
                text-align: left;
                font-weight: 600;
            }
            .grade-table td { 
                padding: 10px 12px; 
                border-bottom: 1px solid #f0f0f0;
                background: white;
                color: #1a1a1a !important;
            }
            .grade-table tr:last-child td {
                border-bottom: none;
            }
            .grade-table tr:hover td {
                background: #f8fcf9;
            }
            
            /* Custom button */
            .stButton > button {
                border-radius: 8px;
                font-weight: 500;
                transition: all 0.3s ease;
            }
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }
            
            /* Expander */
            .streamlit-expanderHeader {
                font-weight: 600;
                background: #f8fcf9;
                border-radius: 8px;
            }
            
            /* Success/Warning messages */
            .stAlert {
                border-radius: 8px;
                border-left-width: 4px;
            }
            
            /* ========== PRINT STYLES - FIXED ========== */
            @media print {
                /* Hide all non-essential elements */
                .stApp, .stApp > header, .stApp > footer, 
                .stButton, .stSelectbox, .stNumberInput,
                .stAlert, .stExpander, .stMarkdown > div > p > button,
                .css-1rs6os, .css-1v3fvcr, .css-1dp5vir,
                .css-1inwz65, .css-1offfwp, .css-1xhj18k {
                    display: none !important;
                }
                
                /* Show only print content */
                .print-content {
                    display: block !important;
                    visibility: visible !important;
                    opacity: 1 !important;
                }
                
                /* Ensure text is visible */
                * {
                    color: #000000 !important;
                    background: white !important;
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                }
                
                /* Keep header colors */
                .school-header {
                    background: #2d8659 !important;
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                    color: white !important;
                }
                .school-header h1, .school-header h3 {
                    color: white !important;
                }
                
                /* Table header colors */
                .grade-table th {
                    background: #2d8659 !important;
                    color: white !important;
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                }
                
                .grade-table td {
                    color: #000000 !important;
                    background: white !important;
                }
                
                /* Info table */
                .info-table td {
                    color: #000000 !important;
                }
                
                /* Summary box */
                .summary-box {
                    border: 1px solid #ddd !important;
                    background: white !important;
                }
                .summary-box .num {
                    color: #000000 !important;
                }
                
                /* Bold text */
                b, strong {
                    color: #000000 !important;
                }
            }
            
            /* Print content wrapper - hidden by default, shown during print */
            .print-content {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)

apply_styles()

# Header - Hidden during print
st.markdown("""
    <div class="school-header no-print">
        <h1>🏫 SHARAT CHANDRA NANDALAL</h1>
        <h3>PUBLIC SCHOOL AND COLLEGE</h3>
        <h3 style="font-size: 16px; letter-spacing: 2px; margin-top: 5px;">SCHOOL PORTAL</h3>
    </div>
""", unsafe_allow_html=True)

# ---------------- HELPER FUNCTIONS ----------------
def compute_summary():
    """Calculate total students, passed, and failed from all classes"""
    total, failed = 0, 0
    if not os.path.exists(FILE_NAME):
        return total, 0, 0
    
    for cls in CLASS_LIST:
        try:
            df = pd.read_excel(FILE_NAME, sheet_name=cls)
        except Exception:
            continue
        if 'গ্রেড' not in df.columns:
            continue
        total += len(df)
        failed += df['গ্রেড'].astype(str).str.upper().eq('F').sum()
    
    passed = total - failed
    return total, passed, failed

def load_student_data(class_name, roll_no):
    """Load student data from Excel file"""
    try:
        df = pd.read_excel(FILE_NAME, sheet_name=class_name)
        student = df[df['রোল নাম্বার'].astype(str) == str(int(roll_no))]
        return student if not student.empty else None
    except Exception:
        return None

def get_class_students(class_name):
    """Get all students from a specific class"""
    try:
        df = pd.read_excel(FILE_NAME, sheet_name=class_name)
        return df
    except Exception:
        return None

def generate_print_html(student_data, class_name, roll_no):
    """Generate HTML for printing with proper colors"""
    row = student_data.iloc[0]
    skip_cols = {'রোল নাম্বার', 'নাম', 'আইডি', 'পাসওয়ার্ড', 'মোট নম্বর', 'জিপিএ', 'গ্রেড'}
    subject_cols = [c for c in student_data.columns if c not in skip_cols]
    
    # Build marks table
    marks_html = ""
    for subj in subject_cols:
        marks_html += f"<tr><td>{subj}</td><td style='text-align:center;'>{row[subj]}</td></tr>"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Result - {row['নাম']}</title>
        <style>
            /* Reset and base styles */
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: 'Arial', 'Times New Roman', sans-serif;
                padding: 30px;
                max-width: 900px;
                margin: 0 auto;
                background: white;
                color: #000000 !important;
            }}
            
            /* School Header */
            .school-header {{
                background: #2d8659;
                padding: 25px 20px;
                border-radius: 10px;
                text-align: center;
                color: white;
                margin-bottom: 25px;
            }}
            .school-header h1 {{
                margin: 0;
                font-size: 26px;
                font-weight: 700;
                color: white !important;
            }}
            .school-header h3 {{
                margin: 8px 0 0 0;
                font-weight: 400;
                letter-spacing: 3px;
                color: white !important;
                opacity: 0.95;
            }}
            .school-header .sub-title {{
                font-size: 14px;
                letter-spacing: 2px;
                margin-top: 5px;
                color: white !important;
                opacity: 0.8;
            }}
            
            /* Print Date */
            .print-date {{
                text-align: right;
                color: #444 !important;
                font-size: 12px;
                margin-bottom: 15px;
                border-bottom: 1px solid #ddd;
                padding-bottom: 8px;
            }}
            
            /* Info Table */
            .info-table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                background: #f9f9f9;
                border-radius: 8px;
                overflow: hidden;
                border: 1px solid #ddd;
            }}
            .info-table td {{
                padding: 10px 15px;
                border-bottom: 1px solid #ddd;
                color: #000000 !important;
                font-size: 14px;
            }}
            .info-table td:first-child {{
                font-weight: 600;
                background: #f0f0f0;
                width: 30%;
            }}
            .info-table tr:last-child td {{
                border-bottom: none;
            }}
            
            /* Grade Table */
            .grade-table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                border-radius: 8px;
                overflow: hidden;
                border: 1px solid #ddd;
            }}
            .grade-table th {{
                background: #2d8659;
                color: white !important;
                padding: 12px 15px;
                text-align: left;
                font-weight: 600;
                font-size: 14px;
                border-bottom: 2px solid #1a5f3f;
            }}
            .grade-table td {{
                padding: 10px 15px;
                border-bottom: 1px solid #ddd;
                color: #000000 !important;
                font-size: 14px;
            }}
            .grade-table tr:nth-child(even) {{
                background: #f9f9f9;
            }}
            .grade-table tr:last-child td {{
                border-bottom: none;
            }}
            
            /* Highlight rows */
            .highlight {{
                background: #e8f5e9 !important;
                font-weight: 700;
            }}
            .highlight td {{
                font-weight: 700;
                color: #000000 !important;
            }}
            
            /* Footer */
            .footer {{
                text-align: center;
                margin-top: 30px;
                padding-top: 15px;
                border-top: 2px solid #ddd;
                color: #666 !important;
                font-size: 11px;
            }}
            .footer p {{
                margin: 3px 0;
                color: #666 !important;
            }}
            
            /* Print button */
            .print-btn-container {{
                text-align: center;
                margin-top: 25px;
            }}
            .print-btn {{
                padding: 12px 40px;
                background: #2d8659;
                color: white !important;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
                font-weight: 500;
            }}
            .print-btn:hover {{
                background: #1a5f3f;
            }}
            
            /* Print-specific styles */
            @media print {{
                body {{
                    padding: 20px !important;
                    background: white !important;
                }}
                .no-print {{
                    display: none !important;
                }}
                .grade-table {{
                    box-shadow: none !important;
                    border: 1px solid #000 !important;
                }}
                .school-header {{
                    background: #2d8659 !important;
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                    color-adjust: exact !important;
                }}
                .grade-table th {{
                    background: #2d8659 !important;
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                    color-adjust: exact !important;
                    color: white !important;
                }}
                .highlight {{
                    background: #e8f5e9 !important;
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                    color-adjust: exact !important;
                }}
                .info-table {{
                    background: #f9f9f9 !important;
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                }}
                .info-table td:first-child {{
                    background: #f0f0f0 !important;
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                }}
                .print-btn {{
                    display: none !important;
                }}
                /* Ensure ALL text is visible */
                * {{
                    color: #000000 !important;
                }}
                .school-header h1, .school-header h3, .school-header .sub-title {{
                    color: white !important;
                }}
                .grade-table th {{
                    color: white !important;
                }}
            }}
        </style>
    </head>
    <body>
        <!-- School Header -->
        <div class="school-header">
            <h1>🏫 SHARAT CHANDRA NANDALAL</h1>
            <h3>PUBLIC SCHOOL AND COLLEGE</h3>
            <div class="sub-title">SCHOOL PORTAL - MARKSHEET</div>
        </div>
        
        <!-- Print Date -->
        <div class="print-date">
            📅 Printing Date: {pd.Timestamp.now().strftime('%d/%m/%Y %I:%M %p')}
        </div>
        
        <!-- Student Information -->
        <table class="info-table">
            <tr>
                <td>🎯 রোল নম্বর</td>
                <td>{roll_no}</td>
                <td>👤 নাম</td>
                <td>{row['নাম']}</td>
            </tr>
            <tr>
                <td>📚 শ্রেণী</td>
                <td>{class_name}</td>
                <td>🆔 আইডি</td>
                <td>{row.get('আইডি', '')}</td>
            </tr>
        </table>
        
        <!-- Marks Table -->
        <table class="grade-table">
            <tr>
                <th style="width:70%;">📖 বিষয়</th>
                <th style="width:30%; text-align:center;">📊 প্রাপ্ত নম্বর</th>
            </tr>
            {marks_html}
            <tr class="highlight">
                <td>📈 মোট নম্বর</td>
                <td style="text-align:center;">{row.get('মোট নম্বর', '')}</td>
            </tr>
            <tr class="highlight">
                <td>⭐ জিপিএ</td>
                <td style="text-align:center;">{row.get('জিপিএ', '')}</td>
            </tr>
            <tr class="highlight">
                <td>🏅 গ্রেড</td>
                <td style="text-align:center;">{row.get('গ্রেড', '')}</td>
            </tr>
        </table>
        
        <!-- Footer -->
        <div class="footer">
            <p>© 2026 Sharat Chandra Nandalal Public School and College</p>
            <p>This is a system generated marksheet. No signature required.</p>
            <p style="margin-top:5px; font-size:10px; color:#999 !important;">
                Generated on: {pd.Timestamp.now().strftime('%d/%m/%Y %I:%M %p')}
            </p>
        </div>
        
        <!-- Print Button -->
        <div class="print-btn-container no-print">
            <button class="print-btn" onclick="window.print()">
                🖨️ প্রিন্ট করুন
            </button>
            <br><br>
            <small style="color:#666;">💡 Tip: Press Ctrl+P (Windows) or Cmd+P (Mac) to print</small>
        </div>
    </body>
    </html>
    """
    return html_content

# ==================== PAGE: HOME ====================
if st.session_state.page == "home":
    total, passed, failed = compute_summary()
    pass_pct = round((passed / total) * 100, 1) if total > 0 else 0
    fail_pct = round((failed / total) * 100, 1) if total > 0 else 0

    # Summary statistics
    st.markdown(f"""
        <div class="summary-box">
            <div>
                <div class="num">{total}</div>
                <div class="label">📊 মোট শিক্ষার্থী</div>
            </div>
            <div>
                <div class="num" style="color:#2d8659;">{pass_pct}%</div>
                <div class="label">✅ পাস</div>
            </div>
            <div>
                <div class="num" style="color:#c0392b;">{fail_pct}%</div>
                <div class="label">❌ ফেল</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Menu cards
    cards = [
        ("👥", "Student List", go_to_student_list),
        ("🧑‍🏫", "Our Teachers", go_to_teachers),
        ("📄", "Verify Certificate", None),
        ("✅", "Attendance Sheet", None),
        ("⚡", "Result", go_to_input),
        ("🔔", "Exam Schedule", None),
        ("📚", "News & Events", None),
        ("🅡", "Class Routine", go_to_routine),
        ("🖼️", "Gallery", None),
    ]

    # Display cards in 2-column grid
    for i in range(0, len(cards), 2):
        row = cards[i:i+2]
        cols = st.columns(len(row))
        for col, (icon, label, action) in zip(cols, row):
            with col:
                st.markdown('<div class="card-btn">', unsafe_allow_html=True)
                clicked = st.button(f"{icon}\n\n{label}", key=label, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                if clicked:
                    if action:
                        action()
                        st.rerun()
                    else:
                        st.info(f"ℹ️ '{label}' পেজটি এখনো তৈরি হয়নি।")

# ==================== PAGE: STUDENT LIST ====================
elif st.session_state.page == "student_list":
    st.button("⬅️ হোমে ফিরে যান", on_click=go_home, use_container_width=False)
    st.subheader("📋 শ্রেণী অনুযায়ী শিক্ষার্থী তালিকা")

    if not os.path.exists(FILE_NAME):
        st.warning("⚠️ ডেটা ফাইল পাওয়া যায়নি।")
    else:
        for cls in CLASS_LIST:
            df = get_class_students(cls)
            if df is None:
                st.warning(f"{cls}: ডেটা পাওয়া যায়নি")
                continue

            with st.expander(f"📘 {cls} — {len(df)} জন শিক্ষার্থী", expanded=False):
                display_cols = [c for c in ['রোল নাম্বার', 'আইডি', 'নাম', 'গ্রেড', 'জিপিএ'] if c in df.columns]
                if display_cols:
                    sorted_df = df[display_cols].sort_values(by='রোল নাম্বার') if 'রোল নাম্বার' in display_cols else df[display_cols]
                    st.dataframe(
                        sorted_df,
                        use_container_width=True,
                        hide_index=True,
                        height=300
                    )
                else:
                    st.dataframe(df, use_container_width=True, hide_index=True)

# ==================== PAGE: TEACHERS ====================
elif st.session_state.page == "teachers":
    st.button("⬅️ হোমে ফিরে যান", on_click=go_home, use_container_width=False)
    st.subheader("🧑‍🏫 আমাদের শিক্ষকবৃন্দ")
    
    teachers_data = {
        "নাম": ["ড. মোঃ রহিম উদ্দিন", "শ্রীমতি সুমনা রায়", "মোঃ কামাল হোসেন", "শ্রীমতি রুবিনা আক্তার"],
        "পদবি": ["অধ্যক্ষ", "সহকারী অধ্যাপক", "সিনিয়র শিক্ষক", "শিক্ষক"],
        "বিষয়": ["গণিত", "ইংরেজি", "বাংলা", "বিজ্ঞান"],
        "মোবাইল": ["০১৭১২-৩৪৫৬৭৮", "০১৮১২-৩৪৫৬৭৮", "০১৯১২-৩৪৫৬৭৮", "০১৬১২-৩৪৫৬৭৮"]
    }
    df_teachers = pd.DataFrame(teachers_data)
    st.dataframe(df_teachers, use_container_width=True, hide_index=True)

# ==================== PAGE: ROUTINE ====================
elif st.session_state.page == "routine":
    st.button("⬅️ হোমে ফিরে যান", on_click=go_home, use_container_width=False)
    st.subheader("🅡 ক্লাস রুটিন")
    
    st.info("📅 ক্লাস রুটিন শীঘ্রই যোগ করা হবে।")
    
    # Example routine structure
    routine_data = {
        "দিন": ["শনিবার", "রবিবার", "সোমবার", "মঙ্গলবার", "বুধবার", "বৃহস্পতিবার"],
        "১ম পিরিয়ড": ["বাংলা", "গণিত", "ইংরেজি", "বাংলা", "গণিত", "ইংরেজি"],
        "২য় পিরিয়ড": ["গণিত", "ইংরেজি", "বাংলা", "গণিত", "ইংরেজি", "বাংলা"],
        "৩য় পিরিয়ড": ["ইংরেজি", "বাংলা", "গণিত", "ইংরেজি", "বাংলা", "গণিত"],
        "৪র্থ পিরিয়ড": ["বিজ্ঞান", "বাংলা", "গণিত", "বিজ্ঞান", "বাংলা", "গণিত"],
    }
    df_routine = pd.DataFrame(routine_data)
    st.dataframe(df_routine, use_container_width=True, hide_index=True)

# ==================== PAGE: INPUT ====================
elif st.session_state.page == "input":
    col1, col2 = st.columns([3, 1])
    with col1:
        st.button("⬅️ হোমে ফিরে যান", on_click=go_home, use_container_width=False)
    
    st.subheader("🔍 ফলাফল দেখুন")
    
    if not os.path.exists(FILE_NAME):
        st.error("❌ ডেটা ফাইল পাওয়া যায়নি। দয়া করে অ্যাডমিনের সাথে যোগাযোগ করুন।")
    else:
        class_choice = st.selectbox("শ্রেণী নির্বাচন করুন:", CLASS_LIST, key="class_select")
        roll_input = st.number_input("রোল নম্বর লিখুন:", min_value=1, step=1, key="roll_input_field")
        
        if st.button("🔍 ফলাফল দেখুন", use_container_width=True):
            try:
                roll_number = int(roll_input)
                student = load_student_data(class_choice, roll_number)
                if student is not None:
                    st.session_state.class_choice = class_choice
                    st.session_state.roll_input = roll_number
                    go_to_result()
                    st.rerun()
                else:
                    st.warning("⚠️ এই রোল নম্বরের তথ্য পাওয়া যায়নি। দয়া করে সঠিক রোল নম্বর দিন।")
            except ValueError:
                st.error("❌ দয়া করে একটি বৈধ রোল নম্বর দিন।")

# ==================== PAGE: RESULT (Marksheet) ====================
elif st.session_state.page == "result":
    # Check if session state has the required data
    if st.session_state.class_choice is None or st.session_state.roll_input is None:
        st.error("❌ তথ্য পাওয়া যায়নি। দয়া করে আবার চেষ্টা করুন।")
        if st.button("⬅️ ফিরে যান", on_click=go_to_input):
            st.rerun()
    else:
        class_choice = st.session_state.class_choice
        roll_input = st.session_state.roll_input
        
        try:
            if not os.path.exists(FILE_NAME):
                st.error("❌ ডেটা ফাইল পাওয়া যায়নি।")
                st.button("⬅️ ফিরে যান", on_click=go_to_input)
            else:
                df = pd.read_excel(FILE_NAME, sheet_name=class_choice)
                student = df[df['রোল নাম্বার'].astype(str) == str(int(roll_input))]
                
                if student.empty:
                    st.error("❌ তথ্য পাওয়া যায়নি।")
                    st.button("⬅️ ফিরে যান", on_click=go_to_input)
                else:
                    row = student.iloc[0]
                    
                    # ========== STUDENT INFO ==========
                    st.markdown(f"""
                        <div style="background: #f8fcf9; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                            <table style="width:100%; border-collapse:collapse;">
                                <tr>
                                    <td><b>🎯 রোল নম্বর</b></td>
                                    <td>{roll_input}</td>
                                    <td><b>👤 নাম</b></td>
                                    <td>{row['নাম']}</td>
                                </tr>
                                <tr>
                                    <td><b>📚 শ্রেণী</b></td>
                                    <td>{class_choice}</td>
                                    <td><b>🆔 আইডি</b></td>
                                    <td>{row.get('আইডি', '')}</td>
                                </tr>
                            </table>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # ========== MARKS TABLE ==========
                    skip_cols = {'রোল নাম্বার', 'নাম', 'আইডি', 'পাসওয়ার্ড', 'মোট নম্বর', 'জিপিএ', 'গ্রেড'}
                    subject_cols = [c for c in df.columns if c not in skip_cols]
                    
                    marks_html = ""
                    for subj in subject_cols:
                        marks_html += f"<tr><td>{subj}</td><td>{row[subj]}</td></tr>"
                    
                    st.markdown(f"""
                        <table class="grade-table">
                            <tr><th>📖 বিষয়</th><th>📊 প্রাপ্ত নম্বর</th></tr>
                            {marks_html}
                            <tr style="font-weight: 700; background: #f8fcf9;">
                                <td>📈 মোট নম্বর</td>
                                <td>{row.get('মোট নম্বর', '')}</td>
                            </tr>
                            <tr style="font-weight: 700; background: #f8fcf9;">
                                <td>⭐ জিপিএ</td>
                                <td>{row.get('জিপিএ', '')}</td>
                            </tr>
                            <tr style="font-weight: 700; background: #f8fcf9;">
                                <td>🏅 গ্রেড</td>
                                <td>{row.get('গ্রেড', '')}</td>
                            </tr>
                        </table>
                    """, unsafe_allow_html=True)
                    
                    # ========== PRINT OPTIONS ==========
                    st.markdown("---")
                    st.subheader("🖨️ প্রিন্ট অপশন")
                    
                    # Create two columns for print options
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("""
                            <div style="background: #f0f7f3; padding: 15px; border-radius: 10px; border: 1px solid #2d8659;">
                                <p style="font-weight: 600; color: #1a5f3f;">📌 Option 1: Direct Print</p>
                                <p style="font-size: 13px; color: #555;">Browser এর Print Dialog ব্যবহার করে প্রিন্ট করুন</p>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        components.html(
                            """
                            <div style="text-align:center; margin-top: 10px;">
                                <button onclick="window.print()"
                                    style="width:100%; padding: 12px; background: #2d8659; 
                                           color: white; border: none; border-radius: 8px; 
                                           cursor: pointer; font-size: 16px; font-weight: 600;
                                           transition: all 0.3s ease;">
                                    🖨️ ডিরেক্ট প্রিন্ট
                                </button>
                                <p style="font-size: 11px; color: #888; margin-top: 5px;">
                                    ⚡ Ctrl+P (Windows) বা Cmd+P (Mac) চাপুন
                                </p>
                            </div>
                            """,
                            height=100,
                        )
                    
                    with col2:
                        st.markdown("""
                            <div style="background: #f0f7f3; padding: 15px; border-radius: 10px; border: 1px solid #2d8659;">
                                <p style="font-weight: 600; color: #1a5f3f;">📌 Option 2: New Window Print</p>
                                <p style="font-size: 13px; color: #555;">নতুন উইন্ডোতে খুলে প্রিন্ট করুন (সেরা মান)</p>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Generate print HTML
                        html_content = generate_print_html(student, class_choice, roll_input)
                        b64 = base64.b64encode(html_content.encode()).decode()
                        href = f'data:text/html;base64,{b64}'
                        
                        st.markdown(f"""
                            <div style="text-align:center; margin-top: 10px;">
                                <a href="{href}" target="_blank"
                                    style="display: inline-block; width: 100%; padding: 12px; 
                                           background: #1a5f3f; color: white; border: none; 
                                           border-radius: 8px; cursor: pointer; font-size: 16px; 
                                           font-weight: 600; text-decoration: none; text-align: center;
                                           transition: all 0.3s ease;">
                                    🖨️ নতুন উইন্ডোতে প্রিন্ট
                                </a>
                                <p style="font-size: 11px; color: #888; margin-top: 5px;">
                                    📌 সেরা প্রিন্ট কোয়ালিটির জন্য এই অপশন ব্যবহার করুন
                                </p>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    # Navigation buttons
                    col3, col4, col5 = st.columns([1, 1, 1])
                    with col3:
                        if st.button("⬅️ ফিরে যান", use_container_width=True):
                            go_to_input()
                            st.rerun()
                    with col4:
                        if st.button("🏠 হোম", use_container_width=True):
                            go_home()
                            st.rerun()
                    with col5:
                        if st.button("🔄 নতুন অনুসন্ধান", use_container_width=True):
                            go_to_input()
                            st.rerun()
                    
                    st.balloons()
                    
        except Exception as e:
            st.error(f"❌ অ্যাপে সমস্যা হচ্ছে: {str(e)}")
            st.button("⬅️ ফিরে যান", on_click=go_to_input, use_container_width=True)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666; font-size: 12px; padding: 10px;">
        © 2026 Sharat Chandra Nandalal Public School and College<br>
        Developed with ❤️ for better education
    </div>
    """,
    unsafe_allow_html=True
)
