import streamlit as st
import pandas as pd
import plotly.express as px
from intervention_tracker import (
    load_interventions,
    add_intervention,
    update_intervention_status,
    interventions_dataframe,
)

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="SAATHI AI | Student Success",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ================= SAATHI AI FULL-SCREEN INTRO =================

import streamlit.components.v1 as components

if "intro_completed" not in st.session_state:
    st.session_state.intro_completed = False

if not st.session_state.intro_completed:

    components.html(
        """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            * {
                box-sizing: border-box;
            }

            html, body {
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                overflow: hidden;
                font-family: Arial, sans-serif;
                background: #080b18;
            }

            .intro {
                position: fixed;
                inset: 0;
                width: 100vw;
                height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                overflow: hidden;
                color: white;
                background:
                    radial-gradient(
                        ellipse at 50% 45%,
                        #263f91 0%,
                        #111a3a 40%,
                        #080b18 78%
                    );
                animation: fadeOut 1s ease 5s forwards;
                z-index: 999999;
            }

            .orb {
                position: absolute;
                width: 260px;
                height: 260px;
                border-radius: 50%;
                background: #6366f1;
                filter: blur(100px);
                opacity: .25;
                animation: pulse 3s ease-in-out infinite alternate;
            }

            .logo {
                position: relative;
                font-size: clamp(42px, 9vw, 100px);
                font-weight: 900;
                letter-spacing: clamp(3px, 1vw, 12px);
                background: linear-gradient(
                    100deg,
                    #60a5fa,
                    #c084fc,
                    #38bdf8
                );
                background-size: 200% auto;
                color: transparent;
                background-clip: text;
                -webkit-background-clip: text;
                opacity: 0;
                animation:
                    reveal 1.2s ease .3s forwards,
                    shine 3s linear infinite;
            }

            .fullform {
                position: relative;
                max-width: 850px;
                padding: 0 24px;
                margin-top: 24px;
                font-size: clamp(16px, 2.5vw, 25px);
                line-height: 1.7;
                color: #dbeafe;
                opacity: 0;
                animation: riseIn 1s ease 1.3s forwards;
            }

            .tagline {
                position: relative;
                max-width: 90%;
                margin-top: 30px;
                font-size: clamp(10px, 1.5vw, 14px);
                letter-spacing: 2px;
                line-height: 1.8;
                color: #a5b4fc;
                opacity: 0;
                animation: riseIn 1s ease 2.3s forwards;
            }

            .line {
                position: relative;
                width: 0;
                height: 3px;
                margin-top: 35px;
                border-radius: 10px;
                background: linear-gradient(
                    90deg,
                    #3b82f6,
                    #a855f7,
                    #38bdf8
                );
                animation: expand 1.4s ease 2.8s forwards;
            }

            @keyframes reveal {
                from {
                    opacity: 0;
                    transform: translateY(35px) scale(.92);
                }
                to {
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }
            }

            @keyframes riseIn {
                from {
                    opacity: 0;
                    transform: translateY(22px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            @keyframes shine {
                to {
                    background-position: 200% center;
                }
            }

            @keyframes pulse {
                from {
                    transform: scale(.8);
                    opacity: .15;
                }
                to {
                    transform: scale(1.3);
                    opacity: .35;
                }
            }

            @keyframes expand {
                to {
                    width: min(320px, 65vw);
                }
            }

            @keyframes fadeOut {
                to {
                   animation: fadeOut 1s ease 4s forwards;
                }
            }

            @media (prefers-reduced-motion: reduce) {
                *, *::before, *::after {
                    animation-duration: .01ms !important;
                    animation-delay: 0ms !important;
                }
            }
        </style>
        </head>

        <body>
            <div class="intro">
                <div class="orb"></div>

                <div class="logo">SAATHI AI</div>

                <div class="fullform">
                    Student Analytics &amp; Actionable<br>
                    Timely Help Intelligence
                </div>

                <div class="tagline">
                    PREDICT CHALLENGES · DISCOVER POTENTIAL<br>
                    EMPOWER EVERY STUDENT
                </div>

                <div class="line"></div>
            </div>
        </body>
        </html>
        """,
        height=1000,
        scrolling=False,
    )

# ================= END SAATHI AI INTRO =================
# ---------------- CUSTOM DESIGN ----------------


