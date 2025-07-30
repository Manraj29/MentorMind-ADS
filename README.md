# MentorMindFlows

**MentorMindFlows** is an AI-powered student insight and study planning tool built with **Streamlit** and **CrewAI**. It analyzes academic performance, study habits, and lifestyle data to generate personalized reports, weekly study plans, and career guidance.

The system uses LLM agents, Google Generative AI, and custom tools to automate analysis and report generation.

---

## 🚀 Features

- **Student Data Input**:  Collects scores, attendance, habits, and extracurricular data via a user-friendly Streamlit UI.
- **Automated Academic Analysis**: Identifies strong/weak subjects, attendance issues, and academic risk factors.
- **Personalized Study Planner**: Generates weekly schedules using productivity techniques like Pomodoro and time-blocking.
- **Career Guidance**: Offers AI-driven career advice based on academic performance and interests.
- **Peer Comparison**: Benchmarks students' performance against peers using CSV data.
- **Markdown Report Generation**: Produces structured reports and mindmaps summarizing insights.
- **Email Integration**: Sends reports directly to students via email.
---

## 📁 Outputs
Input students details
<img width="1368" height="653" alt="image" src="https://github.com/user-attachments/assets/401682d4-d4d0-4216-babc-4ea90bc9be6e" />
<img width="1379" height="364" alt="image" src="https://github.com/user-attachments/assets/8b840145-8bdf-4551-9360-76898c9327ef" />
Generated Report
<img width="1399" height="550" alt="image" src="https://github.com/user-attachments/assets/cc1241c7-39fa-4149-99c2-84c887f348de" />
Download report
<img width="1448" height="619" alt="image" src="https://github.com/user-attachments/assets/1843c4c2-9eb3-4368-a7e5-768cfb0d70c9" />
Mindmap for report
<img width="1430" height="725" alt="image" src="https://github.com/user-attachments/assets/b653f7f9-f503-49f4-a6b8-a121cb405006" />
Mailed report
<img width="1096" height="749" alt="image" src="https://github.com/user-attachments/assets/515ced4b-c826-45a6-8816-9414983626ae" />


## Key Files

- **app.py**: Streamlit UI and main entry point.
- **main.py**: Orchestrates the flow, agent calls, and report generation.
- **studyplanner_tasks.yaml**: Task definitions for the study planner agent.
- **writeFile_Tool.py**: Custom tool for writing output files.
- **outputs/**: Directory where reports and generated files are saved.

Developed by Manraj Singh Virdi
