from base64 import b64decode
from io import BytesIO

import speech_recognition as sr
from flask import Blueprint, redirect, render_template, request
from openai.error import AuthenticationError

from hackathon.utils import ask_chat_gpt, speech_to_text

search_bp = Blueprint('search', __name__)


# Dictionary mapping services to URLs
services = {
    "Tutoring": "https://www.laguardia.edu/Tutoring/",
    "Financial Aid": "https://www.laguardia.edu/Financial-Aid/",
    "Academic Advising": "https://www.laguardia.edu/Academic-Advising/",
    "Career Services": "https://www.laguardia.edu/Career-Services/"
}

internship_resources = [
    ["LinkedIn", "https://www.linkedin.com/"],
    ["LAGCC Job Postings", "https://www.laguardia.edu/careerservices/job-posting/"]
]

# Prompt to use for the ChatGPT API
prompt = "I want you to act as a LaGuardia Community College mentor. You must be friendly and polite. Your job is to quickly guide students to the information and resources they are looking for. Please jump straight to the answer, and do not include any unnecessary phrases or introductions. Only respond to academic searches related to LaGuardia Community College. Otherwise, please respond with 'No available resources'."


@search_bp.route('/search', methods=["GET", "POST"])
def search():
    if request.method == 'GET':
        return redirect('/')

    available_services = [_.lower() for _ in services.keys()]
    if "service" in request.form:
        service = request.form["service"]
        if service.lower() in available_services:
            keyname = list(services.keys())[available_services.index(service.lower())]
            return redirect(services[keyname])

        if "internship" in service.lower():
            return render_template('search.html', answer="Here are some internship resources:", service_links=internship_resources)

    if "audio_file" in request.form:
        audio_base64 = request.form["audio_file"]
        audio = BytesIO(b64decode(audio_base64))
        try:
            service = speech_to_text(audio)
        except sr.UnknownValueError:
            return render_template('error.html', error="Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            return render_template('error.html', error="Could not request results from Google Speech Recognition service; {0}".format(e))

    try:
        answer = ask_chat_gpt(prompt + "\nStudent question: " + service + "\n")
    except AuthenticationError:
        return render_template('error.html', error="Invalid API key for OpenAI. Please check your .env file.")

    # Check if the answer matches one of the services in the dictionary
    service_links = []
    for word in answer.lower().split():
        if word in available_services:
            # If it does, add a link to the corresponding service
            keyname = list(services.keys())[available_services.index(word)]
            service_links.append((word.capitalize(), services[keyname]))
    service_links = list(set(service_links))
    service_link_title = True if service_links else False

    # Render the template with the answer and service links
    return render_template('search.html', answer=answer, service_link_title=service_link_title, service_links=service_links)
