const backendUrl = 'http://192.168.2.39:5000/predict';

document.getElementById('uploadButton').addEventListener('click', () => {
    document.getElementById('imageInput').click();
});

document.getElementById('imageInput').addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = () => {
            const imgElement = document.getElementById('selectedImage');
            imgElement.src = reader.result;
            imgElement.style.display = 'block';
            uploadImage(file);
        };
        reader.readAsDataURL(file);
    }
});

async function uploadImage(file) {
    const formData = new FormData();
    formData.append('image', file);
    
    document.getElementById('loading').style.display = 'block';

    try {
        const response = await fetch(backendUrl, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        document.getElementById('loading').style.display = 'none';
        document.getElementById('prediction').style.display = 'block';
        document.getElementById('artwork').innerText = `Predicted Artwork: ${data.artwork}`;
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('loading').style.display = 'none';
        document.getElementById('prediction').style.display = 'block';
        document.getElementById('artwork').innerText = 'Error predicting artwork. Please try again.';
    }
}
