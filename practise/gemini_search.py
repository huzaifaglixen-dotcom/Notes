

# Sahi import line (Google ki official library se import karne ke liye)
from google import genai

# Gemini Client setup (Apni valid API key quotes ke andar likhein)
client = genai.Client(
    api_key="Your_Google_API_Key_Here"
)

# Send Prompt
response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents="Hello Gemini! Who are you?"
)

# Print Response
print(response.text)