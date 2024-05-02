alert("check");
const resultsDiv = document.getElementById('results');

async function displayResults(data) {
    resultsDiv.innerHTML = ''; 

    if (data.message) {
    resultsDiv.innerHTML = `<p style="color: red;">${data.message}</p>`;
    return;
    }

    for (const result of data.results) {
    const imageContainer = document.createElement('div');
    imageContainer.classList.add('image-container');
    imageContainer.style.height = '400px';
    imageContainer.style.width = '200px';

    const imageData = `data:image/jpeg;base64,${result.image}`;
    const image = document.createElement('img');
    image.style.height = '300px';
    image.style.width = '194px';
    image.src = imageData;
    if (result.match) {
        const topLeft = `(${result.top_left[0]}, ${result.top_left[1]})`;
        const bottomRight = `(${result.bottom_right[0]}, ${result.bottom_right[1]})`;
        const caption = `No Defect Detected`;
        imageContainer.appendChild(image);
        imageContainer.insertAdjacentHTML('beforeend', `<p>Image: ${result.image_name}</p>`);
        imageContainer.insertAdjacentHTML('beforeend', `<p>${caption}</p>`);
        
    } else {
        const caption = `Defect Detected`;
        imageContainer.appendChild(image);
        imageContainer.insertAdjacentHTML('beforeend', `<p>Image: ${result.image_name}</p>`);
        imageContainer.insertAdjacentHTML('beforeend', `<p>${caption}</p>`);
    }

    resultsDiv.appendChild(imageContainer);
    }
}

const form = document.querySelector('form');
form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData(form);
    const response = await fetch('/compare', {
    method: 'POST',
    body: formData
    });

    const data = await response.json();
    displayResults(data);
});