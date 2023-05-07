import re
from base64 import b64decode
from io import BytesIO

import speech_recognition as sr
from flask import Blueprint, redirect, request
from openai.error import AuthenticationError

import hackathon.models as models
from hackathon.utils import ask_chat_gpt, speech_to_text

search_bp = Blueprint('search', __name__)

# Dictionary mapping services to URLs
services = {
    "Tutor": "https://www.laguardia.edu/current-students/academic-help-tutoring/",
    "Financial": "https://www.laguardia.edu/financialaid/",
    "Academic": "https://www.laguardia.edu/advising/",
    "Career": "https://www.laguardia.edu/careerservices/",
    "MEC": "https://www.laguardia.edu/mec/home/",
    "Writing": "https://www.laguardia.edu/writingcenter/",
    "API": "https://www.laguardia.edu/academics/programs/api/meet-our-tutors/",
    "Wellness": "https://www.laguardia.edu/wellnesscenter/",
    "Calendar": "https://www.laguardia.edu/uploadedfiles/main_site/content/academics/academic_calendar/pdf/academic-calendar-2022-23.pdf"
}

internship_resources = [
    ["LinkedIn", "https://www.linkedin.com/"],
    ["LAGCC Job Postings", "https://www.laguardia.edu/careerservices/job-posting/"],
    ["Indeed", "https://www.indeed.com/"],
]


@search_bp.route('/search', methods=["GET", "POST"])
def search():
    if request.method == 'GET':
        return redirect('/')

    reply = {
        "status": 200,
        "url": "",
        "answer": "",
        "stringlist": [],
        "urls": [],
        "len": 0,
        "speech": "",
        "internship": False,
        "internship_resources": internship_resources,
        "c_s": False
    }

    if "service" in request.form:
        service = request.form["service"]

    language = request.form["language"]
    speech = ""

    if "audio_file" in request.form and request.form["audio_file"] != "":
        audio_base64 = request.form["audio_file"]
        audio = BytesIO(b64decode(audio_base64))
        try:
            speech_language = models.LanguageModel.__dict__[language]
            service = speech_to_text(audio, speech_language)
            speech = service
        except sr.UnknownValueError:
            reply = {
                "status": 400,
                "error": "Google Speech Recognition could not understand audio"
            }
            return reply
        except sr.RequestError as e:
            reply = {
                "status": 500,
                "error": f"Could not request results from Google Speech Recognition service; {e}"
            }
            return reply

    internship = True if "internship" in service.lower() else False
    cs = True if "computer science" in service.lower() else False

    reply["internship"] = internship
    reply["c_s"] = cs
    reply["speech"] = speech

    if internship:
        return reply

    if not service:
        reply["status"] = 302
        reply["url"] = "/resources"
        return reply

    initial_prompt = models.InitialPrompt.__dict__[language] + str(services)
    try:
        answer = ask_chat_gpt(initial_prompt + service + "\n")
    except AuthenticationError:
        reply = {
            "status": 500,
            "error": "Invalid API key for OpenAI. Please check your .env file."
        }
        return reply

    # Check if the answer matches one of the services in the dictionary
    urls = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\d_?&=#%+()~.,!:-]*', answer)
    strlist = []
    j = 0
    for i in urls:
        index = answer.find(i)
        strlist += [answer[j:index]]
        j = index + len(i)
    strlist += [answer[j:]]

    # Render the template with the answer and service links
    reply.update({
        "answer": answer,
        "stringlist": strlist,
        "urls": urls,
        "len": len(urls)
    })
    return reply
