document.getElementById('audio-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const audioFile = document.getElementById('audio-file').files[0];
    if (!audioFile) {
        return;
    }

    const formData = new FormData();
    formData.append('audio_file', audioFile);

    const response = await fetch('/', { method: 'POST', body: formData });
    const data = await response.json();

    if (data.result === 'success') {
        document.getElementById('result').textContent = 'Analysis complete!';
    } else {
        document.getElementById('result').textContent = 'Error during analysis';
    }
});

document.getElementById("send_to_openai").addEventListener("click", function(event) {
  event.preventDefault();
  
  // Call the Flask route to send data to OpenAI and get the response
  fetch("/send_to_openai", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({"txt_file": "rgb_colors.txt"})
  })
  .then(response => response.json())
  .then(data => {
    // Update the webpage with the generated text
    document.getElementById("generated_text").innerText = data.generated_text;
  });
});


document.getElementById("submit").addEventListener("click", function(event) {
  event.preventDefault();
  
  // Get the wav file from the input field
  let wavFile = document.getElementById("wav_file").files[0];

  // Create a FormData object and append the wav file
  let formData = new FormData();
  formData.append("wav_file", wavFile);

  // Make an AJAX request to the Flask route
  fetch("/process_wav", {
    method: "POST",
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    // Update the webpage with the returned data
    document.getElementById("rgb_values").innerText = data.rgb_values.join(", ");
  });
});
