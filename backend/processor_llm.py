import os
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Initialize Groq client with proxy workaround
try:
    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
except TypeError:
    # Fallback for proxy issues
    from groq._base_client import SyncHttpxClientWrapper
    groq_client = Groq(
        api_key=os.getenv("GROQ_API_KEY"),
        http_client=SyncHttpxClientWrapper(proxies=None)
    )

def classify_with_llm(log_msg: str) -> str:
    """
    Generate a variant of the input sentence. For example,
    If input sentence is "User session timed out unexpectedly, user ID: 9250.",
    variant would be "Session timed out for user 9251"
    """
    prompt = f'''Classify the log message into one of these categories: 
    (1) Workflow Error, (2) Deprecation Warning.
    If you can't figure out a category, use "Unclassified".
    Put the category inside <category> </category> tags. 
    Log message: {log_msg}'''

    chat_completion = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="gemma2-9b-it",
        temperature=0.5
    )

    content = chat_completion.choices[0].message.content
    match = re.search(r'<category>(.*)<\/category>', content, flags=re.DOTALL)
    category = "Unclassified"
    if match:
        category = match.group(1)

    return category


if __name__ == "__main__":
    print(classify_with_llm(
        "Case escalation for ticket ID 7324 failed because the assigned support agent is no longer active."))
    print(classify_with_llm(
        "The 'ReportGenerator' module will be retired in version 4.0. Please migrate to the 'AdvancedAnalyticsSuite' by Dec 2025"))
    print(classify_with_llm("System reboot initiated by user 12345."))