const form = document.getElementById("image-upload-form");
const url = "/api/ephemeral";


function uploadImage() {

    const formData = new FormData();


    input_docstring = document.getElementById('fname').value
    // Send the request
    fetch(
        url,
        {
            method: 'POST',
            body: input_docstring
        }
    ).then((response) => {
        if (response.status == 200) {
            // The request worked
            document.getElementById('code').innerHTML = "";
            return response.text().then((response_text) => {
                document.getElementById('code').value = response_text;
            });
        } else {
            // The request failed, so let's send the error to the user
            document.getElementById('code').value = "";
            return response.text().then((response_text) => {
                console.log(response_text);
                document.getElementById('code').value = "Error: " + response_text;
            });
        }
    })
    ;
    return false;
}
