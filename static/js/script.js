console.log('asdasdasdasdasdasdads')
function transcribeAudio(event) {
    event.preventDefault()
    let spinner = document.getElementById('spinner1Div')
    spinner.style.display='block'
    console.log('asda')
    let url = document.getElementById('youtubeURL').value
    const data = { youtube_url: url };
  
    fetch('http://127.0.0.1:5000/api/transcribe_audio', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
      .then(response => response.json())
      .then(result => {
        spinner.style.display='none'
        if(result['status'] == '200'){
            console.log(result);        
            var textArea = document.getElementById('transcribedText')
            textArea.value=result['transcription']
            textArea.disabled = false
            document.getElementById('tvshow').disabled = false
            document.getElementById('customReq').disabled = false
        }
        else
            alert('An error occurred. Please try again later. Status - ',result['status'])
      })
      .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again')
      });
}

function generateGptScript(event){
    event.preventDefault();
    console.log('API is being called')
    let spinner = document.getElementById('spinner2Div')
    spinner.style.display='block'
    let tvshow = document.getElementById('tvshow').value
    let customreq = document.getElementById('customReq').value
    let transcribedText = document.getElementById('transcribedText').value
    
    const data = { 'prompt': transcribedText, 'tvshow':tvshow, 'customReq':customreq };

    fetch('http://127.0.0.1:5000/api/generate_script', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
      .then(response => response.json())
      .then(result => {
        console.log(Object.keys(result))
        console.log(result)
        console.log(result['status']+'\n'+result['script'])
        spinner.style.display='none'
        if(result['status'] == '200'){     
            var textArea = document.getElementById('gptGeneratedScript')
            textArea.value=result['script']
            textArea.disabled = false
        }
        else
            alert('An error occurred. Please try again later. Status - ',result['status'])
      })
      .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again')
      });
}