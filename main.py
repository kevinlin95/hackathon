from flask import Flask, request, render_template
import openai
import os

app = Flask(__name__)

# Configure OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Dictionary mapping services to URLs
services = {
    "Tutoring": "https://www.laguardia.edu/Tutoring/",
    "Financial Aid": "https://www.laguardia.edu/Financial-Aid/",
    "Academic Advising": "https://www.laguardia.edu/Academic-Advising/",
    "Career Services": "https://www.laguardia.edu/Career-Services/"
}

# Prompt to use for the ChatGPT API
prompt = "I want you to act as a LaGuardia Community College mentor. You must be friendly and polite. Your job is to quickly guide students to the information and resources they are looking for. Please jump straight to the answer, and do not include any unnecessary phrases or introductions. Only respond to academic searches related to LaGuardia Community College. Otherwise, please respond with 'No available resources'."

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == 'POST':
        try:
            service = request.form["service"]
            if service.lower() in services:
                return redirect(services[service.lower()])
        except KeyError:
            pass
    
    else:
        # Render the index template for GET requests
        return render_template('index.html')
    
    # Call the ChatGPT API with the question and prompt
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt + "\nStudent question: " + service + "\n",
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    # Extract the answer from the response
    answer = response.choices[0].text.strip()

    # Check if the answer matches one of the services in the dictionary
    service_links = []
    service_names = set(services.keys())
    for word in answer.lower().split():
        if word in service_names:
            # If it does, add a link to the corresponding service
            service_links.append((word.capitalize(), services[word]))
    
    # Render the template with the answer and service links
    return render_template('search.html', answer=answer, service_links=service_links)

if __name__ == "__main__":
    app.run(debug=True)
