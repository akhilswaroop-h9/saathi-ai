import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen3:1.7b"


def generate_student_insight(student_data):
    """
    Generate AI-powered student support recommendations
    using the local Ollama model.
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
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
            },
            timeout=180,
        )

        response.raise_for_status()
        result = response.json()

        return result.get(
            "response",
            "The AI did not return a response."
        )

    except requests.exceptions.ConnectionError:
        return (
            "Ollama is not running. "
            "Please start Ollama and try again."
        )

    except requests.exceptions.Timeout:
        return (
            "The AI is taking too long to respond. "
            "Please try again."
        )

    except requests.exceptions.RequestException as error:
        return f"AI request failed: {error}"

    except (ValueError, json.JSONDecodeError):
        return "Could not process the AI response."