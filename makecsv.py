import csv
import random

# Base data for the given student
students_data = [
    {
        "student_id": 101,
        "name": "Manraj Singh Virdi",
        "email": "d2021.manrajsingh.virdi@ves.ac.in",
        "Advanced_Data_Science_score": 75,
        "Advanced_Data_Science_attendance": 80,
        "Social_Media_Analysis_score": 65,
        "Social_Media_Analysis_attendance": 75,
        "Distributed_Computing_score": 55,
        "Distributed_Computing_attendance": 60,
        "study_hours_weekly": 60,
        "extracurricular_activities": "sports;debate;coding",
        "extracurricular_hours_weekly": 5,
        "mobile_usage_hours_daily": 3,
        "social_media_usage_hours_daily": 2
    }
]

# Sample names and activities
first_names = ["Aarav", "Vihaan", "Vivaan", "Aditya", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan"]
last_names = ["Sharma", "Verma", "Mehta", "Patel", "Reddy", "Nair", "Bhat", "Kapoor", "Malhotra", "Desai"]
activities = ["sports", "music", "debate", "art", "coding", "photography", "drama", "robotics"]

# Generate 50 random student entries
for i in range(102, 152):
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    email = f"student{i}@university.edu"
    ads_score = random.randint(50, 95)
    sma_score = random.randint(50, 95)
    dc_score = random.randint(50, 95)
    ads_att = random.randint(50, 100)
    sma_att = random.randint(50, 100)
    dc_att = random.randint(50, 100)
    study_hours = random.randint(10, 70)
    extra_acts = ";".join(random.sample(activities, random.randint(1, 3)))
    extra_hours = random.randint(0, 10)
    mobile_use = random.randint(1, 6)
    social_use = random.randint(0, mobile_use)

    students_data.append({
        "student_id": i,
        "name": name,
        "email": email,
        "Advanced_Data_Science_score": ads_score,
        "Advanced_Data_Science_attendance": ads_att,
        "Social_Media_Analysis_score": sma_score,
        "Social_Media_Analysis_attendance": sma_att,
        "Distributed_Computing_score": dc_score,
        "Distributed_Computing_attendance": dc_att,
        "study_hours_weekly": study_hours,
        "extracurricular_activities": extra_acts,
        "extracurricular_hours_weekly": extra_hours,
        "mobile_usage_hours_daily": mobile_use,
        "social_media_usage_hours_daily": social_use
    })

# Save to CSV
with open("student_academic_data.csv", mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=students_data[0].keys())
    writer.writeheader()
    writer.writerows(students_data)

print("CSV file 'student_academic_data.csv' created with 51 rows.")
