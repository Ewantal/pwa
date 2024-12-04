// Handle the image upload
function handleImageUpload(event) {
    const file = event.target.files[0];

    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function (e) {
            // Push the image data to the uploadedImages array (no preview displayed)
            uploadedImages.push(e.target.result);
            imageCount++;

            // Check if both images have been uploaded
            if (imageCount === 2) {
                document.getElementById('createModelButton').style.display = 'block';  // Show the "Create the model" button
            }
        };
        reader.readAsDataURL(file);
    } else {
        alert('Please upload a valid image file.');
    }
}