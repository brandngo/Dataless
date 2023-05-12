const apiUrl = 'https://modern-nation-385900.uk.r.appspot.com/websim';
const formInput = document.getElementById('formSmsSim')
const formTxt = document.getElementById('formSmsSimTxt')
const replyBox = document.getElementById('textSmsSimReplyBox')

function getForm(event) {
    event.preventDefault();
    if (formTxt.value === "") return
    replyBox.innerHTML += '<div style="border: 1px solid #c7c7c7; border-radius: 8px; background-color: #add8e6; margin-bottom: 5px;"><div style="padding: 3px">' + formTxt.value + '</div></div>'
    
    //if (formTxt.value.search(/^bus_.*_.*/)) {
        targets = formTxt.value.split("_")
        formTxt.value = ""
        targets.shift()
        if (targets.length == 2) {
            fetchData(targets[0], targets[1])
        }
    //}
    
}

function fetchData(origin, dest) {
    const url = `${apiUrl}?origin=${origin}&dest=${dest}`;

    fetch(url)
        .then(response => {
            if (response.ok) {
            return response.json();
            } else {
            throw new Error('Error: ' + response.status);
            }
        })
    .then(data => {
        replyBox.innerHTML += '<div style="border: 1px solid #c7c7c7; border-radius: 8px; background-color: #D3D3D3; margin-bottom: 5px;"><div style="padding: 3px">' + data.data + '</div></div>'
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