st.markdown("""
<style>
    .stApp {
        background-color: #F4F7FC;
    }

    [data-testid="stSidebar"] {
        background-color: #101D36;
    }

    [data-testid="stSidebar"] * {
        color: white;
    }

    .hero {
        padding: 28px;
        border-radius: 18px;
        background: linear-gradient(120deg, #142850, #276EF1);
        color: white;
        margin-bottom: 25px;
    }

    .hero h1 {
        color: white;
        font-size: 38px;
    }

    .hero p {
        color: #E5EDFF;
        font-size: 17px;
    }

    div[data-testid="stMetric"] {
        background: white;
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #E1E8F5;
        box-shadow: 0 3px 12px rgba(20, 40, 80, 0.04);
    }

    h2, h3 {
        color: #142850;
    }/* ===== SAATHI AI MODERN DASHBOARD ===== */

[data-testid="stMetric"] {
    border-radius: 16px;
    padding: 20px;
    border: 1px solid var(--secondary-background-color);
    box-shadow: 0 4px 16px rgba(30, 60, 100, 0.08);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(30, 60, 100, 0.15);
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 16px;
}

.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
}

[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

hr {
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
}
/* ===== SAATHI AI  CONSISTENCY ===== */

/* Theme-aware main content */
.stApp {
    color: var(--text-color);
}

/* Theme-aware cards */
[data-testid="stMetric"],
[data-testid="stExpander"],
[data-testid="stDataFrame"],
[data-testid="stTable"] {
    border-radius: 14px;
}

/* Form controls */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    border-radius: 10px;
}

/* Buttons */
.stButton > button,
.stDownloadButton > button {
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.2s ease;
}

/* Cleaner section headings */
h1, h2, h3 {
    letter-spacing: -0.3px;
}

/* Improve page spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Smooth  transitions */
.stApp,
[data-testid="stSidebar"],
[data-testid="stMetric"] {
    transition: background-color 0.2s ease,
                color 0.2s ease,
                border-color 0.2s ease;
}
/* ===== SAATHI AI SIDEBAR NAVIGATION ===== */

/* Sidebar layout */
[data-testid="stSidebar"] {
    border-right: 1px solid var(--secondary-background-color);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}

/* Navigation labels */
[data-testid="stSidebar"] label {
    font-weight: 500;
}

/* Sidebar radio buttons */
[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 8px;
}

/* Individual navigation options */
[data-testid="stSidebar"] [role="radiogroup"] label {
    border-radius: 10px;
    padding: 9px 12px;
    transition: background-color 0.2s ease,
                transform 0.2s ease;
}

/* Hover effect */
[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background-color: rgba(59, 130, 246, 0.12);
    transform: translateX(3px);
}

/* Sidebar title */
[data-testid="stSidebar"] h1 {
    font-size: 1.45rem;
    font-weight: 750;
    letter-spacing: -0.5px;
}

/* Sidebar caption */
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    font-size: 0.8rem;
    opacity: 0.8;
}

/* Sidebar separators */
[data-testid="stSidebar"] hr {
    margin: 1.4rem 0;
    opacity: 0.2;
}
/* ===== SAATHI AI MINIMAL NAVIGATION ===== */

[data-testid="stSidebar"] {
    border-right: 1px solid var(--border-color, #334155);
}

[data-testid="stSidebar"] > div:first-child {
    padding: 24px 14px;
}

/* Sidebar brand */
[data-testid="stSidebar"] h1 {
    font-size: 1.55rem;
    font-weight: 800;
    letter-spacing: -0.7px;
}

/* Navigation group */
[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 6px;
}

/* Navigation items */
[data-testid="stSidebar"] [role="radiogroup"] label {
    padding: 10px 12px;
    border-radius: 9px;
    border: 1px solid transparent;
    transition: all 180ms ease;
}

/* Hover state */
[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: rgba(99, 102, 241, 0.10);
    border-color: rgba(99, 102, 241, 0.20);
    transform: translateX(2px);
}

/* Radio indicator */
[data-testid="stSidebar"] [role="radiogroup"] label [data-testid="stMarkdownContainer"] {
    font-weight: 500;
}

/* Section captions */
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    font-size: 0.78rem;
    letter-spacing: 0.6px;
    text-transform: uppercase;
}

/* Sidebar separators */
[data-testid="stSidebar"] hr {
    margin: 22px 0;
    opacity: 0.18;
}
</style>
""", unsafe_allow_html=True)

# ---------------- DATA INTEGRATION ----------------

# ---------------- DATA INTEGRATION ----------------

from data_engine import (
    load_student_data,
    calculate_success_score,
    identify_risks,
    generate_student_insights,
    segment_student,
)

# Load the original CSV datasets
students = load_student_data()

# Calculate scores and risks using original column names
students = calculate_success_score(students)
students = identify_risks(students)

# Create student segments
students["Student Segment"] = students.apply(
    segment_student,
    axis=1
)

