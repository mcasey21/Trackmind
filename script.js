
const upload = document.getElementById("trackUpload");
const preview = document.getElementById("trackPreview");

// Takes image and creates a temp URl so it can display it
upload.addEventListener("change", async () => {
    // Image preview 
    const file = upload.files[0];
    if (!file) return;

    preview.src = URL.createObjectURL(file);
    preview.hidden = false;

    // Send image to backend
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData
    });

    // Read the JSON response from FastAPI
    const result = await response.json();

    // Display the processed image
    const processedPreview = document.getElementById("processedPreview");

    processedPreview.src = "data:image/png;base64," + result.processed_image;

    // Keep text hidden until image is ready
    document.getElementById("processedSection").hidden = false;

    console.log(result);
});