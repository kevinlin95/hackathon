<h1 align="center">LaGuardia Express Search</h1>

<p align="center">
  <img src="https://raw.githubusercontent.com/MateoNitro550/hackathon/main/hackathon/static/assets/home.png">
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/MateoNitro550/hackathon/main/hackathon/static/assets/resources.png">
</p>

LaGuardia Express Search is a powerful tool designed to help LaGuardia Community College students quickly find the information and resources they need. Our application offers both text-based search and speech-to-text search capabilities for English, Spanish, and Chinese languages.

## How It Works

LaGuardia Express Search works by using the powerful GPT-3 natural language processing engine to provide quick and accurate responses to user queries. Users simply enter a search term, and our application will provide a response with relevant links to LaGuardia's tutoring, financial aid, academic advising, career services, and other important resources.

## Speech-to-Text Capabilities

In addition to traditional text-based search, our application also offers speech-to-text capabilities for English, Spanish, and Chinese languages. We use the FFmpeg library to convert audio files into text, which is then processed by our GPT-3 engine for relevant responses.

## Setup
```
$ git clone https://github.com/MateoNitro550/hackathon
$ cd hackathon
$ python3 -m venv env
$ env/bin/activate
$ pip install -r requirements.txt
```

## Run
```
$ python3 main.py
```
or
```
$ python3 main.py --mode prod
```
