import openai
from flask import Blueprint, redirect, render_template, request

from config import Config

search_bp = Blueprint('search', __name__)
openai.api_key = Config.OPENAI_API_KEY


# Dictionary mapping services to URLs
services = {
    "Tutoring": "https://www.laguardia.edu/Tutoring/",
    "Financial Aid": "https://www.laguardia.edu/Financial-Aid/",
    "Academic Advising": "https://www.laguardia.edu/Academic-Advising/",
    "Career Services": "https://www.laguardia.edu/Career-Services/"
}

# Prompt to use for the ChatGPT API
prompt = "I want you to act as a LaGuardia Community College mentor. You must be friendly and polite. Your job is to quickly guide students to the information and resources they are looking for. Please jump straight to the answer, and do not include any unnecessary phrases or introductions. Only respond to academic searches related to LaGuardia Community College. Otherwise, please respond with 'No available resources'."


@search_bp.route('/search', methods=["GET", "POST"])
def search():
    available_services = [_.lower() for _ in services.keys()]
    if request.method == 'GET':
        return render_template('index.html')

    service = request.form["service"]
    if service.lower() in available_services:
        keyname = list(services.keys())[available_services.index(service.lower())]
        return redirect(services[keyname])

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
    answer: str = response.choices[0].text.strip()

    # Check if the answer matches one of the services in the dictionary
    service_links = []
    for word in answer.lower().split():
        if word in available_services:
            # If it does, add a link to the corresponding service
            keyname = list(services.keys())[available_services.index(word)]
            service_links.append((word.capitalize(), services[keyname]))

    # Render the template with the answer and service links
    return render_template('search.html', answer=answer, service_links=service_links)
