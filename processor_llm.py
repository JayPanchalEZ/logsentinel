from dotenv import load_dotenv
from groq import Groq
load_dotenv()

groq = Groq()

def classify_with_llm(log_msg):
    prompt = f"""
    Classify this log into one of these categories:
    - failed_login
    - brute_force_attempt
    - possible_attack
    - suspicious_activity
    - normal_activity
    - system_event

    Only return the label name.

    Log: {log_msg}
    """

    chat_completion = groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    response = chat_completion.choices[0].message.content.strip().lower()

    allowed_labels = [
        "failed_login",
        "brute_force_attempt",
        "possible_attack",
        "suspicious_activity",
        "normal_activity",
        "system_event"
    ]

    if response not in allowed_labels:
        return "suspicious_activity"

    return response

# if __name__ == "__main__":
#     print(classify_with_llm(
#         "Case escalation for ticket ID 7324 failed because the assigned support agent is no longer active."))
#     print(classify_with_llm(
#         "The 'ReportGenerator' module will be retired in version 4.0. Please migrate to the 'AdvancedAnalyticsSuite' by Dec 2025"))
#     print(classify_with_llm("System reboot initiated by user 12345."))