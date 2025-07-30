#!/usr/bin/env python
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from typing import Any, Dict, Optional
from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from mentormindflows.crews.mentormind_crew.mentormind_crew import MentorMindCrew

from mentormindflows.tools.custom_tool import StudentCSVTool

from crewai_tools import FileWriterTool, FileReadTool

class MentorMindState(BaseModel):
    user_input: Optional[Dict[str, Any]] = None   # input from frontend
    thresholds: Optional[Dict[str, float]] = None # risk thresholds (academic, attendance, study)
    risk_status: Optional[str] = None             # "at-risk" or "safe"
    analysis: Optional[Dict[str, Any]] = None     # risk evaluation report
    agent_response: Optional[str] = None          # output from Crew agents
    final_send_report: Optional[str] = None       # generated report text
    final_report: Optional[str] = None            # path to the generated report file

def collect_user_data():
    return {
        "student_id": 101,
        "name": "Manraj Singh Virdi",
        "academic_performance": {
            "Advanced Data Science": {"score": 75, "attendance": 80},
            "Social Media Analysis": {"score": 45, "attendance": 75},
            "Distributed Computing": {"score": 55, "attendance": 60},
        },
        "study_hours_weekly": 60,
        "extracurricular_activities": [
            "sports",
            "debate",
            "coding"
        ],
        "extracurricular_hours_weekly": 5,
        "mobile_usage_hours_daily": 3,
        "social_media_usage_hours_daily": 2,
        "email": "d2021.manrajsingh.virdi@ves.ac.in"
    }

def assess_risk(user_data):
    scores = {}
    attendance = {}
    risk_reasons = []
    for subject, data in user_data['academic_performance'].items():
        scores[subject] = data['score']
        attendance[subject] = data['attendance']

    overall_score = sum(scores.values()) / len(scores)
    overall_attendance = sum(attendance.values()) / len(attendance)
    study_hours = user_data['study_hours_weekly']
    extracurricular_hours = user_data['extracurricular_hours_weekly']
    mobile_usage_hours = user_data['mobile_usage_hours_daily']
    social_media_usage_hours = user_data['social_media_usage_hours_daily']

    thresholds = {
        "academic": 60,
        "attendance": 75,
        "study_hours": 10,
        "extracurricular": 5,
        "mobile_usage": 3,
        "social_media_usage": 2
    }

    risk_status = "safe"
    low_score_subjects = [subject for subject, score in scores.items() if score < thresholds["academic"]]
    low_attendance_subjects = [subject for subject, att in attendance.items() if att < thresholds["attendance"]]

    if overall_score < thresholds["academic"] and overall_attendance < thresholds["attendance"]:
        risk_status = "at-risk"
        risk_reasons.append("Low overall score and attendance")
    if low_score_subjects and low_attendance_subjects:
        risk_status = "at-risk"
        risk_reasons.append("Low scores and attendance in subjects: " + ", ".join(low_score_subjects + low_attendance_subjects))
    if low_score_subjects and overall_attendance >= thresholds["attendance"]:
        risk_status = "at-risk"
        risk_reasons.append("Low scores in subjects: " + ", ".join(low_score_subjects))
    if overall_score < thresholds["academic"] and overall_attendance >= thresholds["attendance"]:
        risk_status = "at-risk"
        risk_reasons.append("Low overall score")
    if low_attendance_subjects and overall_score >= thresholds["academic"]:
        risk_status = "at-risk"
        risk_reasons.append("Low attendance in subjects: " + ", ".join(low_attendance_subjects))
    if study_hours < thresholds["study_hours"]:
        risk_status = "at-risk"
        risk_reasons.append("Low study hours")
    if extracurricular_hours < thresholds["extracurricular"]:
        risk_status = "at-risk"
        risk_reasons.append("Low extracurricular activities")
    if mobile_usage_hours > thresholds["mobile_usage"]:
        risk_status = "at-risk"
        risk_reasons.append("High mobile usage")
    if social_media_usage_hours > thresholds["social_media_usage"]:
        risk_status = "at-risk"
        risk_reasons.append("High social media usage")

    analysis = {
        "user_data": user_data,
        "thresholds": thresholds,
        "overall_score": overall_score,
        "overall_attendance": overall_attendance,
        "study_hours": study_hours,
        "extracurricular_hours": extracurricular_hours,
        "mobile_usage_hours": mobile_usage_hours,
        "social_media_usage_hours": social_media_usage_hours,
        "risk_status": risk_status,
        "risk_reasons": risk_reasons
    }
    return risk_status, analysis


def get_csv_data(file_path: str) -> str:
    file_path = os.path.join(os.path.dirname(__file__), "tools", "student_data.csv")
    tool = StudentCSVTool()
    result = tool._run(file_path=file_path, query_type="full")
    return result

def read_file(file_path: str) -> str:
    tool = FileReadTool()
    result = tool._run(file_path=file_path)
    return result

class MentorMindFlow(Flow[MentorMindState]):

    @start()
    def get_user_input(self):
        self.state.user_input = collect_user_data()
        print("User input received", self.state.user_input)

    @listen(get_user_input)
    def run_risk_analysis(self):
        self.state.risk_status, self.state.analysis = assess_risk(self.state.user_input)
        print("Risk analysis done", self.state.risk_status, self.state.analysis)

    @listen(run_risk_analysis)
    def trigger_agents(self):
        print("Triggering agents")
        crew = MentorMindCrew()
        inputs = {
            "final_send_report": self.state.analysis,
            "csv_data": get_csv_data("student_data.csv"),
            "study_plan": read_file("D:\VESIT\SEM 8\ADS\ADS project\mentormindflows\src\outputs\study_plan.md"),
            "career_guide": read_file("D:\VESIT\SEM 8\ADS\ADS project\mentormindflows\src\outputs\career_guide.md"),
            "peer_comparison": read_file("D:\VESIT\SEM 8\ADS\ADS project\mentormindflows\src\outputs\peer_comparison.md"),
        }

        crew_result = crew.crew().kickoff(inputs=inputs)
        self.state.agent_response = crew_result
        print("Agents triggered", self.state.agent_response)


    @listen(trigger_agents)
    def generate_report(self):
        print("Generating report")
        agent_response = self.state.agent_response
        agent_response_str = str(agent_response)
        with open("report.md", "w") as f:
            f.write(agent_response_str)

        self.state.final_report = "report.md"
        print("Report generated", self.state.final_report)

def kickoff():
    mentormind_flow = MentorMindFlow()
    mentormind_flow.kickoff()

def plot():
    mentormind_flow = MentorMindFlow()
    mentormind_flow.plot()

if __name__ == "__main__":
    kickoff()