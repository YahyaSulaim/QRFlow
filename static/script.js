const imgurClientId = "a15f86a39c45ffe";

function addRow() {
  const form = document.getElementById("dynamicForm");

  const formRow = document.createElement("div");
  formRow.classList.add("form-row");

  const textInput = document.createElement("input");
  textInput.type = "text";
  textInput.name = "textInput[]";
  textInput.placeholder = "Enter text";

  const numberInput = document.createElement("input");
  numberInput.type = "number";
  numberInput.name = "numberInput[]";
  numberInput.placeholder = "Enter number";
  numberInput.min = "0";
  numberInput.step = "1";

  const fileInput = document.createElement("input");
  fileInput.type = "file";
  fileInput.name = "fileInput[]";
  fileInput.accept = "image/*";

  const uploadButton = document.createElement("button");
  uploadButton.type = "button";
  uploadButton.textContent = "Upload";
  uploadButton.onclick = () => uploadImage(fileInput, textInput);

  const removeButton = document.createElement("button");
  removeButton.type = "button";
  removeButton.textContent = "Remove";
  removeButton.onclick = () => formRow.remove();

  formRow.appendChild(textInput);
  formRow.appendChild(numberInput);
  formRow.appendChild(fileInput);
  formRow.appendChild(uploadButton);
  formRow.appendChild(removeButton);

  form.appendChild(formRow);
}

async function uploadImage(fileInput, textInput) {
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select a file to upload.");
    return;
  }

  const formData = new FormData();
  formData.append("image", file);

  try {
    const response = await fetch(`https://api.imgur.com/3/image`, {
      method: "POST",
      headers: {
        Authorization: `Client-ID ${imgurClientId}`,
      },
      body: formData,
    });

    if (!response.ok) throw new Error("Failed to upload image");

    const data = await response.json();
    textInput.value = data.data.link;
    alert("Upload successful! URL added to text input.");
  } catch (error) {
    console.error("Error:", error);
    alert("Error uploading the image: " + error.message);
  }
}

document.addEventListener("DOMContentLoaded", () => addRow());
