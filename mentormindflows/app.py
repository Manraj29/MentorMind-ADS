import streamlit as st
import sys
import os
from streamlit_markmap import markmap

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from mentormindflows.main import MentorMindFlow

import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_KEY")
genai.configure(api_key=api_key)

print(dir(genai)) 
def generate_mindmap(prompt):
    query = rf"""
        Study the given report which is {prompt} and generate a summary then please be precise in selecting the data such that it gets to a heirarchical structure. Dont give anything else, i just want to display the structure as a mindmap so be precise please. Dont write anything else, Just return the md file. It is not neccessay to cover all information. dont use triple backticks or ` anywhere. Cover the main topics. Please convert this data into a markdown mindmap format similar to the following example:
        ---
        markmap:
        colorFreezeLevel: 2
        ---

        # Gemini Account Summary

        ## Balances

        - Bitcoin (BTC): 0.1234
        - Ethereum (ETH): 0.5678

        ## Orders

        - Open Orders
        - Buy Order (BTC): 0.01 BTC @ $40,000
        - Trade History
        - Sold 0.1 ETH for USD at $2,500

        ## Resources

        - [Gemini Website](https://www.gemini.com/)
    """
    
    model = genai.GenerativeModel("gemini-2.0-flash-001")
    response = model.generate_content(query)
    return response.text


# Streamlit UI
st.set_page_config(page_title="MentorMind", layout="wide")
st.title("📊 MentorMind: Student Insight Generator")

with st.form("user_input_form"):
    # Two-column layout
    col1, spacer, col2 = st.columns([1, 0.1, 1])

    with col1:
        st.markdown("### 👤 Personal Info")
        name = st.text_input("Full Name", placeholder="John Doe")
        student_id = st.number_input("Student ID", min_value=1001, step=1)
        
        st.markdown("---")
        extracurricular_activities = st.text_area(
            "Extracurricular Activities (comma-separated)",
            placeholder="e.g., Football, Basketball, Coding Club"
        ).split(",")

        email = st.text_input("Email Address", placeholder="msv@gmail.com")

        st.markdown("---")
        st.markdown("### 📘 Academic Performance: Scores")
        score_ads = st.slider("Advanced Data Science Score", 0, 100, 75)
        score_sma = st.slider("Social Media Analysis Score", 0, 100, 45)
        score_dc = st.slider("Distributed Computing Score", 0, 100, 55)

    with col2:
        st.markdown("### 📝 Academic Performance: Attendance (%)")
        att_ads = st.number_input("Advanced Data Science Attendance", min_value=0, max_value=100, value=80, step=1)
        att_sma = st.number_input("Social Media Analysis Attendance", min_value=0, max_value=100, value=75, step=1)
        att_dc = st.number_input("Distributed Computing Attendance", min_value=0, max_value=100, value=60, step=1)

        st.markdown("### 🧠 Habits & Lifestyle")
        study_hours = st.slider("Study Hours per Week", 0, 100, 60)
        extra_hrs = st.slider("Extracurricular Hours per Week", 0, 30, 5)
        mobile_use = st.slider("Mobile Usage per Day (hrs)", 0, 10, 3)
        social_media = st.slider("Social Media Usage per Day (hrs)", 0, 10, 2)

    # Spacing around button
    st.markdown("<br><br>", unsafe_allow_html=True)
    submitted = st.form_submit_button(
        label="🔍 Analyze and Generate Report",
        type="primary",
        use_container_width=True
    )
    st.markdown("<br><br>", unsafe_allow_html=True)

if submitted:
    try:
        # ✅ Validations
        if not name.strip():
            raise ValueError("Please enter your full name.")
        if not email.strip():
            raise ValueError("Please enter your email address.")
        if student_id < 1000 or student_id > 9999:
            raise ValueError("Student ID must be a 4-digit number (e.g., 1234).")

        required_scores = [score_ads, score_sma, score_dc]
        required_attendance = [att_ads, att_sma, att_dc]

        if any(score is None for score in required_scores):
            raise ValueError("All subject scores must be provided.")
        if any(att is None for att in required_attendance):
            raise ValueError("All attendance values must be provided.")

        with st.spinner("Running MentorMind AI agents..."):
            # Initialize the flow
            mentormind_flow = MentorMindFlow()
            mentormind_flow.state.user_input = {
                "student_id": student_id,
                "name": name,
                "academic_performance": {
                    "Advanced Data Science": {"score": score_ads, "attendance": att_ads},
                    "Social Media Analysis": {"score": score_sma, "attendance": att_sma},
                    "Distributed Computing": {"score": score_dc, "attendance": att_dc},
                },
                "study_hours_weekly": study_hours,
                "extracurricular_activities": [activity.strip() for activity in extracurricular_activities if activity.strip()],
                "extracurricular_hours_weekly": extra_hrs,
                "mobile_usage_hours_daily": mobile_use,
                "social_media_usage_hours_daily": social_media,
                "email": email
            }

            # Run the MentorMind flow
            mentormind_flow.get_user_input()
            mentormind_flow.run_risk_analysis()
            mentormind_flow.trigger_agents()
            mentormind_flow.generate_final_report()
            mentormind_flow.mail_report()

            # 📎 Report Section
            st.markdown("### 📎 Report Preview or Download")
            report_path = os.path.join(os.path.dirname(__file__), "src", "outputs", "report.md")
            if os.path.exists(report_path):
                with open(report_path, "r", encoding="utf-8") as f:
                    report_content = f.read()
                st.markdown(report_content, unsafe_allow_html=True)

            else:
                st.warning("⚠️ Report file not found. Please ensure the report generation process completed successfully.")

            st.markdown("---")

            st.markdown("### MindMap of the report")
            # add  button to generate mindmap
            # gene_map = st.button("Generate MindMap")
            # if gene_map:
            prompt = report_content
            mindmap_content = generate_mindmap(prompt)
            # st.markdown(mindmap_content, unsafe_allow_html=True)
            markmap(mindmap_content)
            st.markdown("---")


    except ValueError as ve:
        st.error(f"❗ {ve}")
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {e}")

# st.markdown('<div style="display: flex; justify-content: center;">', unsafe_allow_html=True)
#                     st.download_button(
#                         label="📥 Download Report",
#                         data=report_content,
#                         file_name="MentorMind_Report.md",
#                         mime="text/markdown"
#                     )
#                     st.markdown('</div>', unsafe_allow_html=True)