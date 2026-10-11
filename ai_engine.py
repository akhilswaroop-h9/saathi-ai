import os
import streamlit as st
from groq import Groq


def generate_student_insight(student_data):
    """Generate AI-powered student support recommendations."""

    prompt = f"""
You are SAATHI AI, a respectful student-success assistant.

Analyze the following student data:
{student_data}

Provide:
1. A summary of current performance.
2. Academic or attendance concerns supported by the data.
3. Three practical recommendations.
4. One immediate action for faculty.
5. A simple 7-day support plan.

Rules:
- Use only the supplied information.
- Do not invent missing values.
- Use clear, respectful language.
- Treat recommendations as guidance, not validated predictions.
"""

    try:
        api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

        if not api_key:
            return (
                "AI service is not configured. "
                "Please add GROQ_API_KEY to Streamlit Secrets."
            )

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
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.3,
        )

        return response.choices[0].message.content or (
            "The AI did not return a response."
        )

    except Exception as error:
        print(f"SAATHI AI error: {type(error).__name__}: {error}")
        return "SAATHI AI could not generate a response. Please try again."
