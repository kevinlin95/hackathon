var record;
var audioContext;
var gumStream;
var input;

function handlerFunction(stream) {
    audioContext = new AudioContext();
    input = audioContext.createMediaStreamSource(stream);
    gumStream = stream;
    rec = new Recorder(input, {
        numChannels: 1
    })
    rec.record();
}

function createDownloadLink(blob) {

    let form = document.getElementById("form");
    let reader = new FileReader();
    reader.readAsDataURL(blob); 
    reader.onloadend = function() {
        var base64data = reader.result.split(',')[1];
        var x = document.createElement("INPUT");

        x.setAttribute("type", "text");
        x.setAttribute("value", base64data);
        x.setAttribute("name", "audio_file");
        x.setAttribute("id", "audio_file");
        x.setAttribute("hidden", "true");

        form.appendChild(x);
        form.submit();

        spinner.style.display = "block";
        submitButton.disabled = true;
        record.disabled = true;
    }

}

document.addEventListener("DOMContentLoaded", function(event) { 
    record = document.getElementById("record");
    record.onmousedown = e => {
        navigator.mediaDevices.getUserMedia({audio:true}).then(stream => {handlerFunction(stream)})
        console.log('I was clicked');
        record.style.backgroundColor = "blue"
    }
    record.onmouseup = e => {
        record.style.backgroundColor = "red"
        rec.stop();
        gumStream.getAudioTracks()[0].stop();
        rec.exportWAV(createDownloadLink);
    }
});

const form = document.getElementById("form");
const spinner = document.getElementById("spinner");
const submitButton = document.getElementById("submit-button");

form.addEventListener("submit", function() {
    spinner.style.display = "block";
    submitButton.disabled = true;
    record.disabled = true;
});
