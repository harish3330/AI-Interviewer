from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_interview_questions(topic, skills, level):
    prompt = f"""
    Generate exactly 5 interview questions.
    Role: {topic}
    Skills: {skills}
    Level: {level}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        text = response.choices[0].message.content
        questions = text.split("\n")

        return [q.strip("0123456789. ").strip() for q in questions if q.strip()][:5]

    except Exception as e:
        
        return [
            f"What is {topic}?",
            f"Explain core concepts of {skills}.",
            f"Difference between beginner and advanced concepts in {topic}?",
            f"How do you handle errors in {topic}?",
            f"Explain a real-world use case of {topic}."
        ]
