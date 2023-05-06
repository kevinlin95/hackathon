from base64 import b64decode
from io import BytesIO

import re
import speech_recognition as sr
from flask import Blueprint, redirect, render_template, request
from openai.error import AuthenticationError

from hackathon.utils import ask_chat_gpt, speech_to_text

search_bp = Blueprint('search', __name__)


# Dictionary mapping services to URLs
services = {
    "Tutor": "https://www.laguardia.edu/current-students/academic-help-tutoring/",
    "Financial": "https://www.laguardia.edu/financialaid/",
    "Academic": "https://www.laguardia.edu/advising/",
    "Career": "https://www.laguardia.edu/Career-Services/",
    "MEC":"https://www.laguardia.edu/mec/home/",
    "Writing":"https://www.laguardia.edu/writingcenter/",
    "API":"https://www.laguardia.edu/academics/programs/api/meet-our-tutors/",
    "Wellness":"https://www.laguardia.edu/wellnesscenter/",
    "Calender":"https://www.laguardia.edu/uploadedfiles/main_site/content/academics/academic_calendar/pdf/academic-calendar-2022-23.pdf"
}

internship_resources = [
    ["LinkedIn", "https://www.linkedin.com/"],
    ["LAGCC Job Postings", "https://www.laguardia.edu/careerservices/job-posting/"],
    ["Indeed","https://www.indeed.com/"],
]

# Prompt to use for the ChatGPT API
prompt = "I want you to act as a LaGuardia Community College adviser. You must be friendly and polite. These are the only resources that you can show them "+str(services)


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
            return render_template('search.html', answer="Here are some internship resources:", service_links=internship_resources, gpt = False)

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
    urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\d_?&=#%+()~.,!:-]*', answer)
    # print(urls)
    strlist = []
    j = 0
    if urls!= []:
        for i in urls:
            index = answer.find(i)
            # print(index)
            strlist += [answer[j:index]]
            j = index + len(i)
    strlist += [answer[j:]]

    # Render the template with the answer and service links
    return render_template('search.html', answer=answer, stringlist = strlist, urls = urls, len = len(urls), gpt = True)
