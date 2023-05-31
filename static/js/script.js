console.log('asdasdasdasdasdasdads')
imageURL=''
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

    let charNamesElements = document.getElementsByClassName('charName')    
    let speakerLabelElements = document.getElementsByClassName('speakerLabel')
    let charNames = []
    let speakerLabels = []



    // for()
    for(var i=0; i<charNamesElements.length; i++){
      charNames.push(charNamesElements[i].value)
    }
    for(var i=0; i<speakerLabelElements.length; i++){
      speakerLabels.push(speakerLabelElements[i].value)
    }

    // console.log(charNames)
    // console.log(speakerLabels)
    let updatedTranscribedText = transcribedText
    for(var i=0; i<speakerLabelElements.length; i++){
      updatedTranscribedText = updatedTranscribedText.replaceAll(speakerLabels[i], charNames[i])
    }
    
    //Add character descriptions
    var charDescriptions = ''
    for(var i=0; i<charNamesElements.length; i++){
      var char = charNames[i].toLowerCase()
      if(bbtCharacters.char)
        charDescriptions += bbtCharacters.char
    }
    updatedTranscribedText = charDescriptions+updatedTranscribedText

    const data = { 'prompt': updatedTranscribedText, 'tvshow':tvshow, 'customReq':customreq };

    console.log(data['prompt'])

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


function generateComic(event){
  event.preventDefault()
  console.log('API is being called')
  let spinner = document.getElementById('spinner3Div')
  spinner.style.display='block'
  let comicSection = document.getElementById('comicSection')
  comicSection.style.display = 'block'
  let script = document.getElementById('gptGeneratedScript').value
  let imageModel = document.getElementById('imageModel').value
  let tvshow = document.getElementById('tvshow').value
  let customReq = document.getElementById('customReq').value
  
  const data = { 'script': script, 'imageModel':imageModel, 'tvshow':tvshow, 'customReq':customReq};
  console.log(data)

  fetch('http://127.0.0.1:5000/api/generate_comic', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
    .then(response => response.json())
    .then(result => {
      console.log(result)
      spinner.style.display='none'
      if(result['status'] == '200'){     
          let comicElement = document.getElementById('comic')
          comicElement.src = result['url'] 
          imageURL=result['url']         
          let comicSectionButtons = document.getElementById('comicSectionButtons')
          comicSectionButtons.style.display = 'block'
      }
      else
          alert('An error occurred. Please try again later. Status - ',result['status'])
    })
    .catch(error => {
      console.error('Error:', error);
      alert('An error occurred. Please try again')
    });
}

function regenerateComic(event) {
  event.preventDefault();
  console.log('Regenerating comic...');
  generateComic(event);
}

var fieldCounter = 1;

function addFormField() {
    var container = document.getElementById("speakerLabels");

    // Create a new form field container
    var fieldContainer = document.createElement("div");
    fieldContainer.className = "charNameDiv row";

    // Create new input fields
    var newField = document.createElement("input");
    newField.id = 'speakerLabel'+fieldCounter
    newField.type = "text";
    newField.name = "dynamicField" + fieldCounter;
    newField.className = "speakerLabel form-field form-control col-4";
    newField.placeholder = "Given Speaker label";

    var newFieldContainer = document.createElement("div");
    newFieldContainer.className = "col my-2";
    newFieldContainer.appendChild(newField)
    
    var newField1 = document.createElement("input");
    newField1.id = "charName"+fieldCounter
    newField1.type = "text";
    newField1.name = "dynamicField" + fieldCounter;
    newField1.className = "charName form-control col-4";
    newField1.placeholder = "Corresponding Character Name";

    var newField1Container = document.createElement("div");
    newField1Container.className = "col my-2";
    newField1Container.appendChild(newField1)

    // Create a remove button
    var removeButton = document.createElement("button");
    removeButton.type = "button";
    removeButton.className = "btn btn-sm btn-light px-4"
    removeButton.innerHTML = "Remove";
    removeButton.addEventListener("click", function() {
        container.removeChild(fieldContainer);
    });

    var removeButtonContainer = document.createElement("div");
    removeButtonContainer.className = "col my-2";
    removeButtonContainer.appendChild(removeButton)

    // Append the new field and remove button to the field container
    fieldContainer.appendChild(newFieldContainer);
    fieldContainer.appendChild(newField1Container);
    fieldContainer.appendChild(removeButtonContainer);

    // Append the field container to the form container
    container.appendChild(fieldContainer);

    fieldCounter++;
}