document.addEventListener("DOMContentLoaded", function(event) { 
    let record, audioContext, gumStream, input;
    record = document.getElementById("record");
    record.onmousedown = e => {
        navigator.mediaDevices.getUserMedia({audio:true}).then(stream => {
            audioContext = new AudioContext();
            input = audioContext.createMediaStreamSource(stream);
            gumStream = stream;
            rec = new Recorder(input, {
                numChannels: 1
            })
            rec.record();
        })
        record.style.backgroundColor = "blue"
    }
    record.onmouseup = e => {
        record.style.backgroundColor = "red"
        rec.stop();
        gumStream.getAudioTracks()[0].stop();
        rec.exportWAV(createDownloadLink);
    }
    record.onclick = e => {
        e.preventDefault();
    }
});

function createDownloadLink(blob) {
    let formData = new FormData();
    let reader = new FileReader();
    formData.append("language", document.getElementsByTagName('select')['language'].value);
    reader.readAsDataURL(blob);
    reader.onloadend = function() {
        let base64data = reader.result.split(',')[1];
        formData.append("audio_file", base64data);

        spinner.style.display = "block";
        submitButton.disabled = true;
        record.disabled = true;

        fetch("/search", {
            method: "POST",
            body: formData
        }).then(response => {
            return response.json();
        }).then(data => {
            handleReply(data, true);
        })
    }
}

const form = document.getElementById("form");
const spinner = document.getElementById("spinner");
const submitButton = document.getElementById("submit-button");

submitButton.addEventListener("click", e => {
    let formData = new FormData();
    formData.append("language", document.getElementsByTagName('select')['language'].value);
    formData.append("service", document.getElementsByTagName("input")['service'].value);

    spinner.style.display = "block";
    submitButton.disabled = true;
    record.disabled = true;

    fetch("/search", {
        method: "POST",
        body: formData
    }).then(response => {
        return response.json();
    }).then(data => {
        handleReply(data);
    })
});

function handleReply(response, isSpeech) {
    console.log(response);
    if (response.status == 302) {
        window.location.href = window.location.origin + response.url;
    }
    else if (response.status < 200 || response.status >= 400) {
        alert(response.error);
    }
    else {
        displayResults(response, isSpeech);
    }

    spinner.style.display = "none";
    submitButton.disabled = false;
    record.disabled = false;

}

function displayResults(response, isSpeech) {
    let internship = response.internship
    let internlist = response.internship_resources
    let c_s = response.c_s;
    let stringlist = response.stringlist;
    let urls = response.urls;
    let len = response.len;

    let result = document.getElementById("results");
    result.style.display = "block";
    result.innerHTML = "";

    let speech = document.getElementById("speech");
    speech.hidden = true;
    speech.innerHTML = "";

    let result_header = document.getElementById("result-header");
    result_header.style.display = "block";

    if (isSpeech) {
        let speech = document.getElementById("speech");
        speech.hidden = false;
        speech.innerHTML = "You asked: " + response.speech;
    }

    if(internship) {
        let ul = document.createElement("ul");
        ul.innerHTML = "These are the links that you can find internships!";
        for(let i=0;i<internlist.length;i++){
            let li = document.createElement("li");
            let a = document.createElement("a");
            a.href = internlist[i][1];
            a.target = "_blank";
            a.innerHTML = internlist[i][0];
            li.appendChild(a);
            ul.appendChild(li);
        }
        result.appendChild(ul)
        if(c_s){
            let li = document.createElement("li");
            li.innerHTML = "There's also a computer science and engineering group in linkedin! Search for Computer Majors - LaGuardia Community College";
            result.appendChild(li)
        }
        result.appendChild(document.createElement("br"));
    }
    else {
        for (let i = 0; i < len; i++) {
            let p = document.createElement("p");
            p.innerHTML = stringlist[i];
            let a = document.createElement("a");
            a.href = urls[i];
            a.target = "_blank";
            a.innerHTML = urls[i];
            p.appendChild(a);
            result.appendChild(p);
        }
        let p = document.createElement("p");
        p.innerHTML = stringlist[len];
        result.appendChild(p);
    }
}
