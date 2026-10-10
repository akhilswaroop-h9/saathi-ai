from pathlib import Path

import pandas as pd

# Project directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def load_csv(filename):
    """Load a CSV file from the data directory."""

    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Required data file not found: {file_path}"
        )

    return pd.read_csv(file_path)


def load_student_data():
    """Combine all student datasets using student_id."""

    students = load_csv("students.csv")

    datasets = [
        "attendance.csv",
        "academics.csv",
        "lms_activity.csv",
        "engagement.csv",
        "placement.csv",
        "skills_feedback.csv",
    ]

    # Check the master student table
    if "student_id" not in students.columns:
        raise ValueError(
            "students.csv must contain a student_id column."
        )

    if students["student_id"].isna().any():
        raise ValueError(
            "students.csv contains missing student IDs."
        )

    if students["student_id"].duplicated().any():
        raise ValueError(
            "students.csv contains duplicate student IDs."
        )

    combined = students.copy()

    for filename in datasets:
        data = load_csv(filename)

        if "student_id" not in data.columns:
            raise ValueError(
                f"{filename} must contain a student_id column."
            )

        if data["student_id"].isna().any():
            raise ValueError(
                f"{filename} contains missing student IDs."
            )

        if data["student_id"].duplicated().any():
            raise ValueError(
                f"{filename} contains duplicate student IDs. "
                "Aggregate repeated records before merging."
            )

        combined = combined.merge(
            data,
            on="student_id",
            how="left",
            validate="one_to_one",
            indicator=f"_merge_{filename.replace('.csv', '')}"
        )

        # Show data coverage without silently hiding missing data
        unmatched = combined[
            combined[f"_merge_{filename.replace('.csv', '')}"]
            == "left_only"
        ]["student_id"].tolist()

        combined = combined.drop(
            columns=[
                f"_merge_{filename.replace('.csv', '')}"
            ]
        )

        if unmatched:
            print(
                f"Warning: {filename} has no matching record "
                f"for student IDs: {unmatched}"
            )

    return combined


def calculate_success_score(data):
    """Calculate a provisional student Success Score."""

    result = data.copy()

    # Normalize column names in case they were renamed in app.py.
    aliases = {
        "CGPA": "cgpa",
        "Attendance": "attendance_percentage",
        "Placement Readiness": "placement_readiness",
        "Backlogs": "backlogs",
    }

    result = result.rename(columns=aliases)

    required_columns = [
        "cgpa",
        "attendance_percentage",
        "placement_readiness",
        "backlogs",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in result.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}. "
            f"Available columns: {list(result.columns)}"
        )

    result["academic_score"] = (
        result["cgpa"].clip(0, 10) * 10
    )

    result["backlog_score"] = (
        100 - result["backlogs"].clip(lower=0) * 20
    ).clip(0, 100)

    result["success_score"] = (
        result["academic_score"] * 0.30
        + result["attendance_percentage"].clip(0, 100) * 0.20
        + result["placement_readiness"].clip(0, 100) * 0.30
        + result["backlog_score"] * 0.20
    ).round(1)

    return result


def identify_risks(data):
    """Identify academic and placement risks transparently."""

    result = data.copy()

    result["academic_risk"] = "Low"

    high_academic_risk = (
        (result["attendance_percentage"] < 65)
        | (result["cgpa"] < 6)
        | (result["backlogs"] >= 3)
    )

    medium_academic_risk = (
        (result["attendance_percentage"] < 75)
        | (result["cgpa"] < 7)
        | (result["backlogs"] >= 2)
    )

    result.loc[
        medium_academic_risk,
        "academic_risk"
    ] = "Medium"

    result.loc[
        high_academic_risk,
        "academic_risk"
    ] = "High"

    result["placement_risk"] = "Low"

    result.loc[
        result["placement_readiness"] < 65,
        "placement_risk"
    ] = "Medium"

    result.loc[
        result["placement_readiness"] < 40,
        "placement_risk"
    ] = "High"

    return result
def generate_student_insights(student):
    """Explain student risks and recommend interventions."""

    insights = []
    recommendations = []

    # Academic performance
    if student["CGPA"] < 6:
        insights.append(
            "Low CGPA is a major academic concern."
        )
        recommendations.append(
            "Arrange subject-wise remedial classes."
        )

    # Attendance
    if student["Attendance"] < 75:
        insights.append(
            "Attendance is below the 75% monitoring threshold."
        )
        recommendations.append(
            "Arrange faculty follow-up and an attendance improvement plan."
        )

    # Backlogs
    if student["Backlogs"] >= 2:
        insights.append(
            f"The student has {student['Backlogs']} backlogs."
        )
        recommendations.append(
            "Create a backlog recovery plan with weekly assessments."
        )

    # Placement readiness
    if student["Placement Readiness"] < 65:
        insights.append(
            "Placement readiness needs improvement."
        )
        recommendations.append(
            "Provide aptitude practice, coding exercises, and mock interviews."
        )

    # LMS activity
    lms_score = student.get("lms_activity_score", None)

    if pd.notna(lms_score) and lms_score < 50:
        insights.append(
            "Learning platform activity is low."
        )
        recommendations.append(
            "Encourage regular LMS usage and assignment completion."
        )

    if not insights:
        insights.append(
            "No major concerns were identified by the current rules."
        )

    if not recommendations:
        recommendations.append(
            "Continue monitoring progress and provide development opportunities."
        )

    return {
        "insights": insights,
        "recommendations": recommendations,
    }
def segment_student(student):
    """
    Assign a student to an interpretable segment.
    """

    if (
        student["academic_risk"] == "High"
        and student["placement_risk"] == "High"
    ):
        return "Comprehensive Support Needed"

    if (
        student["academic_risk"] == "High"
        or student["academic_risk"] == "Medium"
    ):
        return "Academic Support Needed"

    if student["placement_risk"] in ["High", "Medium"]:
        return "Placement Preparation Needed"

    return "High Performing"