import google.generativeai as genai
genai.configure(api_key="AIzaSyCgWELq-jrAZdlvrLNY1v40TxBOBUV6rxs")
model = genai.GenerativeModel("models/gemini-2.5-flash")
response = model.generate_content([
    {"role": "user", "parts": "What is coding?"}
])
print(response.text)
