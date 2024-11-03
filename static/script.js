const imgurClientId = 'a15f86a39c45ffe'; // Replace with your Imgur Client ID

function addRow() {
  const form = document.getElementById("dynamicForm");

  // Create a new form row div
  const formRow = document.createElement("div");
  formRow.classList.add("form-row");

  // Create text input for the row
  const textInput = document.createElement("input");
  textInput.type = "text";
  textInput.name = "textInput[]";
  textInput.placeholder = "Enter text";

  // Create number input for the row
  const numberInput = document.createElement("input");
  numberInput.type = "number";
  numberInput.name = "numberInput[]";
  numberInput.placeholder = "Enter number";
  numberInput.min = "0";   // Ensure only positive numbers are allowed
  numberInput.step = "1";  // Step of 1 for integer input

  // Create file input for the row
  const fileInput = document.createElement("input");
  fileInput.type = "file";
  fileInput.name = "fileInput[]";
  fileInput.accept = "image/*";

  // Create an upload button for the row
  const uploadButton = document.createElement("button");
  uploadButton.type = "button";
  uploadButton.textContent = "Upload";
  uploadButton.onclick = () => uploadImage(fileInput, textInput);

  // Create a remove button for the row
  const removeButton = document.createElement("button");
  removeButton.type = "button";
  removeButton.textContent = "Remove";
  removeButton.onclick = () => formRow.remove();

  // Append inputs and buttons to the row
  formRow.appendChild(textInput);
  formRow.appendChild(numberInput);
  formRow.appendChild(fileInput);
  formRow.appendChild(uploadButton);
  formRow.appendChild(removeButton);

  // Append the new row to the form
  form.appendChild(formRow);
}

async function uploadImage(fileInput, textInput) {
  const file = fileInput.files[0];

  if (!file) {
    alert('Please select a file to upload.');
    return;
  }

  const formData = new FormData();
  formData.append('image', file);

  try {
    const response = await fetch(`https://api.imgur.com/3/image`, {
      method: 'POST',
      headers: {
        'Authorization': `Client-ID ${imgurClientId}`
      },
      body: formData
    });

    if (!response.ok) throw new Error('Failed to upload image');

    const data = await response.json();
    textInput.value = data.data.link; // Set the input to the Imgur URL
    alert('Upload successful! URL added to text input.');
  } catch (error) {
    console.error('Error:', error);
    alert('Error uploading the image: ' + error.message);
  }
}

// Add an initial row when the page loads
document.addEventListener("DOMContentLoaded", () => addRow());
