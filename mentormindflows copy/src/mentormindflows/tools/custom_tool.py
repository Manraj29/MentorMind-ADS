from typing import Type
import pandas as pd
import os
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class StudentCSVToolInput(BaseModel):
    file_path: str = Field(..., description="Path to the student performance CSV file")
    query_type: str = Field(..., description="Type of query: 'summary', 'full', 'by_student_id'")
    student_id: int = Field(None, description="Student ID to filter, required if using 'by_student_id'")


class StudentCSVTool(BaseTool):
    name: str = "Student CSV Data Tool"
    description: str = (
        "This tool reads a student performance CSV file and returns insights. "
        "Use it to get summary statistics, the full dataset, or details for a specific student using student_id."
    )
    args_schema: Type[BaseModel] = StudentCSVToolInput

    def _run(self, file_path: str, query_type: str, student_id: int = None) -> str:
        # Ensure the file path is relative to the current script directory
        if not os.path.isabs(file_path):
            file_path = os.path.join(os.path.dirname(__file__), file_path)

        try:
            df = pd.read_csv(file_path)
        except FileNotFoundError:
            return f"❌ File not found: {file_path}"
        except Exception as e:
            return f"❌ Error reading file: {e}"

        if query_type == "summary":
            return df.describe(include='all').to_string()

        elif query_type == "full":
            return df.to_string(index=False)

        elif query_type == "by_student_id":
            if student_id is None:
                return "❌ Please provide a student_id when using 'by_student_id'."
            result = df[df['student_id'] == student_id]
            return result.to_string(index=False) if not result.empty else "⚠️ No data found for the given student ID."

        else:
            return "❌ Invalid query_type. Use 'summary', 'full', or 'by_student_id'."