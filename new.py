import google.generativeai as genai

# Configure API key
genai.configure(api_key='AIzaSyB85grkuY-LWonZ6yit-jk2EOsfadWY3cg')

# Create GenerativeModel instance
model = genai.GenerativeModel('gemini-1.5-flash')

response = model.generate_content("What is the capital of Maharashtra?")
print(response.text)
