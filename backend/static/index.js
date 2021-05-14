const form = document.getElementById("image-upload-form");
const url = "/api/ephemeral";

// Indicate that the user has selected an image
function change() {
    document.getElementById("drag").innerHTML = "1 Image Selected";
}

// Take the LaTeX code and compile it into an image
async function compile() {
    document.getElementById("compText").innerHTML = "Re-Compile LaTeX"
    document.getElementById("compileDiv").style.visibility = "hidden";
        document.getElementById("compile").style.visibility = "hidden";
    var latex = document.getElementById('code').value;
    document.getElementById('compile').src = String.raw`https://latex.codecogs.com/png.latex?\dpi{400}${latex}`;
    
    setTimeout(function(){
        var width = document.getElementById('compile').clientWidth;
        var height = document.getElementById('compile').clientHeight;
    }, 2000);

    setTimeout(function(){
        var width = document.getElementById('compile').clientWidth;
        var height = document.getElementById('compile').clientHeight;
        document.getElementById("compileDiv").style.width = `${width + 30}px`;
        document.getElementById("compileDiv").style.height = `${height + 30}px`;
        document.getElementById("compileDiv").style.visibility = "visible";
        document.getElementById("compile").style.visibility = "visible";
    }, 2500);
}

// Send the LaTeX to wolfram alpha and display the result to the user
function wolfram() {
    var latex = document.getElementById('code').value;
    document.getElementById("wolframDiv").style.visibility = "visible";
    var encodedURL = encodeURIComponent(`${latex}`);
    document.getElementById('wolfram').src = String.raw`https://api.wolframalpha.com/v1/simple?appid=TUXUG5-KEW895XAX3&&background=193555&foreground=white&i=${encodedURL}`;
}

// Take the provided image and send it to the server to convert to LaTeX,
// then get the result and display it
function uploadImage() {
    document.getElementById('code').value = 'Loading...';
    document.getElementById('textForUpload').style.visibility = "visible";
    document.getElementById("drag").innerHTML = "Drag your image or click in the area"; 
    // Add the image to the request
    const files = document.querySelector('[type=file]').files;
    const formData = new FormData();
    if (files.length == 0) {
        document.getElementById('code').value = 'No Image Uploaded, please try again!';
        return false;
    }
    var image = document.getElementById('image');
    image.src = URL.createObjectURL(files[0]);
    for (let i = 0; i < files.length; i++) {
        let file = files[i];
        formData.append('image', file);
    }
    // Send the request
    fetch(
        url,
        {
            method: 'POST',
            body: formData,
        }
    ).then((response) => {
        if (response.status == 200) {
            // The request worked
            document.getElementById('error').innerHTML = "";
            return response.text().then((response_text) => {
                document.getElementById('code').value = response_text;
            });
        } else {
            // The request failed, so let's send the error to the user
            document.getElementById('code').value = "";
            return response.text().then((response_text) => {
                console.log(response_text);
                document.getElementById('error').value = "Error: " + response_text;
            });
        }
    })
    ;
    return false;
}

function copy(){
    var copyText = document.getElementById("code");
    copyText.select();
    copyText.setSelectionRange(0, 99999)
    document.execCommand("copy");

    var tooltip = document.getElementById("myTooltip");
    tooltip.innerHTML = "Copied: " + copyText.value;
}

function outFunc() {
    var tooltip = document.getElementById("myTooltip");
    tooltip.innerHTML = "Copy to clipboard";
  }

function save_permalink() {
    document.getElementById('permalink').innerHTML = 'Loading...';
    // Add the file to the image
    const files = document.querySelector('[type=file]').files;
    const formData = new FormData();
    if (files.length == 0) {
        document.getElementById('error').innerHTML = 'No Image Uploaded, please try again!';
        return false;
    }

    var image = document.getElementById('image');
    image.src = URL.createObjectURL(files[0]);
    for (let i = 0; i < files.length; i++) {
        let file = files[i];
        formData.append('image', file);
    }
    formData.append('latex', document.getElementById('code').value);
    fetch(
        "/api/upload",
        {
            method: 'POST',
            body: formData,
        }
    ).then((response) => {
        if (response.status == 200) {
            document.getElementById('error').innerHTML = "";
            return response.text().then((response_text) => {
                document.getElementById("perma").style.visibility = "visible";
                document.getElementById('permalink').innerHTML = "https://image-to-latex-backend.herokuapp.com/static/index.html?image=" + response_text;
                document.getElementById('permalink').href = "https://image-to-latex-backend.herokuapp.com/static/index.html?image=" + response_text;
            });
        } else {
            document.getElementById('permalink').innerHTML = "";
            return response.text().then((response_text) => {
                console.log(response_text);
                document.getElementById('error').innerHTML = "Error: " + response_text;
            });
        }
    })
    ;
    return false;
}

// Request the server for the image and LaTeX that was stored for the given key
function fetch_key() {
    const params = new URLSearchParams(window.location.search);
    if (!params.has("image")) {
        return;
    }
    fetch("/api/download?image="+params.get("image")).then((response) => {
        if (response.status == 200) {
            document.getElementById('error').innerHTML = "";
            response.text().then((response_text) => {
                var body = JSON.parse(response_text);
                document.getElementById('code').value = body.latex;
                document.getElementById('image').src = 'data:image;base64,' + body.image;
                document.getElementById('permalink').innerHTML = "Permalink to this result: https://image-to-latex-backend.herokuapp.com/static/index.html?image=" + params.get("image");
            });
        } else {
            return response.text().then((response_text) => {
                console.log(response_text);
                document.getElementById('error').innerHTML = "Error: " + response_text;
            });
        }
    });
}
window.onload = fetch_key;
