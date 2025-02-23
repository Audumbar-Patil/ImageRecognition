document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('uploadForm');
    const imageInput = document.getElementById('imageInput');
    const preview = document.getElementById('preview');
    const previewImage = document.getElementById('previewImage');
    const results = document.getElementById('results');
    const resultsList = document.getElementById('resultsList');
    const error = document.getElementById('error');
    const submitBtn = document.getElementById('submitBtn');
    const spinner = submitBtn.querySelector('.spinner-border');

    // Preview image before upload
    imageInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImage.src = e.target.result;
                preview.classList.remove('d-none');
            }
            reader.readAsDataURL(file);
        }
    });

    // Handle form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const formData = new FormData();
        const file = imageInput.files[0];

        if (!file) {
            showError('Please select an image first.');
            return;
        }

        formData.append('image', file);

        // Show loading state
        setLoading(true);
        hideError();
        results.classList.add('d-none');

        try {
            const response = await fetch('/detect', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Error processing image');
            }

            displayResults(data.predictions);
        } catch (err) {
            showError(err.message);
        } finally {
            setLoading(false);
        }
    });

    function displayResults(predictions) {
        resultsList.innerHTML = '';
        predictions.forEach(pred => {
            const item = document.createElement('div');
            item.className = 'list-group-item d-flex justify-content-between align-items-center';
            item.innerHTML = `
                ${pred.label}
                <span class="badge bg-primary rounded-pill">${pred.confidence.toFixed(2)}%</span>
            `;
            resultsList.appendChild(item);
        });
        results.classList.remove('d-none');
    }

    function showError(message) {
        error.textContent = message;
        error.classList.remove('d-none');
    }

    function hideError() {
        error.classList.add('d-none');
    }

    function setLoading(isLoading) {
        submitBtn.disabled = isLoading;
        if (isLoading) {
            spinner.classList.remove('d-none');
            submitBtn.textContent = ' Processing...';
        } else {
            spinner.classList.add('d-none');
            submitBtn.textContent = 'Analyze Image';
        }
    }
});