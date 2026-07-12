# stage1.py
import re
from groq import Groq  
from llm_utils import extract_code

# 1. Create an instance of the Groq client

client = Groq()

# 2. Call the API

completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
      {
        "role": "user",
        "content": "Write a Python function that reverses a string."
      }
    ],
    max_completion_tokens=800,
    stream=False,
)

# 3. Look at the raw response object first — see its full shape
# print(completion)
print(completion.choices[0].finish_reason)
print("---")

# 4. Now pull out just the text.

text = completion.choices[0].message.content
print(text)

# available in llm_utils.py
# def extract_code(text):


text = completion.choices[0].message.content
code = extract_code(text)
print("EXTRACTED CODE:")
print(code)
print("---")
print("Does it contain reverse_string?", "reverse_string" in code)
print("Does it contain the test block?", "__main__" in code)