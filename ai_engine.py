import os
import json
import streamlit as st
from groq import Groq


def generate_student_insight(student_data):
    """
    Generate student support recommendations using a hosted AI model.
    """

    prompt = f"""
You are SAATHI AI, a college student success assistant.

Analyze the following student data:
{json.dumps(student_data, indent=2, default=str)}

Your tasks:
1. Summarize the student's current performance.
2. Identify concerns using the supplied data.
3. Review attendance and academic performance when available.
4. Review engagement, LMS activity, and placement readiness when available.
5. Recommend three practical, personalized actions.
6. Suggest one follow-up action for faculty.
7. Provide a supportive message for the student.
8. Suggest one immediate action for faculty.
9. Create a practical 7-day support plan.
10. Recommend one measurable 30-day goal and a follow-up method.

Rules:
- Use only information present in the supplied data.
- Do not invent missing values or assume missing data indicates poor performance.
- If a metric is unavailable, say so.
- Explain recommendations in simple, respectful language.
- Treat your output as guidance for faculty review, not a validated prediction.
"""

    try:
        api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

        if not api_key:
            return "AI service is not configured. Please add GROQ_API_KEY in Streamlit Secrets."

        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are SAATHI AI, a respectful student-success "
                        "assistant. Provide practical, evidence-based guidance."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )

        return response.choices[0].message.content or (
            "The AI did not return a response."
        )
        except Exception as error:
            print(f"SAATHI AI error: {type(error).__name__}: {error}")
            return "SAATHI AI could not generate a response. Please try again."
