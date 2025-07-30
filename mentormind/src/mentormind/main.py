#!/usr/bin/env python
import warnings
from datetime import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from mentormind.crew import Mentormind
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Inside your `run()` function

def run():
    """
    Run the crew and get output.
    """
    inputs = {
        "dataset_path": "knowledge/student_data.csv",  # or wherever your CSV is
        "current_year": str(datetime.now().year),
    }
    
    try:
        crew_result = Mentormind().crew().kickoff(inputs=inputs)
        print("Crew execution completed. Here's the output:")
        print(crew_result)  # This will print the task output to the console

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

run()
