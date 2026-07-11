import re
import subprocess
import sys
from pathlib import Path
from groq import Groq

client = Groq()

def extract_code(text):
    pattern = r"```(?:python)?\n(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

def ask_model_with_history(messages):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_completion_tokens=800,
    )
    return completion.choices[0].message.content

def execute_code(code):
    filepath = Path("generated.py")
    filepath.write_text(code)
    try:
        result = subprocess.run(
            [sys.executable, str(filepath)],
            capture_output=True, text=True, timeout=10
        )
        return {"exit_code": result.returncode, "stdout": result.stdout,
                "stderr": result.stderr, "timed_out": False}
    except subprocess.TimeoutExpired:
        return {"exit_code": None, "stdout": "",
                "stderr": "Process timed out after 10 seconds", "timed_out": True}