# Rename columns only AFTER all calculations are complete
students = students.rename(columns={
    "student_id": "Student ID",
    "name": "Name",
    "department": "Department",
    "year": "Year",
    "cgpa": "CGPA",
    "attendance_percentage": "Attendance",
    "backlogs": "Backlogs",
    "placement_readiness": "Placement Readiness",
    "success_score": "Success Score",
    "academic_risk": "Academic Risk",
    "placement_risk": "Placement Risk",
})
# ---------------- SIDEBAR ----------------

st.sidebar.markdown("# 🎓 SAATHI AI")
st.sidebar.caption("STUDENT SUCCESS INTELLIGENCE")


st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Overview",
        "Student Analytics",
        "At-Risk Students",
        "Placement Readiness",
        "Student Intelligence",
        "Data Import",
        "Student Search",
        "Faculty Intervention",
        "Student Success Plan",
        "Faculty Progress Tracking",
        "AI Student Insights",
    ]
)

st.sidebar.divider()
st.sidebar.caption("Hackathon Prototype | 2026")

# ---------------- SUCCESS SCORE ----------------

students["Academic Score"] = (
    students["CGPA"] / 10 * 100
)

students["Success Score"] = (
    students["Academic Score"] * 0.30
    + students["Attendance"] * 0.20
    + students["Placement Readiness"] * 0.30
    + (100 - students["Backlogs"] * 20).clip(0, 100) * 0.20
).round(1)

students["Academic Risk"] = students.apply(
    lambda row: "High" if (
        row["Attendance"] < 65
        or row["Backlogs"] >= 3
        or row["CGPA"] < 6
    ) else "Medium" if (
        row["Attendance"] < 75
        or row["Backlogs"] >= 2
        or row["CGPA"] < 7
    ) else "Low",
    axis=1
)

students["Placement Risk"] = students[
    "Placement Readiness"
].apply(
    lambda score: "High" if score < 40
    else "Medium" if score < 65
    else "Low"
)

# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">
    <h1>SAATHI AI</h1>
    <p>Student Success Intelligence Platform</p>
    <p>Predict challenges. Discover potential. Improve student success.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- OVERVIEW PAGE ----------------

if page == "Overview":

    st.subheader("Campus Intelligence Overview")

    department = st.selectbox(
        "Select Department",
        ["All Departments"] + sorted(
            students["Department"].unique().tolist()
        )
    )

    filtered = students.copy()

    if department != "All Departments":
        filtered = filtered[
            filtered["Department"] == department
        ]

    total_students = len(filtered)

    high_risk = len(
        filtered[filtered["Academic Risk"] == "High"]
    )

    avg_score = (
        filtered["Success Score"].mean()
        if total_students else 0
    )

    avg_attendance = (
        filtered["Attendance"].mean()
        if total_students else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Students", total_students)

    c2.metric(
        "Average Success Score",
        f"{avg_score:.1f}/100"
    )

    c3.metric(
        "High Academic Risk",
        high_risk
    )

    c4.metric(
        "Average Attendance",
        f"{avg_attendance:.1f}%"
    )

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Student Success Distribution")

        fig = px.histogram(
            filtered,
            x="Success Score",
            nbins=8,
            title="Success Score Distribution",
            color_discrete_sequence=["#276EF1"]
        )

        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Academic Risk Distribution")

        risk_counts = (
            filtered["Academic Risk"]
            .value_counts()
            .rename_axis("Risk Level")
            .reset_index(name="Students")
        )

        fig = px.pie(
            risk_counts,
            names="Risk Level",
            values="Students",
            hole=0.55,
            title="Academic Risk Overview"
        )

        fig.update_layout(
            paper_bgcolor="white"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Student Performance Overview")

    st.dataframe(
        filtered[
            [
                "Student ID",
                "Department",
                "CGPA",
                "Attendance",
                "Backlogs",
                "Success Score",
                "Academic Risk",
                "Placement Risk"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

# ---------------- STUDENT ANALYTICS ----------------

elif page == "Student Analytics":

    st.subheader("📊 Student Analytics")

    selected_id = st.selectbox(
        "Select Student",
        students["Student ID"].tolist()
    )

    student = students[
        students["Student ID"] == selected_id
    ].iloc[0]

    c1, c2, c3 = st.columns(3)

    c1.metric("CGPA", f"{student['CGPA']:.2f}/10")
    c2.metric("Attendance", f"{student['Attendance']}%")
    c3.metric("Success Score", f"{student['Success Score']}/100")

    st.write("### Performance Indicators")

    indicators = pd.DataFrame({
        "Indicator": [
            "Academic Performance",
            "Attendance",
            "Placement Readiness"
        ],
        "Score": [
            student["Academic Score"],
            student["Attendance"],
            student["Placement Readiness"]
        ]
    })

    fig = px.bar(
        indicators,
        x="Indicator",
        y="Score",
        range_y=[0, 100],
        text="Score",
        title=f"Performance Profile: {selected_id}"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.write("### Recommended Interventions")

    if student["Attendance"] < 75:
        st.warning(
            "Attendance support: arrange faculty follow-up."
        )

    if student["Backlogs"] > 0:
        st.info(
            f"Academic support: review {student['Backlogs']} backlog(s)."
        )

    if student["Placement Readiness"] < 65:
        st.info(
            "Placement support: recommend aptitude, coding, "
            "and mock interview practice."
        )

    if (
        student["Attendance"] >= 75
        and student["Backlogs"] == 0
        and student["Placement Readiness"] >= 65
    ):
        st.success(
            "Continue regular monitoring and skill development."
        )

# ---------------- AT-RISK STUDENTS ----------------

elif page == "At-Risk Students":

    st.subheader("🚨 Students Requiring Attention")

    risk_type = st.selectbox(
        "Select Risk Category",
        ["Academic Risk", "Placement Risk"]
    )

    risk_level = st.selectbox(
        "Select Risk Level",
        ["All", "High", "Medium", "Low"]
    )

    risk_column = risk_type

    risk_data = students.copy()

    if risk_level != "All":
        risk_data = risk_data[
            risk_data[risk_column] == risk_level
        ]

    st.dataframe(
        risk_data[
            [
                "Student ID",
                "Department",
                "CGPA",
                "Attendance",
                "Backlogs",
                "Success Score",
                "Academic Risk",
                "Placement Risk"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Risk flags are based on transparent prototype rules "
        "and should be validated before real-world use."
    )

# ---------------- PLACEMENT READINESS ----------------

elif page == "Placement Readiness":

    st.subheader("🎯 Placement Readiness Analytics")

    fig = px.scatter(
        students,
        x="CGPA",
        y="Placement Readiness",
        size="Attendance",
        color="Department",
        hover_name="Student ID",
        hover_data=["Backlogs", "Success Score"],
        title="Academic Performance vs Placement Readiness",
        labels={
            "CGPA": "CGPA",
            "Placement Readiness": "Placement Readiness Score"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

    st.write("### Placement Support Candidates")

    placement_candidates = students[
        students["Placement Risk"] != "Low"
    ].sort_values("Placement Readiness")

    st.dataframe(
        placement_candidates[
            [
                "Student ID",
                "Department",
                "CGPA",
                "Placement Readiness",
                "Placement Risk"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "This prototype uses sample data. Placement predictions "
        "are not validated forecasts."
    )
    # ---------------- STUDENT INTELLIGENCE ----------------

elif page == "Student Intelligence":

    st.subheader("🧠 Explainable Student Intelligence")

    selected_id = st.selectbox(
        "Choose a student",
        students["Student ID"].tolist(),
        key="intelligence_student"
    )

    student = students[
        students["Student ID"] == selected_id
    ].iloc[0]

    insights_data = generate_student_insights(student)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Success Score",
        f"{student['Success Score']}/100"
    )

    col2.metric(
        "Academic Risk",
        student["Academic Risk"]
    )

    col3.metric(
        "Placement Risk",
        student["Placement Risk"]
    )

    st.divider()

    st.markdown("### 🎯 Student Segment")

    st.info(student["Student Segment"])

    st.markdown("### 🔍 Why does this student need attention?")

    for insight in insights_data["insights"]:
        st.warning(insight)

    st.markdown("### 💡 Recommended Actions")

    for recommendation in insights_data["recommendations"]:
        st.success(recommendation)

    st.markdown("### 📊 Student Performance Indicators")

    indicators = pd.DataFrame({
        "Indicator": [
            "Academic Performance",
            "Attendance",
            "Placement Readiness",
            "LMS Activity",
            "Technical Skills",
            "Soft Skills",
        ],
        "Score": [
            student["academic_score"],
            student["Attendance"],
            student["Placement Readiness"],
            student.get("lms_activity_score", 0),
            student.get("technical_skill_score", 0),
            student.get("soft_skill_score", 0),
        ]
    })

    fig = px.bar(
        indicators,
        x="Indicator",
        y="Score",
        range_y=[0, 100],
        text="Score",
        title="Student Performance Breakdown",
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    # ---------------- DATA IMPORT ----------------

elif page == "Data Import":

    st.subheader("📂 Student Data Import Center")

    st.write(
        "Upload student datasets to preview and validate "
        "them before integration."
    )

    dataset_type = st.selectbox(
        "Select Dataset Type",
        [
            "Students",
            "Attendance",
            "Academics",
            "LMS Activity",
            "Engagement",
            "Placement",
            "Skills & Feedback"
        ]
    )

    uploaded_file = st.file_uploader(
        "Upload a CSV file",
        type=["csv"],
        key="student_data_upload"
    )

    expected_columns = {
        "Students": [
            "student_id", "name", "department", "year"
        ],
        "Attendance": [
            "student_id", "attendance_percentage"
        ],
        "Academics": [
            "student_id", "cgpa", "internal_marks", "backlogs"
        ],
        "LMS Activity": [
            "student_id", "lms_activity_score",
            "assignment_completion"
        ],
        "Engagement": [
            "student_id", "engagement_score",
            "certifications", "events_participated"
        ],
        "Placement": [
            "student_id", "aptitude_score", "coding_score",
            "mock_interview_score", "placement_readiness"
        ],
        "Skills & Feedback": [
            "student_id", "technical_skill_score",
            "soft_skill_score", "student_satisfaction"
        ]
    }

    if uploaded_file is not None:
        try:
            uploaded_data = pd.read_csv(uploaded_file)

            st.write("### Uploaded Data Preview")

            st.dataframe(
                uploaded_data.head(20),
                use_container_width=True,
                hide_index=True
            )

            required = expected_columns[dataset_type]

            missing_columns = [
                column
                for column in required
                if column not in uploaded_data.columns
            ]

            if missing_columns:
                st.error(
                    "Missing required columns: "
                    + ", ".join(missing_columns)
                )

            elif uploaded_data["student_id"].isna().any():
                st.error("Some records have missing student IDs.")

            elif uploaded_data["student_id"].astype(str).str.strip().eq("").any():
                st.error("Some records have empty student IDs.")

            elif uploaded_data["student_id"].duplicated().any():
                st.error(
                    "Duplicate student IDs found. "
                    "Please correct the file before importing."
                )

            else:
                st.success("Dataset structure validated.")

                st.metric(
                    "Records Uploaded",
                    len(uploaded_data)
                )

                st.metric(
                    "Columns Detected",
                    len(uploaded_data.columns)
                )

                if st.button(
                    "Save & Import Dataset",
                    type="primary"
                ):
                    from pathlib import Path

                    data_folder = (
                        Path(__file__).resolve().parent / "data"
                    )
                    data_folder.mkdir(exist_ok=True)

                    filenames = {
                        "Students": "students.csv",
                        "Attendance": "attendance.csv",
                        "Academics": "academics.csv",
                        "LMS Activity": "lms_activity.csv",
                        "Engagement": "engagement.csv",
                        "Placement": "placement.csv",
                        "Skills & Feedback": "skills_feedback.csv",
                    }

                    destination = data_folder / filenames[dataset_type]

                    uploaded_data.to_csv(
                        destination,
                        index=False
                    )

                    st.success(
                    f"Successfully imported {len(uploaded_data)} records "
                    f"into {destination.name}."
                )

                    st.cache_data.clear()

                    st.info("Refreshing SAATHI AI with the imported data...")

                    st.rerun()

        except Exception as error:
            st.error(f"Unable to process the CSV file: {error}")
            # ---------------- STUDENT SEARCH ----------------

elif page == "Student Search":

    st.subheader("🔎 Student Search")
    st.write(
        "Search for a student by name or student ID."
    )

    search_query = st.text_input(
        "Enter student name or ID",
        placeholder="Example: STU188 or Krishna"
    )

    if search_query.strip():

        query = search_query.strip().lower()

        matches = students[
            students["Student ID"].astype(str).str.lower().str.contains(
                query, na=False
            )
            |
            students["Name"].astype(str).str.lower().str.contains(
                query, na=False
            )
        ]

        if matches.empty:

            st.warning("No matching students found.")

        else:

            st.success(
                f"Found {len(matches)} matching student(s)."
            )

            st.dataframe(
                matches[
                    [
                        "Student ID",
                        "Name",
                        "Department",
                        "Year",
                        "CGPA",
                        "Attendance",
                        "Success Score",
                        "Academic Risk",
                        "Placement Risk",
                    ]
                ],
                use_container_width=True,
                hide_index=True,
            )

            selected_id = st.selectbox(
                "Select a student to view details",
                matches["Student ID"].tolist(),
            )

            student = matches[
                matches["Student ID"] == selected_id
            ].iloc[0]

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Success Score",
                f"{student['Success Score']}/100",
            )

            col2.metric(
                "Academic Risk",
                student["Academic Risk"],
            )

            col3.metric(
                "Placement Readiness",
                f"{student['Placement Readiness']}/100",
            )

            st.markdown("### Student Profile")

            st.write(f"**Name:** {student['Name']}")
            st.write(f"**Student ID:** {student['Student ID']}")
            st.write(f"**Department:** {student['Department']}")
            st.write(f"**Year:** {student['Year']}")
            st.write(f"**CGPA:** {student['CGPA']}")
            st.write(f"**Attendance:** {student['Attendance']}%")

            # ---------------- PERSONALIZED RECOMMENDATIONS ----------------

            st.markdown("### 🎯 Personalized Recommendations")

            recommendations = []

            # Academic recommendations
            if student["CGPA"] < 6:
                recommendations.append(
                    "📚 Academic Support: Arrange mentoring and focused subject revision."
                )
            elif student["CGPA"] < 7.5:
                recommendations.append(
                    "📖 Academic Improvement: Follow a weekly study plan and practice assessments."
                )
            else:
                recommendations.append(
                    "🌟 Academic Excellence: Maintain performance and explore advanced projects."
                )

            # Attendance recommendations
            if student["Attendance"] < 75:
                recommendations.append(
                    "⚠️ Attendance: Create an attendance improvement plan with faculty support."
                )
            else:
                recommendations.append(
                    "✅ Attendance: Maintain consistent class attendance."
                )

            # Placement recommendations
            if student["Placement Readiness"] < 50:
                recommendations.append(
                    "💼 Placement Preparation: Start with aptitude basics, coding practice, and mock interviews."
                )
            elif student["Placement Readiness"] < 75:
                recommendations.append(
                    "🚀 Placement Preparation: Practice coding problems and participate in mock interviews."
                )
            else:
                recommendations.append(
                    "🏆 Placement Readiness: Attempt advanced assessments and company-specific mock interviews."
                )

            # Display recommendations
            for recommendation in recommendations:
                st.info(recommendation)

# ---------------- FACULTY INTERVENTION ----------------

elif page == "Faculty Intervention":

    st.title("🎓 Faculty Intervention Dashboard")

    st.write(
        "Identify students who may benefit from academic "
        "support, attendance monitoring, or placement preparation."
    )

    intervention_data = students.copy()

    # Ensure numeric fields are usable
    intervention_data["CGPA"] = pd.to_numeric(
        intervention_data["CGPA"], errors="coerce"
    )

    intervention_data["Attendance"] = pd.to_numeric(
        intervention_data["Attendance"], errors="coerce"
    )

    intervention_data["Success Score"] = pd.to_numeric(
        intervention_data["Success Score"], errors="coerce"
    )

    intervention_data["Placement Readiness"] = pd.to_numeric(
        intervention_data["Placement Readiness"], errors="coerce"
    )

    # Assign intervention priorities using transparent rules
    def assign_intervention(row):

        reasons = []

        if row["CGPA"] < 6:
            reasons.append("Academic support")

        if row["Attendance"] < 75:
            reasons.append("Attendance improvement")

        if row["Placement Readiness"] < 50:
            reasons.append("Placement preparation")

        if row["Academic Risk"] == "High":
            reasons.append("High academic risk")

        if reasons:
            return ", ".join(reasons)

        return "Regular monitoring"

    intervention_data["Recommended Intervention"] = (
        intervention_data.apply(assign_intervention, axis=1)
    )

    intervention_data["Priority"] = intervention_data.apply(
        lambda row: (
            "High"
            if (
                row["Academic Risk"] == "High"
                or row["Attendance"] < 60
                or row["CGPA"] < 5
            )
            else (
                "Medium"
                if row["Recommended Intervention"] != "Regular monitoring"
                else "Low"
            )
        ),
        axis=1,
    )

    # Summary metrics
    high_priority = (
        intervention_data["Priority"] == "High"
    ).sum()

    medium_priority = (
        intervention_data["Priority"] == "Medium"
    ).sum()

    regular_monitoring = (
        intervention_data["Priority"] == "Low"
    ).sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("High Priority", int(high_priority))
    col2.metric("Medium Priority", int(medium_priority))
    col3.metric("Regular Monitoring", int(regular_monitoring))

    st.divider()

    # Filters
    st.subheader("Student Intervention List")

    priority_filter = st.selectbox(
        "Filter by Priority",
        ["All", "High", "Medium", "Low"],
    )

    filtered_data = intervention_data.copy()

    if priority_filter != "All":
        filtered_data = filtered_data[
            filtered_data["Priority"] == priority_filter
        ]

    filtered_data = filtered_data.sort_values(
        by=["Priority", "Success Score"],
        ascending=[True, True],
    )

    display_columns = [
        "Student ID",
        "Name",
        "Department",
        "CGPA",
        "Attendance",
        "Success Score",
        "Academic Risk",
        "Placement Readiness",
        "Priority",
        "Recommended Intervention",
    ]

    st.dataframe(
        filtered_data[display_columns],
        use_container_width=True,
        hide_index=True,
    )

    # Download the intervention report
    csv_data = filtered_data[display_columns].to_csv(index=False)

    st.download_button(
        label="📥 Download Intervention Report",
        data=csv_data,
        file_name="saathi_faculty_intervention_report.csv",
        mime="text/csv",
    )

    st.caption(
        "Priorities are generated using transparent prototype rules. "
        "Faculty should review each case before taking action."
    )
    # ---------------- STUDENT SUCCESS PLAN ----------------

elif page == "Student Success Plan":

    st.title("🎯 Student Success Action Plan")

    st.write(
        "Create personalized improvement plans using student "
        "academic performance, attendance, and placement readiness."
    )

    # Select a student
    selected_student_id = st.selectbox(
        "Select Student",
        students["Student ID"].tolist(),
    )

    student = students[
        students["Student ID"] == selected_student_id
    ].iloc[0]

    # Display student profile
    st.subheader("Student Profile")

    col1, col2, col3 = st.columns(3)

    col1.metric("CGPA", f"{student['CGPA']:.2f}")
    col2.metric("Attendance", f"{student['Attendance']}%")
    col3.metric(
        "Success Score",
        f"{student['Success Score']:.1f}/100",
    )

    st.divider()

    st.subheader("📚 Academic Improvement")

    if student["CGPA"] < 6:
        st.warning(
            "Priority: Academic mentoring and focused revision. "
            "Create a weekly subject-wise study schedule."
        )
    elif student["CGPA"] < 7.5:
        st.info(
            "Target: Improve academic consistency through "
            "weekly revision and practice assessments."
        )
    else:
        st.success(
            "Maintain strong academic performance and participate "
            "in advanced projects."
        )

    st.subheader("📅 Attendance Improvement")

    if student["Attendance"] < 75:
        st.warning(
            "Attendance is below 75%. Meet the faculty mentor "
            "and establish a realistic attendance improvement plan."
        )
    else:
        st.success(
            "Attendance is at least 75%. Maintain regular attendance."
        )

    st.subheader("💼 Placement Preparation")

    if student["Placement Readiness"] < 50:
        st.warning(
            "Focus on aptitude fundamentals, coding basics, "
            "and introductory mock interviews."
        )
    elif student["Placement Readiness"] < 75:
        st.info(
            "Practice coding problems, aptitude tests, "
            "and technical interview questions every week."
        )
    else:
        st.success(
            "Practice advanced coding problems and company-specific "
            "mock interviews."
        )

    st.divider()

    st.subheader("🗓️ Suggested 30-Day Action Plan")

    action_plan = [
        {
            "Week": "Week 1",
            "Activity": "Review academic performance and identify weak areas.",
        },
        {
            "Week": "Week 2",
            "Activity": "Complete focused revision and practice assessments.",
        },
        {
            "Week": "Week 3",
            "Activity": "Practice aptitude, coding, and interview questions.",
        },
        {
            "Week": "Week 4",
            "Activity": "Review progress with the faculty mentor and update goals.",
        },
    ]

    st.dataframe(
        action_plan,
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "This is a suggested, rule-based action plan. "
        "Faculty and students should adapt it to individual needs."
    )

elif page == "Faculty Progress Tracking":

    st.title("📋 Faculty Progress Tracking")

    st.write(
        "Record student interventions and track their progress."
    )

    with st.form("new_intervention_form"):

        st.subheader("Assign a New Intervention")

        student_id = st.selectbox(
            "Select Student",
            students["Student ID"].tolist(),
        )

        selected_student = students[
            students["Student ID"] == student_id
        ].iloc[0]

        intervention = st.selectbox(
            "Intervention Type",
            [
                "Academic Mentoring",
                "Attendance Improvement",
                "Placement Preparation",
                "Technical Skills Development",
                "Soft Skills Development",
            ],
        )
        from ai_engine import generate_student_insight
        
        student_data = selected_student.to_dict()

        with st.spinner("Generating intervention suggestions..."):
                ai_suggestion = generate_student_insight(student_data)

        st.session_state["ai_intervention_suggestion"] = ai_suggestion

        if "ai_intervention_suggestion" in st.session_state:
            st.info(st.session_state["ai_intervention_suggestion"])

        faculty_mentor = st.text_input(
            "Faculty Mentor Name"
        )

        review_date = st.date_input(
            "Review Date"
        )

        submitted = st.form_submit_button(
            "Assign Intervention"
        )

        if submitted:

            if not faculty_mentor.strip():
                st.error("Please enter the faculty mentor's name.")

            else:
                add_intervention(
                    student_id=student_id,
                    student_name=selected_student["Name"],
                    intervention=intervention,
                    faculty_mentor=faculty_mentor.strip(),
                    review_date=review_date,
                )

                st.success("Intervention assigned successfully!")
                st.rerun()

    st.divider()

    st.subheader("Intervention Records")

    records = load_interventions()

    if records:

        records_df = pd.DataFrame(records)

        st.dataframe(
            records_df,
            use_container_width=True,
            hide_index=True,
        )

        for index, record in enumerate(records):

            with st.expander(
                f"{record['student_id']} — {record['intervention']}"
            ):

                st.write(
                    f"**Student:** {record['student_name']}"
                )

                st.write(
                    f"**Faculty Mentor:** {record['faculty_mentor']}"
                )

                st.write(
                    f"**Review Date:** {record['review_date']}"
                )

                current_status = record["status"]

                statuses = [
                    "Not Started",
                    "In Progress",
                    "Completed",
                    "Needs Follow-up",
                ]

                selected_status = st.selectbox(
                    "Update Status",
                    statuses,
                    index=statuses.index(current_status),
                    key=f"status_{index}",
                )

                if st.button(
                    "Save Status",
                    key=f"save_{index}",
                ):

                    update_intervention_status(
                        index,
                        selected_status,
                    )

                    st.success("Status updated successfully!")
                    st.rerun()

        st.download_button(
            "Download Intervention Records",
            data=records_df.to_csv(index=False),
            file_name="faculty_intervention_records.csv",
            mime="text/csv",
        )

    else:

        st.info(
            "No interventions assigned yet. "
            "Create your first intervention above."
        )
elif page == "AI Student Insights":
    from ai_engine import generate_student_insight

    st.title("🤖 AI Student Insights")
    st.write(
        "Generate personalized student support recommendations "
        "using local AI."
    )

    # Select a student
    student_options = students["Student ID"].astype(str).tolist()

    selected_student = st.selectbox(
        "Select a Student",
        student_options
    )

    # Get selected student's information
    student_row = students[
        students["Student ID"].astype(str) == selected_student
    ].iloc[0]

    student_data = student_row.to_dict()
    st.subheader("📊 Student Performance Dashboard")

    # Display available student metrics
    metric_columns = [
        ("Attendance", ["attendance_percentage", "Attendance"]),
        ("Academic Performance", ["average_marks", "Average Marks"]),
        ("Placement Readiness", ["placement_readiness", "Placement Readiness"]),
        ("Success Score", ["success_score", "Success Score"]),
    ]

    metric_values = {}

    for label, possible_columns in metric_columns:
        for column in possible_columns:
            if column in student_row.index:
                metric_values[label] = student_row[column]
                break

    metric_containers = st.columns(4)

    for container, (label, value) in zip(
        metric_containers,
        metric_values.items()
    ):
        container.metric(label, value)

    st.subheader("📊 Student Information")
    st.dataframe(
        student_row.to_frame(name="Value"),
        use_container_width=True
    )

    if st.button("✨ Generate AI Insights", type="primary"):
      with st.spinner("SAATHI AI is analyzing the student..."):
        st.session_state["current_ai_insight"] = generate_student_insight(
            student_data
        )

if st.session_state.get("current_ai_insight"):
    st.subheader("💡 AI-Generated Recommendations")
    st.markdown(st.session_state["current_ai_insight"])
import json
from pathlib import Path
from datetime import datetime

if st.button("📋 Save AI Plan as Draft"):
    draft_file = Path(__file__).parent / "ai_drafts.json"

    draft = {
        "student_id": selected_student,
        "recommendation": st.session_state.get("ai_intervention_draft", {}).get(
        "recommendation", "No AI recommendation generated yet."
),
        "saved_at": datetime.now().isoformat(timespec="seconds"),
        "status": "Pending Faculty Review",
    }

    try:
        if draft_file.exists():
            with open(draft_file, "r", encoding="utf-8") as file:
                drafts = json.load(file)
        else:
            drafts = []

        if not isinstance(drafts, list):
            drafts = []

        drafts.append(draft)

        with open(draft_file, "w", encoding="utf-8") as file:
            json.dump(drafts, file, indent=2, ensure_ascii=False)

        st.session_state["ai_intervention_draft"] = draft
        st.success("AI plan saved permanently for faculty review.")

    except (OSError, json.JSONDecodeError) as error:
        st.error(f"Could not save the AI draft: {error}")
